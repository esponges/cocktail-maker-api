
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
)
from app.vendor.anthropic.anthropic import AnthropicService
from app.vendor.olllama.ollama import OllamaService

class CocktailService:
    async def create_cocktail(
        self, request: CreateCocktailRequestSchema, vendor: str):
        # TODO: implement similarity search from vector store before creating a new one

        res = None
        if vendor == "ollama":
            res = await OllamaService().create_cocktail(request)
        else:
            res = await AnthropicService().create_cocktail(request)

        # TODO: parse the steps and use existing images from cdn

        return res
