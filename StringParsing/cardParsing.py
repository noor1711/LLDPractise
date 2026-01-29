import re
CONFIG = {
    "VISA": lambda x: len(x) == 16 and x.startswith("4"),
    "MASTERCARD": lambda x: len(x) == 16 and re.match(r'5[1-5]', x),
    "AMEX": lambda x: len(x) == 15 and x.startswith(("34", "37")),
    "DISCOVER": lambda x: len(x) == 16 and x.startswith(("6011", "65")),
    "DINERS_CLUB": lambda x: len(x) == 14 and re.match(r'30[0-5]', x)
}

"""
    Remove unwanted characters from card data
"""
def clean_card_data(card_number):
    return "".join(filter(str.isdigit, card_number))

"""
    Mask card data since its PI 
"""
def mask_card_data(card_number):
    total_len = len(card_number)
    if total_len > 5:
        masked_len = total_len - 5
        return card_number[:1] + "*" * masked_len + card_number[-4:]
    elif total_len <= 2:
        return card_number
    else:
        masked_len = total_len - 2
        return card_number[:1] + "*" * masked_len + card_number[-1:]

def preprocess_card_data(card_number):
    return mask_card_data(clean_card_data(card_number))

def get_card_brand(card_number):
    print(card_number)
    for type, type_filter in CONFIG.items():
        if type_filter(card_number):
            return type
    return "UNKNOWN"

print(preprocess_card_data("4111-2222-3333-4444"))
print(preprocess_card_data("4-4444"))
print(preprocess_card_data("4-4"))
print(preprocess_card_data("---"))
print(get_card_brand(clean_card_data("4111-2222-3333-4444")))
print(get_card_brand(clean_card_data("341-2222-3333-4444")))
print(get_card_brand(clean_card_data("5151-2222-3333-4444")))
print(get_card_brand(clean_card_data("5951-2222-3333-4444")))
print(get_card_brand(clean_card_data("6011-2222-3333-4444")))
print(get_card_brand(clean_card_data("6511-2222-3333-4444")))
print(get_card_brand(clean_card_data("302-222-3333-4444")))