# from anthropic import Anthropic
# import uuid
# import os
from functools import reduce
import ollama

from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
    # CreateCocktailResponseSchema,
)
# from app.vendor.openai.openai import OpenAIService
# from app.vendor.pinecone.pinecone import PineconeService
from core.db.cocktails.cocktails import CocktailsDB
# from app.vendor.anthropic.schemas.create_cocktail import create_cocktail
from app.vendor.olllama.queries.create_cocktail import getCreateCocktailQuery


class OllamaService:
    # MODEL_NAME = "claude-3-5-sonnet-20240620"

    async def create_cocktail(self, request: CreateCocktailRequestSchema):

        # mixers = request.mixers + (request.base_ingredients or [])
        # NL_req = f"mixers: {', '.join(mixers)}, moment: {request.moment}, shaker: {request.has_shaker}, tools: {request.required_tools}"
        # embedding = await OpenAIService().create_embedding(NL_req)
        # embedding_data = embedding.data[0].embedding

        # previous_recipes is populated it means that the user wants to retry using the same parameters
        previous_recipes_steps = []
        
            # using the ids from the previous recipes get the steps for each one
        batch = await CocktailsDB().find_batch(request.previous_recipes)

        for item in batch:
            steps = reduce(lambda acc, val: acc + " " + val['description'], item[3]["steps"], "")
            print(steps)
            
            previous_recipes_steps.append(steps)
        
        query = getCreateCocktailQuery(request, previous_recipes_steps)

        response = ollama.generate(
            format="json",
            model="gemma2:2b",
            stream=False,
            prompt=query,
        )

        print(response)

        return response

        # TODO: store in vector store (also in a regular DB?)

        # res = None
        # for content in response.content:
        #     if content.type == "tool_use" and content.name == "create_cocktail":
        #         res = content.input
        #         break

        # try:
        #     if res is not None:
        #         res["id"] = str(uuid.uuid4())
        #         res["base_ingredients"] = request.base_ingredients
        #         apiResponse = CreateCocktailResponseSchema(**res)
        #     else:
        #         raise Exception("No response from API")

        #     upsert_data = [
        #         {
        #             "id": res["id"],
        #             "values": embedding_data,
        #             # TODO: keep this metadata?
        #             "metadata": {
        #                 "required_ingredients": res["required_ingredients"],
        #                 "base_ingredients": res["base_ingredients"],
        #             },
        #         }
        #     ]
        #     vector_upsert = await PineconeService().upsert(upsert_data)

        #     db_record = await CocktailsDB().upsert(apiResponse)

        #     print(f"Upserted vector: {vector_upsert} and db record: {db_record}")

        #     return apiResponse
        # except Exception as e:
        #     print(f"Error parsing response: {e}")
        #     return None
