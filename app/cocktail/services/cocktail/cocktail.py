
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
)
from app.vendor.anthropic.anthropic import AnthropicService

class CocktailService:
    async def create_cocktail(
        self, request: CreateCocktailRequestSchema):
        # TODO: implement similarity search from vector store before creating a new one

        res = await AnthropicService().create_cocktail(request)

        # TODO: parse the steps and use existing images from cdn

        return res
