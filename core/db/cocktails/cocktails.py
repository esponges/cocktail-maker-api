import psycopg
import os

from app.cocktail.schemas.cocktail import CreateCocktailResponseSchema


class CocktailsDB:
    def __init__(self):
        self.client = psycopg.connect(
            host=os.environ.get("COCKROACH_DB_HOST"),
            user=os.environ.get("COCKROACH_DB_USER"),
            password=os.environ.get("COCKROACH_DB_PASSWORD") or "",
            dbname="cocktails",
            port=os.environ.get("COCKROACH_DB_PORT") or 123456,
        )

    async def instance(self):
        return self.client

    async def upsert(self, data: CreateCocktailResponseSchema):
        with self.client.cursor() as cur:
            cur.execute(
                """
                INSERT INTO predictions (id, name, description, steps, is_alcoholic, size, cost, complexity, required_ingredients, required_tools)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    steps = EXCLUDED.steps,
                    is_alcoholic = EXCLUDED.is_alcoholic,
                    size = EXCLUDED.size,
                    cost = EXCLUDED.cost,
                    complexity = EXCLUDED.complexity,
                    required_ingredients = EXCLUDED.required_ingredients,
                    required_tools = EXCLUDED.required_tools
                """,
                (
                    data.id,
                    data.name,
                    data.description,
                    data.model_dump_json(include={"steps"}),
                    data.is_alcoholic,
                    data.size,
                    data.cost,
                    data.complexity,
                    data.required_ingredients,
                    data.required_tools,
                ),
            )
            self.client.commit()

            return data
        
    # returns the first match from a list of ids
    async def find_first(self, ids: list):
        with self.client.cursor() as cur:
            cur.execute(
                "SELECT * FROM predictions WHERE id = ANY(%s)",
                (ids,),
            )
            return cur.fetchone()
