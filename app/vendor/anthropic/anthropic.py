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
from app.vendor.anthropic.schemas.create_cocktail import create_cocktail
from app.vendor.anthropic.queries.create_cocktail import getCreateCocktailQuery

class AnthropicService:
    MODEL_NAME = "claude-3-5-sonnet-20240620"

    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def create_cocktail(self, request: CreateCocktailRequestSchema):
        # TODO: do a similarity search from vector store before creating a new one
        # if the score is low, then create a new one otherwise return the existing db record

        query = getCreateCocktailQuery(request)
        
        embedding = await OpenAIService().create_embedding(query)
        embedding_data = embedding.data[0].embedding

        similarity_search = await PineconeService().query(embedding_data)

        # filter all the elements that score above 0.8
        similar = []
        for item in similarity_search["matches"]:
            # todo: is this the right val?
            if item["score"] > 0.8:
                similar.append(item)

        if len(similar) > 0:
            # order by highest score
            similar.sort(key=lambda x: x["score"], reverse=True)
            ids = [item["id"] for item in similar]
            first = await CocktailsDB().find_first(ids)

            # if any found, return the first one
            if first is not None:
                return first
        
        tools = [create_cocktail["v1"]]

        return tools

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

            embedding = await OpenAIService().create_embedding(query)
            embedding_data = embedding.data[0].embedding

            upsert_data = [
                {
                    "id": res["id"],
                    "values": embedding_data,
                    # TODO: figure out what to really embed, probably the query
                    # is not the right thing to embed, but something more specific
                    # like the mixers and tools which are more user specific
                    # also some metadata would be nice for metadata search
                    "metadata": {"required_ingredients": res["required_ingredients"]},
                }
            ]
            vector_upsert = await PineconeService().upsert(upsert_data)

            db_record = await CocktailsDB().upsert(apiResponse)

            print(f"Upserted vector: {vector_upsert} and db record: {db_record}")

            return apiResponse
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None
