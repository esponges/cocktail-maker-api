from anthropic import Anthropic
from anthropic.types import ToolParam
import json
import os



class AnthropicService:
    client = None
    MODEL_NAME = "claude-3-haiku-20240307"

    def __init__(self):
        print('gooo', os.environ.get("ANTHROPIC_API_KEY"))
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def create_cocktail(self):
        tools = [
            {
                "name": "print_sentiment_scores",
                "description": "Prints the sentiment scores of a given text.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "positive_score": {
                            "type": "number",
                            "description": "The positive sentiment score, ranging from 0.0 to 1.0.",
                        },
                        "negative_score": {
                            "type": "number",
                            "description": "The negative sentiment score, ranging from 0.0 to 1.0.",
                        },
                        "neutral_score": {
                            "type": "number",
                            "description": "The neutral sentiment score, ranging from 0.0 to 1.0.",
                        },
                    },
                    "required": ["positive_score", "negative_score", "neutral_score"],
                },
            }
        ]

        text = "The product was okay, but the customer service was terrible. I probably won't buy from them again."

        query = f"""
    <text>
    {text}
    </text>

    Use the print_sentiment_scores tool.
    """

        response = self.client.messages.create(
            model=self.MODEL_NAME,
            max_tokens=4096,
            tools=tools,
            messages=[{"role": "user", "content": query}],
        )

        json_sentiment = None
        for content in response.content:
            if content.type == "tool_use" and content.name == "print_sentiment_scores":
                json_sentiment = content.input
                break

        if json_sentiment:
            print("Sentiment Analysis (JSON):")
            print(json.dumps(json_sentiment, indent=2))
        else:
            print("No sentiment analysis found in the response.")
