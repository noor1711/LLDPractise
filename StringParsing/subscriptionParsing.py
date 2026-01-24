# we have a time line  -------********-------
# we can keep a list of events and then run a binary search over them
# we will have to keep the events in chronological order though
DEFAULT_GRACE_PERIOD = 5
CONFIG = {
    "BASIC": 5,
    "PREMIUM": 10,
    "API": 0  # No grace period for API access
}
def build_subscription_timeline(events):
    return sorted(events, key=lambda x: x["timestamp"])

def get_latest_event(events, current_time):
    start = 0
    end = len(events) - 1
    ans = None
    while start <= end:
        mid = (start + end) // 2
        mid_time = events[mid]["timestamp"]
        if mid_time == current_time:
            ans = mid
            break
        elif current_time < mid_time:
            end = mid - 1
        elif current_time > mid_time:
            ans = mid
            start = mid + 1
    
    return None if ans is None else events[ans]

def check_is_within_grace_period(time, currentTime, product_id):
    grace = CONFIG[product_id] if product_id in CONFIG else DEFAULT_GRACE_PERIOD
    return currentTime - time < grace
    

def check_is_access_valid(event, current_time, product_id):

    if event["event"] == "START":
        return True

    # else check for grace period logic
    last_time = event["timestamp"]
    return check_is_within_grace_period(last_time, current_time, product_id)

def has_access(events, current_time, product_id="API"):
    sorted_events = build_subscription_timeline(events)
    latest_event = get_latest_event(sorted_events, current_time)
    if latest_event is None:
        return False
    return check_is_access_valid(latest_event, current_time, product_id)


events = [
    {"event": "START", "timestamp": 100},
    {"event": "END", "timestamp": 200},
    {"event": "START", "timestamp": 50}, 
    {"event": "END", "timestamp": 51}, 
]

print(has_access(events, 75))  #-> True  (Started at 50, hasn't ended yet)
print(has_access(events, 150)) #-> True  (Started again at 100)
print(has_access(events, 205, "BASIC")) #-> True  (Started again at 100)
print(has_access(events, 206, "BASIC")) #-> False  (Started again at 100)
print(has_access(events, 206, "PREMIUM")) #-> True  (Started again at 100)
print(has_access(events, 250)) #-> False (Ended at 200)