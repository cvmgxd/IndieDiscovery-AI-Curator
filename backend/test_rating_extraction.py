import httpx
import re
import asyncio

async def get_rating_count(url):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                return None
            
            # Look for schema.org ratingCount
            match = re.search(r'itemprop="ratingCount" content="(\d+)"', resp.text)
            if match:
                return int(match.group(1))
            
            # Fallback to (X ratings)
            match = re.search(r'\((\d+)\s+ratings\)', resp.text)
            if match:
                return int(match.group(1))
                
            return 0
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

async def main():
    test_urls = [
        "https://adamgryu.itch.io/a-short-hike",
        "https://strayfawnstudio.itch.io/the-wandering-village"
    ]
    for url in test_urls:
        count = await get_rating_count(url)
        print(f"{url}: {count} ratings")

if __name__ == "__main__":
    asyncio.run(main())
