from sqlalchemy.orm import Session
import logging
import exceptions
from database.models import Cash
from database.crud import get_bill_by_val, get_inventory, add_funds
import main
from database.database import get_db

logger = logging.getLogger(__name__)


db = next(get_db())


allowed_bills = {200, 100, 20, 10, 5, 1, 0.1, 0.01}

curr_type = {
    200: "B",
    100: "B",
    20: "B",
    10: "C",
    5: "C",
    1: "C",
    0.1: "C",
    0.01: "C"
}


def verify_in_stock(val, amount):
    bill = get_bill_by_val(val=val)
    if bill is not None:
        return amount < bill.amount
    return False


def validate_refill_data(refill_data):
    for bill in refill_data["money"]:
        if float(bill) not in allowed_bills:
            raise exceptions.IlleagalMoneyException
    return "Refill complete"


def refill(refill_data):
    validate_refill_data(refill_data)
    incoming_cash = refill_data["money"]
    for curr_val in incoming_cash.keys():
        amount = incoming_cash[curr_val]
        # if float(curr_val) in allowed_bills:
        fix_inventory(float(curr_val), amount)


def withdrawal(amount: float):
    validate_withdrawal(amount)
    coin_count = 0
    remaining_amount = amount
    result = {}
    update_data = {}

    inventory = get_inventory(db)
    for item in inventory:
        bill_val = item.val
        current_currency_ammout = get_max_curr(
            amount=remaining_amount, val=bill_val)
        if current_currency_ammout > 0:
            if curr_type[bill_val] == "C":
                if current_currency_ammout > 50 or current_currency_ammout + coin_count > 50:
                    raise exceptions.MaxCoinsExceededException
                else:
                    coin_count += current_currency_ammout

            remaining_amount = format_float(
                remaining_amount - (current_currency_ammout*bill_val))
            update_data[bill_val] = -current_currency_ammout

            result = edit_results(
                curr_id=bill_val, amount=current_currency_ammout, results=result)
        if remaining_amount < 0.01:
            break

    if remaining_amount > 0:
        raise exceptions.OutOfCashException()
    if coin_count > 50:
        raise exceptions.MaxCoinsExceededException()
    for bill_val in update_data:
        fix_inventory(bill_val, update_data[bill_val])
    return {"result": result}


def validate_withdrawal(amount):
    if amount > 2000:
        raise exceptions.MaxAmountException(amount)
    if amount <= 0:
        raise Exception("too little")


def get_max_curr(amount: int, val: float):
    # db = main.db
    curr = get_bill_by_val(db, val=val)
    curr_amount = curr.amount

    if val > amount:
        return 0

    return_count = int(amount/val)
    if return_count <= curr_amount:
        return return_count
    else:
        return curr_amount


def fix_inventory(curr_id: float, amount: int):
    try:

        curr = get_bill_by_val(db, curr_id)
        if curr_id > 10:
            bill_type = "B"
        else:
            bill_type = "c"
        if curr is None:
            cash = Cash(val=curr_id, type=bill_type, amount=amount)
            add_funds(cash=cash)
        else:
            curr.amount = curr.amount + amount
            db.commit()
    except Exception as e:
        logger.error(e)
        raise e


def edit_results(curr_id: int, amount, results: dict):
    if curr_type[curr_id] == "B":
        if "bills" not in results:
            results["bills"] = {}
        results["bills"][curr_id] = amount
    else:
        if "coins" not in results:
            results["coins"] = {}
        results["coins"][curr_id] = amount

    return results


def format_float(val):
    return float("{:.2f}".format(val))
