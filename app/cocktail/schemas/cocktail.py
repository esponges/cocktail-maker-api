from pydantic import BaseModel, Field
from typing import List, Dict


class CreateCocktailRequestSchema(BaseModel):
    mixers: list = Field(
        ...,
        description="The mixers of the cocktail",
        max_length=255,
        examples=[["Vodka", "Gin", "Tequila"], ["Vodka", "Bacardi"]],
    )
    suggest_mixers: bool = Field(
        False,
        description="Whether to suggest mixers",
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
    required_tools: list = Field(
        None,
        description="A list of required tools",
    )
    previous_recipes: list = Field(
        None,
        description="The previous recipes of the cocktail",
        max_length=255,
        examples=["Add vodka, add gin, add tequila", "Add vodka, add bacardi"],
    )
    moment: str = Field(
        None,
        description="The activity or situation where the cocktail is used",
        max_length=255,
        examples=["Pool party", "relaxing", "dinner with friends"],
    )
    has_shaker: bool = Field(
        None,
        description="Whether the cocktail has a shaker",
    )


class CreateCocktailResponseSchema(BaseModel):
    id: str = Field(
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
    description: str = Field(
        ...,
        description="The recipe of the cocktail",
        examples=["A powerful cocktail", "A classic cocktail"],
    )
    steps: List[Dict[str, str]] = Field(
        description="The steps of the cocktail.",
        examples=[
            {"description": "Step 1", "index": 1},
            {"description": "Step 2", "index": 2},
        ],
    )
    is_alcoholic: bool = Field(
        ...,
        description="Whether the cocktail is alcoholic",
    )
    mixers: list = Field(
        ...,
        description="The mixers of the cocktail",
        max_length=255,
        examples=[["Vodka", "Gin", "Tequila"], ["Vodka", "Bacardi"]],
    )
    size: str = Field(
        ...,
        description="The size of the cocktail",
        max_length=255,
        examples=["Shot", "Cocktail", "Longdrink", "Mocktail"],
    )
    cost: float = Field(
        ...,
        description="The cost of the cocktail",
        examples=[5, 10],
    )
    complexity: str = Field(
        ...,
        description="The complexity of the cocktail",
        max_length=255,
        examples=["Easy", "Medium", "Hard"],
    )
    required_ingredients: list = Field(
        ...,
        description="The required ingredients of the cocktail",
        max_length=255,
        examples=[["Vodka", "Gin", "Tequila"], ["Vodka", "Bacardi"]],
    )
    required_tools: list = Field(
        description="The required tools of the cocktail",
        max_length=255,
        examples=[
            ["Shaker", "Vodka", "Gin", "Tequila"],
            ["Shaker", "Jigger", "Bacardi"],
        ],
    )
