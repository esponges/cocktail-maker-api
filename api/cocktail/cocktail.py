from fastapi import APIRouter
from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
    CreateCocktailResponseSchema,
)
from app.cocktail.services.cocktail.cocktail import CocktailService

cocktail_router = APIRouter()


@cocktail_router.post("/create", response_model=CreateCocktailResponseSchema)
async def create_cocktail(request: CreateCocktailRequestSchema):
    return await CocktailService().create_cocktail(request)
