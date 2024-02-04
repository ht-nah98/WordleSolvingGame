import httpx

async def fetch_random_word():
    # Specify the URL and parameters
    url = "https://wordle.votee.dev:8000/random"
    params = {
        "guess": "helloa",  # Replace with your actual guess
        "size": 6,  # You can adjust the size parameter if needed
        "seed": 123  # You can provide a specific seed if needed
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
asyncio.run(fetch_random_word())
