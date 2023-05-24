# system imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Boolean, DateTime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import Column
from typing import Any, Dict
import pprint

# instantiate base
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False, nullable=False)
    created_date = Column(
        DateTime, default=current_timestamp(), nullable=False
    )

    @classmethod
    def get_kind(cls) -> str:
        return cls.__name__

    @property
    def dict(self) -> Dict:
        result = {}
        for col in self.__table__.columns:
            name = getattr(self, col.name)
            result[col.name] = str(name) if name is not None else None
        return result

    def __eq__(self, other_object: object) -> Any:
        return True if (
            isinstance(other_object, self.__class__)
            and self.id == other_object.id
        ) else False

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return f'self.__tablename__{pprint.pformat(self.dict)}'
