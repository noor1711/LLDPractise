import hmac
import hashlib
import time
import requests
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError

class AlertDispatcher:
    def __init__(self, webhook_secret, sms_api_key):
        self.secret = webhook_secret
        self.__api_key = sms_api_key
        self.processed_event_ids = set() # Simple idempotency for this session
        self.sms_session = requests.session()
        self.sms_base_url = "https://api.telesign.com/v1/sms"
        self.sms_session.mount(self.sms_base_url, HTTPAdapter(max_retries=Retry(total=2, status_forcelist=[429], backoff_factor=2, backoff_max=2)))

    def verify_signature(self, raw_payload, signature):
        # generate the hash
        hashed_payload = hmac.new(
            self.secret.encode("utf-8"),
            raw_payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(hashed_payload, signature)
        

    def send_sms(self, message):
        # Fix: Use the correct session variable name
        try:
            # Note: TeleSign likely expects JSON, not form-data
            response = self.sms_session.post(
                self.sms_base_url, 
                json={"phone": "+15550101", "message": message},
                timeout=2 # Always set a timeout!
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # If we hit a 429 that the Retry adapter didn't catch
            print(f"TeleSign Error: {e}")
            raise 

    def handle_webhook(self, raw_payload, signature):
        if not self.verify_signature(raw_payload, signature):
            return {"error": "Invalid signature"}, 401
        
        data = json.loads(raw_payload)
        event_id = data.get("id")
        
        # 1. Idempotency Check
        if event_id in self.processed_event_ids:
            return {"status": "already_processed"}, 200
        
        payment_data = data.get("data", {})
        amount = payment_data.get("amount_cents", 0)
        
        # 2. Threshold Check
        if amount < 50000:
            return {"status": "ignored", "reason": "below_threshold"}, 200
        
        # 3. Normalization
        currency = payment_data.get("currency", "usd").upper()
        email = payment_data.get("customer_email")
        message = f"Urgent: Payment of {amount} {currency} failed for {email}." 
        
        try:
            self.send_sms(message)
            # 4. State Update (Crucial!)
            self.processed_event_ids.add(event_id)
            return {"status": "alert_sent"}, 201
        except Exception as e:
            # Log the error but don't leak internals to the sender
            print(f"Alert failed: {str(e)}")
            return {"error": "Internal alert failure"}, 500