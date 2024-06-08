from pydantic import BaseModel, Field


class CreateCocktailRequestSchema(BaseModel):
    mixers: str = Field(
        ...,
        description="The mixers of the cocktail",
        max_length=255,
        examples=["[Vodka, Gin, Tequila]", "[Vodka, Bacardi]"],
    )
    size: str = Field(
        None,
        description="The size of the cocktail",
        max_length=255,
        examples=["Shot", "Cocktail", "Longdrink", "Mocktail"],
    )
    cost: int = Field(None, description="The cost of the cocktail", examples=[5, 10])
    complexity: str = Field(
        None,
        description="The complexity of the cocktail",
        max_length=255,
        examples=["Easy", "Medium", "Hard"],
    )
    requires_tools: bool = Field(
        None,
        description="Whether the cocktail requires special tools",
    )
    previous_recipes: list = Field(
        None,
        description="The previous recipes of the cocktail",
        max_length=255,
        examples=["[Add vodka, add gin, add tequila]", "[Add vodka, add bacardi]"],
    )
    activity: str = Field(
        None,
        description="The activity or situation where the cocktail is used",
        max_length=255,
        examples=["Pool party", "relaxing", "dinner with friends"],
    )


class CreateCocktailResponseSchema(BaseModel):
    id: str = Field(
        ...,
        description="The id of the cocktail",
        max_length=255,
        examples=["a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"],
    )
    name: str = Field(
        ...,
        description="The name of the cocktail",
        max_length=255,
        examples=["Mojito Dessert", "Caipirinha Boom"],
    )
    recipe: str = Field(
        ...,
        description="The recipe of the cocktail",
        max_length=255,
        examples=["[Vodka, Gin, Tequila]", "[Vodka, Bacardi]"],
    )
    is_alcoholic: bool = Field(
        ...,
        description="Whether the cocktail is alcoholic",
    )
    mixers: str = Field(
        ...,
        description="The mixers of the cocktail",
        max_length=255,
        examples=["[Vodka, Gin, Tequila]", "[Vodka, Bacardi]"],
    )
    size: str = Field(
        ...,
        description="The size of the cocktail",
        max_length=255,
        examples=["Shot", "Cocktail", "Longdrink", "Mocktail"],
    )
    cost: str = Field(
        ...,
        description="The cost of the cocktail",
        max_length=255,
        examples=["$5", "$10"],
    )
    complexity: str = Field(
        ...,
        description="The complexity of the cocktail",
        max_length=255,
        examples=["Easy", "Medium", "Hard"],
    )
    required_ingredients: str = Field(
        ...,
        description="The required ingredients of the cocktail",
        max_length=255,
        examples=["[Vodka, Gin, Tequila]", "[Vodka, Bacardi]"],
    )
    required_tools: str = Field(
        ...,
        description="The required tools of the cocktail",
        max_length=255,
        examples=["[Vodka, Gin, Tequila]", "[Vodka, Bacardi]"],
    )
