from functools import reduce
ERROR_MESSAGE = "ERROR: Inconsistent!"
def segregate_requests(requests):
    request_id_dict = {}
    last_valid_timestamp = {}
    inconsistent_requests = []
    response = []
    for request in requests:
        request_id = request["request_id"]
        if request_id in request_id_dict:
            if request["timestamp"] - last_valid_timestamp[request_id] <= 60:
                if request["amount"] != request_id_dict[request_id]["amount"]:
                    inconsistent_requests.append(request)
            else:
                last_valid_timestamp[request_id] = request["timestamp"]
                response.append(request)
            continue
        request_id_dict[request_id] = request
        last_valid_timestamp[request_id] = request["timestamp"]
        response.append(request)

    return response, inconsistent_requests 

def sort_requests_by_time(requests):
    return sorted(requests, key=lambda x: x["timestamp"])

def get_requests_sum(requests):
    return reduce(lambda accum, curr: accum + curr["amount"], requests, 0)

def log_error_message(requests, msg):
    for request in requests:
        print(msg, request["request_id"], request["amount"])

def get_total_amount(requests):
    sorted_requests = sort_requests_by_time(requests)
    unique_requests, inconsistent_requests = segregate_requests(sorted_requests)
    log_error_message(inconsistent_requests, ERROR_MESSAGE)
    return get_requests_sum(unique_requests)

requests = [
    {"request_id": "req_1", "amount": 100, "timestamp": 10},
    {"request_id": "req_1", "amount": 100, "timestamp": 70}, # Within 60? (70-10=60) Yes. Duplicate.
    {"request_id": "req_1", "amount": 500, "timestamp": 71}, # Outside 60? (71-10=61) Yes. NEW request!
]
# Total: 100 + 500 = 600
print(get_total_amount(requests))