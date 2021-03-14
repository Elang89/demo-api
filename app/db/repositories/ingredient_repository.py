from typing import Dict, List, Optional

from sqlalchemy.sql import select

from app.db.repositories.base import BaseRepository
from app.models.ingredient import (
    IngredientForRecipe,
    IngredientModel,
    IngredientOrm,
    UpdatedIngredientModel,
)
from app.models.recipes_ingredients import recipes_ingredients


class IngredientRepository(BaseRepository):
    async def create_ingredient(self, ingredient: IngredientModel) -> IngredientModel:
        sql = IngredientOrm.table().insert().values(**ingredient.dict())
        await self.db.execute(sql)

        return ingredient

    async def get_ingredients(
        self,
        limit: int,
        offset: int,
        sort_params: Dict[str, str] = None,
        filters: List[str] = None,
    ) -> List[IngredientModel]:

        query = IngredientOrm.table().select().limit(limit).offset(offset)

        if sort_params:
            query = self._add_sorting(query, sort_params, IngredientOrm.table())

        if filters:
            query = self._add_filters(query, filters, IngredientOrm.table())

        ingredients = await self.db.fetch_all(query)

        return [IngredientModel(**ingredient) for ingredient in ingredients]

    async def get_one_ingredient(self, id: str) -> Optional[IngredientModel]:
        query = IngredientOrm.table().select().where(IngredientOrm.table().c.id == id)
        ingredient = await self.db.fetch_one(query)

        if ingredient is None:
            return None

        return IngredientModel(**ingredient)

    async def get_ingredients_for_recipe(self, id: str) -> List[IngredientForRecipe]:
        ingredients_table = IngredientOrm.table()

        join = ingredients_table.join(
            recipes_ingredients,
            (ingredients_table.c.id == recipes_ingredients.c.ingredient_id)
            & (recipes_ingredients.c.recipe_id == id),
            isouter=False,
        )

        query = select([ingredients_table.c.id, ingredients_table.c.name]).select_from(
            join
        )

        ingredients = await self.db.fetch_all(query)

        return [IngredientForRecipe(**ingredient) for ingredient in ingredients]

    async def update_ingredient(
        self, id: str, updated_ingredient: UpdatedIngredientModel
    ) -> Optional[IngredientModel]:
        ingredient: Optional[IngredientModel] = await self.get_one_ingredient(id)

        if ingredient is None:
            return None

        values = {
            ingredient_key: ingredient_val
            for ingredient_key, ingredient_val in updated_ingredient.dict().items()
            if ingredient_val is not None
        }

        sql = (
            IngredientOrm.table()
            .update()
            .where(IngredientOrm.table().c.id == id)
            .values(**values)
        )
        await self.db.execute(sql)

        return await self.get_one_ingredient(id)

    async def delete_ingredient(self, id: str) -> Optional[IngredientModel]:
        ingredient: Optional[IngredientModel] = await self.get_one_ingredient(id)

        if ingredient == None:
            return None

        sql = IngredientOrm.table().delete().where(IngredientOrm.table().c.id == id)
        await self.db.execute(sql)

        return ingredient
