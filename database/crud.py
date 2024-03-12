from sqlalchemy.orm import Session
from fastapi import Depends

from database.models import Cash
from database.database import get_db


def get_bill_by_val(db: Session, val: int):
    return db.query(Cash).filter(Cash.val == val).first()


def get_inventory(db: Session, limit: int = 100):
    return db.query(Cash).order_by(Cash.val.desc()).all()


def add_funds(db: Session, cash: Cash):
    try:
        db.add(cash)
        db.commit()
    except Exception as e:
        print(e)
        raise e


def update_funds(db: Session, cash: Cash):
    try:
        db.commit()
    except Exception as e:
        print(e)
        raise e
