from anthropic import Anthropic
import uuid
import os

from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
    CreateCocktailResponseSchema,
)
from app.vendor.openai.openai import OpenAIService
from app.vendor.pinecone.pinecone import PineconeService
from core.db.cocktails.cocktails import CocktailsDB

class AnthropicService:
    MODEL_NAME = "claude-3-5-sonnet-20240620"

    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def create_cocktail(self, request: CreateCocktailRequestSchema):
        tools = [
            {
                "name": "create_cocktail",
                "description": "Create a trendy cocktail based on the input",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the cocktail",
                        },
                        "description": {
                            "type": "string",
                            "description": "A description of the cocktail — this is NOT the steps",
                        },
                        "steps": {
                            "type": "array",
                            "description": "The steps of the cocktail.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {
                                        "type": "string",
                                        "description": "The super detailed description of what to do. Includes portion sizes, directions, etc.",
                                    },
                                    "index": {
                                        "type": "string",
                                        "description": "The index of the step",
                                    },
                                    # todo: return an action that can be associated with an image from the cdn
                                },
                            },
                        },
                        "is_alcoholic": {
                            "type": "boolean",
                            "description": "Whether the cocktail is alcoholic",
                        },
                        "size": {
                            "type": "string",
                            "description": "The size of the cocktail",
                        },
                        "cost": {
                            "type": "integer",
                            "description": "The cost of the cocktail",
                        },
                        "complexity": {
                            "type": "string",
                            "description": "The complexity of the cocktail",
                        },
                        "required_ingredients": {
                            "type": "array",
                            "description": "A list of required ingredients",
                            "items": {
                                "type": "string",
                                "description": "The name of the required ingredient, not the same as the name of the mixers",
                            },
                        },
                        "required_tools": {
                            "type": "array",
                            "description": "A list of required tools. Could be empty if no tools are required",
                            "items": {
                                "type": "string",
                                "description": "The name of the required tool",
                            },
                        },
                    },
                    "required": [
                        "name",
                        "description",
                        "steps",
                        "is_alcoholic",
                        "size",
                        "cost",
                        "complexity",
                        "required_ingredients",
                    ],
                },
            }
        ]

        query = f"""
        <text>
            You are a masterful cocktail creator that can create new and unique cocktail recipes. Please follow the following instructions for the recipe creation:
            * The cocktail should fit the following activity: {request.moment}
            * Then you will give a general and understandable description of the cocktail.
            * Finally you will give the SUPER DETAILED step by step instructions of the cocktail. This includes detailed portions of each ingredient. 
            If no tools were provided the steps won't use any tools. Not even a Shaker. 
            Avoid squashing several steps into one. For example:

            - WRONG: Fill a cocktail shaker with ice. Add 2 oz of mezcal, 1 oz of freshly brewed espresso, and 1 oz of fresh lemon juice. Shake vigorously for 10-15 seconds until well-chilled.
            - CORRECT:
                1. Fill a cocktail shaker with ice.
                2. Add 2 oz of yoga, 1 oz of freshly brewed espresso, and 1 oz of fresh lemon juice.
                3. Shake for 10-15 seconds until well-chilled. 

            Key guidelines:
            - The steps MUST (not optional) at least use the following mixers: {", ".join(request.mixers)}.
            {"Along with the previous ingredients you can suggest extra mixers if necessary" if request.suggest_mixers else ""}
            - Its size should be {request.size or "any of your choice"}. Options are: Shot, Cocktail, Longdrink, Mocktail.
            - Its raw cost should be of {request.cost or "5"} USD.
            - Its complexity should be {request.complexity or "Medium"}. Options are: Easy, Medium, Hard. 
            A Hard cocktail usually requires more time and tooling and it is not suitable for large groups or first-timers.
            - The steps require a shaker: {"True" if request.has_shaker else "False"}.
            {("- The steps could use any of these tools: " + ", ".join(request.required_tools)) if request.required_tools else ""}
            {"- Make a completely different than these previous: {request.previous_recipes}" if request.previous_recipes else ""}
        </text>

        Use the create_cocktail tool.
        """

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=4096,
            tools=tools,
            messages=[{"role": "user", "content": query}],
            temperature=1,
        )

        # TODO: store in vector store (also in a regular DB?)

        res = None
        for content in response.content:
            if content.type == "tool_use" and content.name == "create_cocktail":
                res = content.input
                break

        try:
            if res is not None:
                res["id"] = str(uuid.uuid4())
                apiResponse = CreateCocktailResponseSchema(**res)
            else:
                raise Exception("No response from API")

            # TODO: figure out what to really embed, probably the query
            # is not the right thing to embed, but something more specific
            # like the mixers and tools which are more user specific
            # also some metadata would be nice for metadata search
            embedding = await OpenAIService().create_embedding(query)
            embedding_data = embedding.data[0].embedding
            # {"id": "vec1", "values": [1.0, 1.5]},
            # use required ingredients as metadata

            vector = [{"id": res["id"], "values": embedding_data, "metadata": { "required_ingredients": res["required_ingredients"] }}]
            vector_upsert = await PineconeService().upsert(vector)

            db_record = await CocktailsDB().upsert(apiResponse)

            print(f"Upserted vector: {vector_upsert} and db record: {db_record}")

            return apiResponse
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None
