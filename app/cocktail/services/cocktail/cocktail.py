
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
)
from app.vendor.anthropic.anthropic import AnthropicService

class CocktailService:
    async def create_cocktail(
        self, request: CreateCocktailRequestSchema):
        return await AnthropicService().create_cocktail(request)
