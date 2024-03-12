from typing_extensions import Annotated
from pydantic import (
    BaseModel,
    Field,
    validator
)


class Refill(BaseModel):
    money = {}
