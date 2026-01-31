import requests
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from dotenv import load_dotenv
import os

load_dotenv()
KEY=os.getenv("KEY")

class WeatherServiceError(Exception):
    """Custom exception for weather-related failures"""
    pass

class WeatherClient:
    def __init__(self, api_key, base_url= "https://api.weatherapi.com/v1/current.json"):
        self.api_key = api_key
        self.base_url = base_url
        self.retry_strategy = Retry(total=3, status_forcelist=[429, 500])
        self.weather_adapter = HTTPAdapter(max_retries=self.retry_strategy)

    def get_surge_amount(self, city):
        with requests.session() as session:
            session.mount(self.base_url, self.weather_adapter)
            try:
                response = session.get(self.base_url, params={"key": self.api_key, "q": city}, timeout=2)
                response.raise_for_status()
                response = response.json()
                if response.get("current").get("condition").get("text").lower() in ["rain", "snow"]:
                    return 200
                return 0
            except Exception as e:
                print(e)
                raise WeatherServiceError(e)
            except RetryError as e:
                print(f"Retry error {e}")
                raise e;

def calculate_delivery_fee(city):
    base_fee = 500
    client = WeatherClient(api_key=KEY)

    try:
        amount = client.get_surge_amount(city)
        return base_fee + amount
    except WeatherServiceError as e:
        print(e)
        return base_fee
    
print(calculate_delivery_fee(city="London"))
print(calculate_delivery_fee(city="toronto"))
