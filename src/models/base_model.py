# System imports
from typing import Any, Dict
import pprint
# Finsta imports
from ..database import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(
        db.Datetime, default=db.func.current_timestamp(), nullable=False
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
