from anthropic import Anthropic
from anthropic.types import ToolParam
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
        #     {
        #     "name": "print_summary",
        #     "description": "Prints a summary of the article.",
        #     "input_schema": {
        #         "type": "object",
        #         "properties": {
        #             "author": {"type": "string", "description": "Name of the article author"},
        #             "topics": {
        #                 "type": "array",
        #                 "items": {"type": "string"},
        #                 "description": 'Array of topics, e.g. ["tech", "politics"]. Should be as specific as possible, and can overlap.'
        #             },
        #             "summary": {"type": "string", "description": "Summary of the article. One or two paragraphs max."},
        #             "coherence": {"type": "integer", "description": "Coherence of the article's key points, 0-100 (inclusive)"},
        #             "persuasion": {"type": "number", "description": "Article's persuasion score, 0.0-1.0 (inclusive)"}
        #         },
        #         "required": ['author', 'topics', 'summary', 'coherence', 'persuasion', 'counterpoint']
        #     }
        # }

        # tools: ToolParam = [
        #     {
        #         "name": "create_cocktail",
        #         "description": "Get the current weather in a given location",
        #         "input_schema": {
        #             "type": "object",
        #             "properties": {
        #                 "location": {
        #                     "type": "string",
        #                     "description": "The city and state, e.g. San Francisco, CA",
        #                 }
        #             },
        #             "required": ["location"],
        #         },
        #     }
        # ]
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
