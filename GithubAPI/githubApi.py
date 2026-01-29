import requests
from pprint import pprint
from requests.auth import AuthBase
from datetime import date, timedelta, datetime
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_KEY=os.getenv("GITHUB_API_KEY")
class TokenAuth(AuthBase):
    def __init__(self, token):
        self._token = token
    
    def __call__(self, request: requests.Request):
        request.headers["Authorization"] = f'Bearer {self._token}'
        return request

response = requests.get("https://api.github.com/events", params={"per_page": 10, "page": 1})
response.raise_for_status()

# lets extract all the public libs

def get_public_libs(repos):
    return list(filter(lambda x: x["public"], repos))

def get_last_3month_created(repos):
    three_month_old_date = datetime.date(datetime.now() - timedelta(days=90))
    return list(filter(lambda x: datetime.date(datetime.fromisoformat(x["created_at"].replace("Z", "+00:00"))) > three_month_old_date, repos))

pprint(len(get_last_3month_created(response.json())))

# getting the issues
res = requests.post("https://api.github.com/repos/noor1711/LLDPractise/issues", headers={"Accept": "application/vnd.github+json"}, auth=TokenAuth(GITHUB_KEY), json={"title": "blah, blah", "description": "integrating apis is kinda shitty ngl"})
pprint(res.text)

res = requests.get("https://api.github.com/users/noor1711/repos", headers={"Accept": "application/vnd.github+json"}, auth=TokenAuth(GITHUB_KEY))
pprint(res.text)