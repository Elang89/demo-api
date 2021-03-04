from typing import Dict, List, Optional

from app.db.repositories.base import BaseRepository
from app.models.ingredient import IngredientModel, IngredientOrm, UpdatedIngredientModel


class IngredientRepository(BaseRepository):
    async def create_ingredient(self, ingredient: IngredientModel) -> IngredientModel:
        raise NotImplementedError()

    async def get_ingredients(
        self,
        limit: int,
        offset: int,
        sort_params: Dict[str, str] = None,
        filters: List[str] = None,
    ) -> List[IngredientModel]:
        raise NotImplementedError()

    async def get_one_recipe(self, id: str) -> Optional[IngredientModel]:
        raise NotImplementedError()

    async def update_recipe(
        self, id: str, updated_ingredient: UpdatedIngredientModel
    ) -> Optional[IngredientModel]:
        raise NotImplementedError()

    async def delete_recipe(self, id: str) -> Optional[IngredientModel]:
        raise NotImplementedError()
