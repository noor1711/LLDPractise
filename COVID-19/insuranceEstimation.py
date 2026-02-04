import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import RetryError
class PricingService:
    def __init__(self):
        self.base_fee = 2000
        self.risk_fee = 1500
        self.hazard_fee = 1000

    def get_price(self, risk_level):
        fee = self.base_fee

        if risk_level >= 3:
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
        self.session = requests.session()
        self.session.mount("https://api.risk-level.io/v1/countries/", self.adapter)
        self.country_cache = {}

    def get_risk(self, country_code):
        if country_code in self.country_cache:
            return self.country_cache.get(country_code)
        try:
            # response = self.session.get(f"https://api.risk-level.io/v1/countries/{country_code}")
            # response = response.json()
            response = {
                "country": "IN",
                "risk_level": 4,
                "updated_at": "2026-02-01T23:00:00Z"
            }
            print("Risk Service", response.get("risk_level", 1) )
            self.country_cache[country_code] = {"risk": response.get("risk_level", 1), "status": "SUCCESS"}
            return self.country_cache[country_code]
        except RetryError as e:
            print("Unable to retry", e)
            return {"risk": self.base_risk, "status": "FAILURE", "error": e}
            
class PremiumManager:
    def __init__(self):
        self.risk_service = RiskService()
        self.pricing_service = PricingService()
        self.application_url = "https://api.safepass.com/v1/applications?page=1"
        self.idempotency_store = {}

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

    def process_single_application(self, application, idempotency_key):
        """
        Requirements:
        1. Check if idempotency_key exists in self.idempotency_store.
        2. If it exists:
           - Verify the application ID matches the one stored.
           - If matches, return stored response.
           - If mismatch, raise an Exception ("Key conflict").
        3. If it doesn't exist:
           - Call RiskService and PricingService.
           - Store result + application ID.
           - Return result.
        """
        if idempotency_key in self.idempotency_store:
            if application.get("id") == self.idempotency_store.get("idempotency_key").get("app_id"):
                return self.idempotency_store.get("idempotency_key").get("pricing")
            else:
                raise Exception("Key conflict")
        
        risk_response = self.risk_service.get_risk(application.get("destination"))
        pricing = self.pricing_service.get_price(risk_response.get("risk"))

        self.idempotency_store[idempotency_key] = {"pricing": pricing, "app_id": application.get("id")}
        return pricing

    def calculate_fee(self):
        # lets get all the applications first
        applications = self.get_applications()
        response = {
            "total_premium_cents": 0,
            "success_ids": [],
            "failed_ids": [],
            "errors": [],
        }
        
        try:
            for application in applications:
                risk_response = self.risk_service.get_risk(application.get("destination"))
                print(risk_response)
                if risk_response.get("status") == "SUCCESS":
                    response.get("success_ids").append(application.get("id"))
                else:
                    response.get("failed_ids").append(application.get("id"))
                    response.get("errors").append({"app_id": application.get("id"), "reason": risk_response.get("error").get("message", "Risk Service Failure")})
                response["total_premium_cents"] += self.pricing_service.get_price(risk_response.get("risk"))
        except Exception as e:
            print(e, "here")

        return response

import hmac
import hashlib
import json

def verify_webhook(payload: str, signature: str, secret: str) -> bool:
    """
    Verifies that the webhook signature matches the payload.
    
    :param payload: The RAW string body of the request (not the parsed JSON)
    :param signature: The hex string from the 'X-SafePass-Signature' header
    :param secret: The shared secret key
    """
    # 1. Ensure the secret and payload are in bytes
    secret_bytes = secret.encode('utf-8')
    payload_bytes = payload.encode('utf-8')

    # 2. Create the HMAC-SHA256 hash
    expected_hmac = hmac.new(
        secret_bytes, 
        payload_bytes, 
        hashlib.sha256
    )
    
    # 3. Get the hex representation of our calculated hash
    calculated_signature = expected_hmac.hexdigest()

    # 4. Use a constant-time comparison to prevent timing attacks
    # This is a key "Senior/Stripe" detail!
    return hmac.compare_digest(calculated_signature, signature)

# --- TEST CASE ---
MOCK_SECRET = "whsec_12345"
MOCK_PAYLOAD = json.dumps({"id": "evt_01", "type": "application.created"})
# Normally provided in request headers
MOCK_SIGNATURE = hmac.new(
    MOCK_SECRET.encode(), 
    MOCK_PAYLOAD.encode(), 
    hashlib.sha256
).hexdigest()

is_valid = verify_webhook(MOCK_PAYLOAD, MOCK_SIGNATURE, MOCK_SECRET)
print(f"Is Webhook Valid? {is_valid}")


manager = PremiumManager()
print(manager.calculate_fee())