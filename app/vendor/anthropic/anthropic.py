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

        mixers = request.mixers + (request.base_ingredients or [])
        NL_req = f"mixers: {', '.join(mixers)}, moment: {request.moment}, shaker: {request.has_shaker}, tools: {request.required_tools}"
        embedding = await OpenAIService().create_embedding(NL_req)
        embedding_data = embedding.data[0].embedding

        similarity_search = await PineconeService().query(embedding_data)

        similar = []
        for item in similarity_search["matches"]:
            min_score = float(os.getenv("SIMILARITY_SEARCH_MIN_SCORE", "0.8"))

            if item["score"] > min_score:
                similar.append(item)

        if len(similar) > 0:
            # order by highest score
            similar.sort(key=lambda val: val["score"], reverse=True)
            ids = [item["id"] for item in similar]
            first = await CocktailsDB().find_first(ids)

            # if any found, return the first one
            # otherwise create a new prediction
            if first is not None:
                (
                    id,
                    name,
                    description,
                    steps,
                    is_alcoholic,
                    size,
                    cost,
                    complexity,
                    required_ingredients,
                    required_tools,
                ) = first
                model = CreateCocktailResponseSchema(
                    id=str(id),
                    name=name,
                    description=description,
                    steps=steps["steps"],
                    is_alcoholic=is_alcoholic,
                    size=size,
                    cost=cost,
                    complexity=complexity,
                    required_ingredients=required_ingredients,
                    required_tools=required_tools,
                    base_ingredients=request.base_ingredients,
                )
                return model

        query = getCreateCocktailQuery(request)
        tools = [create_cocktail["v1"]]

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
                res["base_ingredients"] = request.base_ingredients
                apiResponse = CreateCocktailResponseSchema(**res)
            else:
                raise Exception("No response from API")

            upsert_data = [
                {
                    "id": res["id"],
                    "values": embedding_data,
                    # TODO: keep this metadata?
                    "metadata": {
                        "required_ingredients": res["required_ingredients"],
                        "base_ingredients": res["base_ingredients"],
                    },
                }
            ]
            vector_upsert = await PineconeService().upsert(upsert_data)

            db_record = await CocktailsDB().upsert(apiResponse)

            print(f"Upserted vector: {vector_upsert} and db record: {db_record}")

            return apiResponse
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None
