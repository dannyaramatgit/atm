from pydantic import BaseModel


class Cash(BaseModel):
    bills = {}
    coins = {}


class Withdrawal(BaseModel):
    result: Cash
