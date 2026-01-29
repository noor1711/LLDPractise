from functools import reduce
import math

GRACE_PERIOD = 20
def is_valid_transaction(transaction, closing_time):
    created_at = transaction.get("created_at",  -1)
    status = transaction.get("status", "FAILED")
    settlement_deadline = closing_time + GRACE_PERIOD
    settled_at = transaction.get("settled_at", math.inf) if transaction.get("settled_at", math.inf) is not None else math.inf
    return created_at <= closing_time and status == "SUCCESS" and settled_at <= settlement_deadline

def get_total_amount(transactions):
    return reduce(lambda accum, current: accum + current.get("amount", 0), transactions, 0)

def get_closed_total(transactions, closing_time):
    return get_total_amount(filter(lambda transaction: is_valid_transaction(transaction, closing_time), transactions))

def is_pending(transaction, closing_time, current_time):
    created_at = transaction.get("created_at", 0)
    status = transaction.get("status", "PENDING")
    return created_at <= closing_time and status == "PENDING" and current_time < closing_time + GRACE_PERIOD

def is_ready_to_close(transactions, closing_time, current_time):
    return any(map(lambda x: is_pending(x, closing_time, current_time), transactions))

transactions = [
    {"id": "t1", "amount": 100, "created_at": 10, "settled_at": 20, "status": "SUCCESS"},
    {"id": "t2", "amount": 200, "created_at": 50, "settled_at": 90,"status": "PENDING"},
    {"id": "t3", "amount": 300, "created_at": 61, "settled_at": 70,"status": "FAILED"},
]
closing_time = 50
print(get_closed_total(transactions, closing_time))
print(get_closed_total(transactions, 0))
print(is_ready_to_close(transactions, 60, 65))
# Result: 300 (100 + 200)