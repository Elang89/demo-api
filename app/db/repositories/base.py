from typing import Dict, List

from databases import Database
from sqlalchemy import Table  # type: ignore
from sqlalchemy import text
from sqlalchemy.orm import Query  # type: ignore


class BaseRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    @property
    def db(self) -> Database:
        return self._db

    def _add_sorting(
        self,
        query: Query,
        sort_params: Dict[str, str],
        table: Table,
    ) -> Query:
        for sort_key, sort_value in sort_params.items():
            if sort_value == "asc":
                query = query.order_by(table.c[sort_key].asc())
            elif sort_value == "desc":
                query = query.order_by(table.c[sort_key].desc())

        return query

    def _add_filters(self, query: Query, filters: List[str], table: Table) -> Query:

        for filter_param in filters:
            query = query.where(text(filter_param))

        return query
