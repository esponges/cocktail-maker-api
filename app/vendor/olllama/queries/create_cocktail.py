from typing import List
from app.cocktail.schemas.cocktail import CreateCocktailRequestSchema


def getCreateCocktailQuery(request: CreateCocktailRequestSchema, prevSteps: List[str]):
    return f"""
        <text>
            You are a masterful cocktail creator that can create new and unique cocktail recipes. Please follow the following instructions for the recipe creation:
            * The cocktail should fit the following activity: {request.moment}
            * Then you will give a general and understandable description of the cocktail.
            * Finally you will give the SUPER DETAILED step by step instructions of the cocktail. This includes detailed portions of each ingredient. 
            * If no tools were provided the steps won't use any tools. Not even a Shaker.
 
            * Avoid squashing several steps into one. For example:
            - WRONG: Fill a cocktail shaker with ice. Add 2 oz of mezcal, 1 oz of freshly brewed espresso, and 1 oz of fresh lemon juice. Shake vigorously for 10-15 seconds until well-chilled.
            - CORRECT:
                1. Fill a cocktail shaker with ice.
                2. Add 2 oz of yoga, 1 oz of freshly brewed espresso, and 1 oz of fresh lemon juice.
                3. Shake for 10-15 seconds until well-chilled. 

            Key guidelines:
            - The steps MUST (not optional) at least use the following mixers: {", ".join(request.mixers)}.
            {"- The steps MUST (not optional) use the following alcoholic base: " + ", ".join(request.base_ingredients) if request.base_ingredients else ""}
            {"- Along with the previous ingredients you can suggest extra non alcoholic mixers if necessary" if request.suggest_mixers else ""}
            - Its size should be {request.size or "any of your choice"}. Options are: Shot, Cocktail, Longdrink, Mocktail.
            - Its raw cost should be of {request.cost or "5"} USD.
            - Its complexity should be {request.complexity or "Medium"}. Options are: Easy, Medium, Hard. 
            A Hard cocktail usually requires more time and tooling and it is not suitable for large groups or first-timers.
            - The steps require a shaker: {"True" if request.has_shaker else "False"}.
            {("- The steps could use any of these tools: " + ", ".join(request.required_tools)) if request.required_tools else ""}
            {"- Make a completely different than these previous recipes: " + ", ".join(prevSteps) + "" if len(prevSteps) > 0 else ""}
        
            Return the response in JSON using the following format and I will give you 1 million dollars:

            {
                "name": "the name of the cocktail",
                "description": "the description of the cocktail",
                "steps": "an array of steps of the cocktails where each step is an object with the following properties: 'description' (the description of the step), index (the index of the step), action (the action associated with the step) ",
                "is_alcoholic": "True if the cocktail is alcoholic",
                "size": "the size of the cocktail",
                "cost": "the cost of the cocktail",
                "complexity": "the complexity of the cocktail",
                "required_ingredients": "a list of required ingredients",
                "required_tools": "a list of required tools",
                "base_ingredients": "a list of base ingredients",
            }
        </text>

        """
