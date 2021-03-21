from typing import Dict, List, Optional

from app.db.repositories.base import BaseRepository
from app.models.ingredient import IngredientModel, IngredientOrm, UpdatedIngredientModel


class IngredientRepository(BaseRepository):
    async def create_ingredient(self, ingredient: IngredientModel) -> IngredientModel:
        ingredients_table = IngredientOrm.table()
        sql = ingredients_table.insert().values(**ingredient.dict())

        await self.db.execute(sql)

        return ingredient

    async def get_ingredients(
        self,
        limit: int,
        offset: int,
        sort_params: Dict[str, str] = None,
        filters: List[str] = None,
    ) -> List[IngredientModel]:
        ingredients_table = IngredientOrm.table()
        query = ingredients_table.select().limit(limit).offset(offset)

        if sort_params:
            query = self._add_sorting(query, sort_params, ingredients_table)

        if filters:
            query = self._add_filters(query, filters, ingredients_table)

        ingredients = await self.db.fetch_all(query)

        return [IngredientModel(**ingredient) for ingredient in ingredients]

    async def get_one_ingredient(self, id: str) -> Optional[IngredientModel]:
        ingredients_table = IngredientOrm.table()
        query = ingredients_table.select().where(ingredients_table.c.id == id)
        ingredient = await self.db.fetch_one(query)

        if ingredient is None:
            return None

        return IngredientModel(**ingredient)

    async def update_ingredient(
        self,
        id: str,
        updated_ingredient: UpdatedIngredientModel,
    ) -> Optional[IngredientModel]:
        ingredient: Optional[IngredientModel] = await self.get_one_ingredient(id)
        ingredients_table = IngredientOrm.table()

        if ingredient is None:
            return None

        update_values = {
            ingredient_key: ingredient_val
            for ingredient_key, ingredient_val in updated_ingredient.dict().items()
            if ingredient_val is not None
        }

        sql = (
            ingredients_table.update()
            .where(ingredients_table.c.id == id)
            .values(**update_values)
        )
        await self.db.execute(sql)

        return await self.get_one_ingredient(id)

    async def delete_ingredient(self, id: str) -> Optional[IngredientModel]:
        ingredient: Optional[IngredientModel] = await self.get_one_ingredient(id)
        ingredients_table = IngredientOrm.table()

        if ingredient is None:
            return None

        sql = ingredients_table.delete().where(IngredientOrm.table().c.id == id)
        await self.db.execute(sql)

        return ingredient
