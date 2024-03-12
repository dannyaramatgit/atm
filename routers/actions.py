import logging
from fastapi import APIRouter, status, HTTPException
import exceptions
from com_models import response_models
import backend.atm as atm
from com_models import request_models
from database.database import init_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/atm")


def validate_amount(amount):
    amount_str = str(amount)
    if '.' in amount_str:
        dec_index = amount_str.index('.')
        if len(amount_str)-1-dec_index > 2:
            raise ValueError('must be 2 decimal places or less')


@router.get("/withdrawal/", response_model=response_models.Withdrawal, status_code=status.HTTP_200_OK)
def withdrawal(amount: float):
    try:
        validate_amount(amount)
        return atm.withdrawal(amount=amount)
    except exceptions.MaxAmountException as e:
        logger.error(e)
        raise HTTPException(status_code=422)
    except exceptions.OutOfCashException as ce:
        logger.error(ce)
        raise HTTPException(status_code=409)
    except exceptions.MaxCoinsExceededException as mce:
        logger.error(mce)
        raise HTTPException(status_code=422)
    except ValueError as ve:
        logger.error(ve)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@router.post("/refill", status_code=status.HTTP_200_OK)
def refill(refill: request_models.Refill):
    try:
        return atm.refill(refill_data=refill.dict())
    except exceptions.IlleagalMoneyException as e:
        logger.error(e)
        raise HTTPException(status_code=422)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@router.get("/init", status_code=status.HTTP_200_OK)
def init():
    try:
        return init_db()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)
