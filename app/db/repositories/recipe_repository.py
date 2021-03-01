from typing import Dict, List

from sqlalchemy import text
from sqlalchemy.orm import Query

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
            query = self._add_sorting(query, sort_params)

        if filters:
            query = self._add_filters(query, filters)

        recipes = await self.db.fetch_all(query)

        return [RecipeModel(**recipe) for recipe in recipes]

    async def get_one(self, id: str):
        query = RecipeOrm.table().select().where(RecipeOrm.table().c["id"] == id)
        recipe = await self.db.fetch_one(query)

        return RecipeModel(**recipe)

    async def update_recipe(
        self, id: str, updated_recipe: UpdatedRecipeModel
    ) -> RecipeModel:
        query = (
            RecipeOrm.table()
            .update()
            .where(RecipeOrm.table().c["id"] == id)
            .values(**updated_recipe.dict())
        )
        await self.db.execute(query)

        return await self.get_one(id)

    async def delete_recipe(self, id: str) -> RecipeModel:
        recipe = await self.get_one(id)

        query = RecipeOrm.table().delete().where(RecipeOrm.table().c["id"] == id)
        await self.db.execute(query)

        return recipe

    def _add_sorting(self, query: Query, sort_params: Dict[str, str]):
        for sort_key, sort_value in sort_params.items():
            if sort_value == "asc":
                query = query.order_by(RecipeOrm.table().c[sort_key].asc())
            elif sort_value == "desc":
                query = query.order_by(RecipeOrm.table().c[sort_key].desc())
        return query

    def _add_filters(self, query: Query, filters: List[str]):

        for filter_param in filters:
            query = query.where(text(filter_param))

        return query
