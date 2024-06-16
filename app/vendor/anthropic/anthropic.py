from anthropic import Anthropic
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
    # CreateCocktailResponseSchema,
)
from fastapi.responses import JSONResponse
import json
import os


class AnthropicService:
    MODEL_NAME = "claude-3-haiku-20240307"

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
                            "description": "A description of the cocktail — this is NOT the recipe",
                        },
                        "steps": {
                            "type": "array",
                            "description": "The steps of the cocktail.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {
                                        "type": "string",
                                        "description": "The description of what to do",
                                    },
                                    "index": {
                                        "type": "integer",
                                        "description": "The index of the step",
                                    },
                                    # todo: return an action that can be associated with an image from the cdn
                                }
                            },
                        },
                        "is_alcoholic": {
                            "type": "boolean",
                            "description": "Whether the cocktail is alcoholic",
                        },
                        "mixers": {
                            "type": "array",
                            "description": "The mixers of the cocktail",
                            "items": {
                                "type": "string",
                                "description": "The mixers of the cocktail.",
                            },
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
                                "description": "The name of the required ingredient",
                            },
                        },
                        "required_tools": {
                            "type": "array",
                            "description": "A list of required tools",
                            "items": {
                                "type": "string",
                                "description": "The name of the required tool",
                            },
                        },
                    },
                    "required": [
                        "name",
                        "description",
                        "steps"
                        "is_alcoholic",
                        "mixers",
                        "size",
                        "cost",
                        "complexity",
                        "required_ingredients",
                        "required_tools",
                    ],
                },
            }
        ]

        query = f"""
        <text>
            You are a masterful cocktail creator that can create new and unique cocktail recipes. Please follow the following instructions for the recipe creation:
            * Your recipes will be in markdown format.
            * The cocktail should fit the following activity: {request.moment}
            * First you will give a list of required tools and items to use.
            * Then you will give a detailed description of the cocktail.
            * Finally you will give the step by step instructions of the cocktail.

            Key guidelines:
            - The recipe MUST (not optional) at least use: {" ".join(request.mixers)}. You could suggest a brand if only raw mixers are provided.
            - Its size should be {request.size or "Unknown"}". Options are: Shot, Cocktail, Longdrink, Mocktail.
            - Its raw cost should be of {request.cost or "5"} USD".
            - Its complexity should be {request.complexity or "Medium"}". Options are: Easy, Medium, Hard.
            - It could use some of these mixing tools: {" ".join(request.required_tools) or "False"}".
            {f"- Make a completely different than these previous: {request.previous_recipes}" if request.previous_recipes else ""}
        </text>

        Use the create_cocktail tool.
        """

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=4096,
            tools=tools,
            messages=[{"role": "user", "content": query}],
            temperature=0.7,
        )

        # TODO: store in vector store (also in a regular DB?)

        res = None
        for content in response.content:
            if content.type == "tool_use" and content.name == "create_cocktail":
                res = content.input
                break

        if res:
            print("Cocktail response (JSON):")
            print(json.dumps(res, indent=2))
        else:
            print("No Cocktail response found in the response.")

        try :
            # return CreateCocktailResponseSchema(**res)
            return JSONResponse(res)
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None
        
