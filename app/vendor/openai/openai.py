from openai import OpenAI
import os


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def create_embedding(self, text: str):
        return self.client.embeddings.create(input=text, model="text-embedding-ada-002")

      
