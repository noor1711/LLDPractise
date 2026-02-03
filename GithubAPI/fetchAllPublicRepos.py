import asyncio
import aiohttp
import random

sema = asyncio.BoundedSemaphore(5)
async def get_page(session, page_no):
    """Worker function to fetch a single page."""
    url = f"https://api.github.com/orgs/stripe/repos?per_page=10&page={page_no}"
    
    # Introduce jitter to avoid 'thundering herd' on the API
    await asyncio.sleep(random.uniform(0.5, 1.5)) 
    
    try:
        async with sema, session.get(url, timeout=10) as response:
            if response.status == 403:
                print(f"Rate limited on page {page_no}")
                return []
            
            response.raise_for_status()
            # In aiohttp, .json() MUST be awaited
            data = await response.json()
            return [repo.get("description") for repo in data]
    except Exception as e:
        print(f"Error on page {page_no}: {e}")
        return []

async def fetch_all_repos(limit=5):
    # Use ONE session for the entire lifecycle
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks (we want pages 1 through limit)
        tasks = [get_page(session, page) for page in range(1, limit + 1)]
        
        # Run them all concurrently
        pages_data = await asyncio.gather(*tasks)
        
        # Flatten the list of lists
        all_repos = [desc for page in pages_data for desc in page]
        
    return {"repos": all_repos, "count": len(all_repos)}, 200

# To run the async function:
if __name__ == "__main__":
    from pprint import pprint
    result = asyncio.run(fetch_all_repos(limit=3))
    pprint(result)