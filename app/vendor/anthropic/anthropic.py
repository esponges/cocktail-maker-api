from anthropic import Anthropic
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
    CreateCocktailResponseSchema,
)
import json
import os


class AnthropicService:
    MODEL_NAME = "claude-3-haiku-20240307"

    def __init__(self):
        print("gooo", os.environ.get("ANTHROPIC_API_KEY"))
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def create_cocktail(
        self, request: CreateCocktailRequestSchema
    ) -> CreateCocktailResponseSchema:
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
                            "description": "The step by step recipe of the cocktail. One or two paragraphs max. It should be as specific as possible.",
                        },
                    },
                    "required": ["name"],
                },
            }
        ]

        query = f"""
        <text>
            You are a masterful cocktail creator. Create a cocktail based on the following input.
            - It should use the following mixers: {request.mixers.join(", ")}.
            - Its size should be {request.size or "Unknown"}".
            - Its raw cost should be of {request.cost or "5"} USD".
            - Its complexity should be {request.complexity or "Medium"}".
            - Should require mixing tools: {request.requires_tools or "False"}".
        </text>

        Use the create_cocktail tool.
        """

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=4096,
            tools=tools,
            messages=[
                {"role": "user", "content": query}
            ],
        )

        print(response)

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

        return res
