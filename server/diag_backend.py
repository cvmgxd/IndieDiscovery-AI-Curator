import httpx
import asyncio

async def test_discover():
    async with httpx.AsyncClient() as client:
        try:
            print("Fetching http://localhost:8001/discover ...")
            resp = await client.get("http://localhost:8001/discover", timeout=30.0)
            print(f"Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"Error: {resp.text}")
            else:
                print(f"Success! Found {len(resp.json())} games.")
        except Exception as e:
            print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_discover())
