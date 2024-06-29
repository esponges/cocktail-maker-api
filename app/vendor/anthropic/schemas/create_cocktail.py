create_cocktail = {
    "v1": {
        "name": "create_cocktail",
        "description": "Create a trendy cocktail based on the input",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the cocktail",
                },
                "description": {
                    "type": "string",
                    "description": "A description of the cocktail — this is NOT the steps",
                },
                "steps": {
                    "type": "array",
                    "description": "The steps of the cocktail.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "The super detailed description of what to do. Includes portion sizes, directions, etc.",
                            },
                            "index": {
                                "type": "string",
                                "description": "The index of the step",
                            },
                            # todo: return an action that can be associated with an image from the cdn
                        },
                    },
                },
                "is_alcoholic": {
                    "type": "boolean",
                    "description": "Whether the cocktail is alcoholic",
                },
                "size": {
                    "type": "string",
                    "description": "The size of the cocktail",
                },
                "cost": {
                    "type": "integer",
                    "description": "The cost of the cocktail",
                },
                "complexity": {
                    "type": "string",
                    "description": "The complexity of the cocktail",
                },
                "required_ingredients": {
                    "type": "array",
                    "description": "A list of required ingredients",
                    "items": {
                        "type": "string",
                        "description": "The name of the required ingredient, not the same as the name of the mixers",
                    },
                },
                "required_tools": {
                    "type": "array",
                    "description": "A list of required tools. Could be empty if no tools are required",
                    "items": {
                        "type": "string",
                        "description": "The name of the required tool",
                    },
                },
            },
            "required": [
                "name",
                "description",
                "steps",
                "is_alcoholic",
                "size",
                "cost",
                "complexity",
                "required_ingredients",
            ],
        },
    }
}
