from app.cocktail.schemas.cocktail import (
    CreateCocktailRequestSchema,
    CreateCocktailResponseSchema,
)


class CocktailService:
    async def create_cocktail(
        self, request: CreateCocktailRequestSchema
    ) -> CreateCocktailResponseSchema:
        return CreateCocktailResponseSchema(
            id="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            name="Mojito Dessert",
            recipe="[Vodka, Gin, Tequila]",
            is_alcoholic=True,
            mixers="[Vodka, Gin, Tequila]",
            size="Shot",
            cost="$5",
            complexity="Easy",
            required_ingredients="None",
            required_tools="None",
        )
