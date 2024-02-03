import httpx
import enum
import collections

class Tip(enum.Enum):
    ABSENT = 0  # word not in secret word
    PRESENT = 1  # word in secret word but wrong position
    CORRECT = 2  # word in secret word and correct position

async def fetch_random_word():
    # Specify the URL and parameters
    url = "https://wordle.votee.dev:8000/random"
    params = {
        "guess": "hello",  # Replace with your actual guess
        "size": 5,  # You can adjust the size parameter if needed
        "seed": 123  # You can provide a specific seed if needed
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            # Directly use Tip enum values in the list
            tip_feedback = [Tip.CORRECT if item['result'].upper() == 'CORRECT' else
                            Tip.PRESENT if item['result'].upper() == 'PRESENT' else
                            Tip.ABSENT for item in data]

            print("Result:", tip_feedback)
            return tip_feedback
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

# Run the asynchronous function
import asyncio
asyncio.run(fetch_random_word())
