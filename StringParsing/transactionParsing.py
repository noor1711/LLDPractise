# "merchant_id,transaction_id,amount_in_cents,currency,status"
from functools import reduce
import math
MERCHANT_ID = "merchant_id"
TRANSACTION_ID = "transaction_id"
AMOUNT_IN_CENTS = "amount_in_cents"
CURRENCY = "currency"
STATUS = "status"

def calculate_fee():
    merchant_configs = {
        "m001": {"percent": 0.02, "flat": 10},  # m001 gets a better deal
        "m002": {"percent": 0.01, "flat": 5},    # m002 gets a great deal
        "default": {"percent": 0.29, "flat": 30}
    }

    def calulate_fee_for_merchant(amount, merchant_id):
        config = merchant_configs[merchant_id] if merchant_id in merchant_configs else merchant_configs["default"]
        flat = config["flat"]
        percent = config["percent"]
        return math.floor(amount * percent + flat)
    
    return calulate_fee_for_merchant

def calculate_total_success(transactions, merchant_id, currency, status="SUCCESS"):
    calculate_fee_func = calculate_fee()

    def map_to_dic(transaction):
        # ensure that transaction is valid
        arr = transaction.split(",")
        if len(arr) != 5:
            print("transaction is not valid")
            return {}
        
        dic = {}
        dic[MERCHANT_ID] = arr[0]
        dic[TRANSACTION_ID] = arr[1] # dont need this 
        dic[AMOUNT_IN_CENTS] = int(arr[2])
        dic[CURRENCY] = arr[3]
        dic[STATUS] = arr[4]
        return dic
    

    def filter_by_attributes(transaction):
        return transaction[MERCHANT_ID] == merchant_id and transaction[CURRENCY] == currency and transaction[STATUS] == status

    def calculate_final_amount(transaction):
        amount = transaction[AMOUNT_IN_CENTS]
        return max(0, amount - calculate_fee_func(amount, merchant_id))

    def sum_of_cents(accum, curr):
        return accum + curr
    
    def group_by_transaction_id(transactions):
        transaction_id_dic = {}

        for transaction in transactions:
            t_id = transaction[TRANSACTION_ID]
            status = transaction[STATUS]
            if t_id in transaction_id_dic:
                if status == "REFUND":
                    transaction_id_dic[t_id] = transaction
            else:
                transaction_id_dic[t_id] = transaction
                    
        return list(transaction_id_dic.values())
        
    parsed_transactions = filter(lambda x: len(x) > 0, map(map_to_dic, transactions))
    grouped_transactions = group_by_transaction_id(list(parsed_transactions))
    filtered_transactions = filter(filter_by_attributes, grouped_transactions)
    final_amounts = map(calculate_final_amount, filtered_transactions)
    amount = reduce(sum_of_cents, final_amounts, 0)
    return amount
    

transactions = [
    "m001,t01,1000,USD,SUCCESS", # This is good
    "m001,t02,2000,USD,SUCCESS", # This was later refunded!
    "m001,t02,2000,USD,REFUND",  # Refund for t02
    "m001,t03,500,USD,SUCCESS",  # This is good
]

print(calculate_total_success(transactions, "m001", "USD") )