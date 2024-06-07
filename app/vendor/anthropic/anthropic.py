from anthropic import Anthropic
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
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
                        "recipe": {
                            "type": "string",
                            "description": "The step by step recipe of the cocktail.",
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
                        "recipe",
                        "is_alcoholic",
                        "mixers",
                        "size",
                        "cost",
                        "complexity",
                        "requires_tools",
                    ],
                },
            }
        ]

        query = f"""
        <text>
            You are a masterful cocktail creator.
            Create a well detailed step by step (step 1 - do this, step 2 - do that, etc.) cocktail based on the input.
            First specify a list of the required ingredients and tools (if any).

            - It should use the following mixers: {request.mixers.join(", ")}. You could suggest a brand if only raw mixers are provided.
            - Its size should be {request.size or "Unknown"}". Options are: Shot, Cocktail, Longdrink, Mocktail.
            - Its raw cost should be of {request.cost or "5"} USD".
            - Its complexity should be {request.complexity or "Medium"}". Options are: Easy, Medium, Hard.
            - Should require mixing tools: {request.requires_tools or "False"}".
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

        # TODO: store in vector store

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

        # return CreateCocktailResponseSchema(**res) // todo: return schema
        return JSONResponse(content=res)
