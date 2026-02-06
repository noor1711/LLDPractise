import time
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_KEY = os.getenv("GITHUB_API_KEY")

class Github_Client:
    def __init__(self, API_KEY):
        self._key = API_KEY
        self.url = "https://api.github.com"
        # We define the placeholder, but don't initialize the loop-bound object here
        self.semaphore = None

    async def fetch_page(self, org, page_no, session):
        target_url = f"{self.url}/orgs/{org}/repos"
        
        start = time.perf_counter()
        
        # Guard: Use the semaphore to limit concurrency
        async with self.semaphore:
            async with session.get(
                url=target_url, 
                params={"per_page": 10, "page": page_no}
            ) as response:
                data = await response.json() 
                print(f"Page {page_no} | Status: {response.status} | Time: {time.perf_counter() - start:.4f}s")
                return data
        
    async def fetch_all_pages(self):
        # INITIALIZE PRIMITIVES HERE:
        # Now we are inside the loop created by asyncio.run()
        if self.semaphore is None:
            self.semaphore = asyncio.BoundedSemaphore(2)

        headers = {
            "Authorization": f"Bearer {self._key}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [self.fetch_page("stripe", page, session) for page in range(1, 5)]
            responses = await asyncio.gather(*tasks)
            return responses

if __name__ == "__main__":
    client = Github_Client(GITHUB_KEY)
    
    try:
        # This creates the main event loop
        results = asyncio.run(client.fetch_all_pages())
        print(f"Retrieved {len(results)} pages of data.")
    except Exception as e:
        # This will now give you a full traceback if it fails
        import traceback
        traceback.print_exc()