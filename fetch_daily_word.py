import httpx
async def fetch_daily_word():
    # Specify the URL and parameters
    url = "https://wordle.votee.dev:8000/daily"
    params = {
        "guess": "under",  # Replace with your actual guess
        "size": 5  # You can adjust the size parameter if needed
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            print("Received data:", data)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

# Run the asynchronous function
import asyncio
asyncio.run(fetch_daily_word())