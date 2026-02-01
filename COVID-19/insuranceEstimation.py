import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import RetryError
from functools import reduce

class PricingService:
    def __init__(self):
        self.base_fee = 2000
        self.risk_fee = 1500
        self.hazard_fee = 1000

    def get_price(self, risk_level):
        fee = self.base_fee

        if risk_level > 3:
            fee += self.risk_fee
        
        if risk_level == 5:
            fee += self.hazard_fee

        print("Pricing Service", risk_level, fee)
        return fee

# input - trip applications[] -  country code - risk assessment API


class RiskService:
    def __init__(self):
        self.retry_strategy = Retry(total=3, status_forcelist=[500, 503], backoff_factor=2, backoff_max=1.5)
        self.adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.base_risk = 1

    def get_risk(self, country_code):
        with requests.session() as session:
            session.mount("https://api.risk-level.io/v1/countries/", self.adapter)
            try:
                # response = session.get(f"https://api.risk-level.io/v1/countries/{country_code}")
                # response = response.json()
                response = {
                    "country": "IN",
                    "risk_level": 4,
                    "updated_at": "2026-02-01T23:00:00Z"
                }
                print("Risk Service", response.get("risk_level", 1) )
                return response.get("risk_level", 1)
            except RetryError as e:
                print("Unable to retry", e)
                return self.base_risk
            
class PremiumManager:
    def __init__(self):
        self.risk_service = RiskService()
        self.pricing_service = PricingService()
        self.application_url = "https://api.safepass.com/v1/applications?page=1"

    def get_applications(self, limit=10):
        base_url = self.application_url
        response = []
        while base_url and len(response) < limit:
            # current_response = requests.get(base_url)
            current_response = {
                "data": [
                    {"id": "app_01", "name": "Alice", "destination": "IN"},
                    {"id": "app_02", "name": "Bob", "destination": "US"}
                ],
                "next_page": "https://api.safepass.com/v1/applications?page=2"
                }
            base_url = current_response.get("next_page")
            response.extend(current_response.get("data", []))

        response = response[:limit]
        return response
    
    def calculate_fee(self):
        # lets get all the applications first
        applications = self.get_applications()

        risks = map(lambda application: self.risk_service.get_risk(application.get("destination")), applications)
        return reduce(lambda accum, curr: accum + self.pricing_service.get_price(curr),risks, 0)
    

manager = PremiumManager()
print(manager.calculate_fee())