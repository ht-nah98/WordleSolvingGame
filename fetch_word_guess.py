import httpx

async def fetch_word_guess(word, guess):
    # Specify the URL and parameters
    url = f"https://wordle.votee.dev:8000/word/{word}"
    params = {
        "guess": guess  
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
asyncio.run(fetch_word_guess("bling", "clear"))
