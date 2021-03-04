from typing import Dict, List, Optional

from app.db.repositories.base import BaseRepository
from app.models.recipe import RecipeModel, RecipeOrm, UpdatedRecipeModel

RECIPES_TABLE = "recipes"


class RecipeRepository(BaseRepository):
    async def create_recipe(self, recipe: RecipeModel) -> RecipeModel:
        sql = RecipeOrm.table().insert().values(**recipe.dict())
        await self.db.execute(sql)

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

    async def get_one_recipe(self, id: str) -> Optional[RecipeModel]:
        query = RecipeOrm.table().select().where(RecipeOrm.table().c["id"] == id)
        recipe = await self.db.fetch_one(query)

        if recipe is None:
            return None

        return RecipeModel(**recipe)

    async def update_recipe(
        self, id: str, updated_recipe: UpdatedRecipeModel
    ) -> Optional[RecipeModel]:

        recipe: Optional[RecipeModel] = await self.get_one_recipe(id)

        if recipe is None:
            return None

        values = {
            recipe_key: recipe_val
            for recipe_key, recipe_val in updated_recipe.dict().items()
            if recipe_val is not None
        }

        query = (
            RecipeOrm.table()
            .update()
            .where(RecipeOrm.table().c["id"] == id)
            .values(**values)
        )
        await self.db.execute(query)

        return await self.get_one_recipe(id)

    async def delete_recipe(self, id: str) -> Optional[RecipeModel]:
        recipe: Optional[RecipeModel] = await self.get_one_recipe(id)

        if recipe is None:
            return None

        query = RecipeOrm.table().delete().where(RecipeOrm.table().c["id"] == id)
        await self.db.execute(query)

        return recipe
