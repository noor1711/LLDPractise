# Pricing Model
# private and python
# flat fee - $10

# starting_url and cursor -> next_url

# implement retry-after logic - sleep for a certain duration - then retry
# max_retires should also be implemented

"""
{
    "total_cost_cents": 2000,      # (e.g., 2 repos found @ 1000 cents each)
    "repos_scanned": ["repo1", "repo2"],
    "next_cursor": "https://...",  # URL for the next page, or None if finished
    "status": "COMPLETED"          # or "INTERRUPTED" if an error occurred
}
"""

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class GITHUB_ERROR(Exception):
    """
    Docstring for GITHUB_ERROR
    """
    pass

import random
import math
# Github Client
class Github_Client:
    def __init__(self, API_KEY):
        self._key = API_KEY
        self.base_url = "https://api.github.com"
        random.seed(123)
    
    def get_languages(self, owner, repo):
        num = math.floor(random.random() * 2)
        return [{"Python": 200, "Rust": 300}, {"Ruby": 8900, "Js": 400}][num]

    def get_repos(self, org="amazon"):
        URL = f"/orgs/{org}/repos"
        with requests.session() as session:
            try:
                response = [
                {
                    "id": 101,
                    "name": "payments-core",
                    "private": True,
                    "owner": {"login": "stripe"},
                    "languages_url": "https://api.github.com/repos/stripe/payments-core/languages"
                },
                {
                    "id": 102,
                    "name": "public-docs-site",
                    "private": False,
                    "owner": {"login": "stripe"},
                    "languages_url": "https://api.github.com/repos/stripe/public-docs-site/languages"
                }
]
                return response
            except Exception as e:
                print(e)

import os
from dotenv import load_dotenv

load_dotenv()

client = Github_Client(os.getenv("GITHUB_API_KEY"));
client.get_repos("amazon")
