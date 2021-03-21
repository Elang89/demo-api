from typing import Dict, List, Optional

from sqlalchemy import select  # type: ignore

from app.db.repositories.base import BaseRepository
from app.models.ingredient import IngredientForRecipe, IngredientOrm
from app.models.recipe import (
    RecipeModel,
    RecipeModelWithIngredients,
    RecipeOrm,
    UpdatedRecipeModel,
)
from app.models.recipes_ingredients import recipes_ingredients

RECIPES_TABLE = "recipes"
INGREDIENTS = "ingredients"


class RecipeRepository(BaseRepository):
    async def create_recipe(
        self,
        recipe: RecipeModelWithIngredients,
    ) -> RecipeModelWithIngredients:
        recipe_values = recipe.dict()
        ingredients = [
            (recipe.id, ingredient.get("id"))
            for ingredient in recipe_values.get(INGREDIENTS)  # type: ignore
        ]
        recipe_values.pop(INGREDIENTS)

        sql1 = RecipeOrm.table().insert().values(recipe_values)
        sql2 = recipes_ingredients.insert().values(ingredients)

        await self.db.execute(sql1)
        await self.db.execute(sql2)

        return recipe

    async def get_recipes(
        self,
        limit: int,
        offset: int,
        sort_params: Dict[str, str] = None,
        filters: List[str] = None,
    ) -> List[RecipeModel]:

        query = RecipeOrm.table().select().limit(limit).offset(offset)

        if sort_params:
            query = self._add_sorting(query, sort_params, RecipeOrm.table())

        if filters:
            query = self._add_filters(query, filters, RecipeOrm.table())

        recipes = await self.db.fetch_all(query)

        return [RecipeModel(**recipe) for recipe in recipes]

    async def get_one_recipe(self, id: str) -> Optional[RecipeModelWithIngredients]:
        recipes_table = RecipeOrm.table()
        ingredients_table = IngredientOrm.table()

        join = ingredients_table.join(
            recipes_ingredients,
            (ingredients_table.c.id == recipes_ingredients.c.ingredient_id)
            & (recipes_ingredients.c.recipe_id == id),
            isouter=False,
        )

        ingredients_query = select(
            [ingredients_table.c.id, ingredients_table.c.name],
        ).select_from(join)
        recipe_query = recipes_table.select().where(recipes_table.c.id == id)

        ingredients = await self.db.fetch_all(ingredients_query)
        recipe = await self.db.fetch_one(recipe_query)

        if recipe is None:
            return None

        return RecipeModelWithIngredients(
            id=recipe.get("id"),
            name=recipe.get("name"),
            description=recipe.get("description"),
            ingredients=[
                IngredientForRecipe(**ingredient) for ingredient in ingredients
            ],
        )

    async def update_recipe(
        self,
        id: str,
        updated_recipe: UpdatedRecipeModel,
    ) -> Optional[RecipeModelWithIngredients]:
        recipe_table = RecipeOrm.table()
        recipe: Optional[RecipeModelWithIngredients] = await self.get_one_recipe(id)

        if recipe is None:
            return None

        update_values = {
            recipe_key: recipe_val
            for recipe_key, recipe_val in updated_recipe.dict().items()
            if recipe_val is not None
        }

        ingredients_to_delete = [
            ingredient
            for ingredient in update_values.get(INGREDIENTS)  # type: ignore
            if ingredient.get("is_deleted") is True
        ]

        update_values.pop(INGREDIENTS)

        sql = (
            recipe_table.update().where(recipe_table.c.id == id).values(**update_values)
        )

        for ingredient in ingredients_to_delete:
            ingredient_sql = recipes_ingredients.delete().where(
                recipes_ingredients.c.ingredient_id == ingredient.get("id"),
            )
            await self.db.execute(ingredient_sql)

        await self.db.execute(sql)

        return await self.get_one_recipe(id)

    async def delete_recipe(self, id: str) -> Optional[RecipeModelWithIngredients]:
        recipe: Optional[RecipeModelWithIngredients] = await self.get_one_recipe(id)
        recipe_table = RecipeOrm.table()

        if recipe is None:
            return None

        sql = recipe_table.delete().where(RecipeOrm.table().c.id == id)
        await self.db.execute(sql)

        return recipe
