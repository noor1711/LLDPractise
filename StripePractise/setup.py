import stripe 
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("API_KEY")

first_sub = stripe.Product.create(
    name="Clay Flower Basket Subscription",
    description="$10/Month Subscription"
)

first_sub_price = stripe.Price.create(
    product=first_sub.id, 
    unit_amount=10,
    currency="usd",
    recurring={"interval": "month"}
)


pprint(f"Product - {first_sub}")
pprint(f"Price - {first_sub_price}")