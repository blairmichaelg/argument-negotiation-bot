import os
from cachetools import cached, TTLCache
import aiohttp
from modal import Secret

# Adzuna API credentials from Modal secrets
ADZUNA_API_ID = os.environ.get("ADZUNA_API_ID", Secret.from_name("ADZUNA_API_ID"))
ADZUNA_API_KEY = os.environ.get("ADZUNA_API_KEY", Secret.from_name("ADZUNA_API_KEY"))

# Cache for API responses
cache = TTLCache(maxsize=100, ttl=300)


@cached(cache)
async def fetch_salary_data(job_title: str, location: str) -> dict:
    """
    Fetches salary data from the Adzuna API.

    Parameters:
        job_title (str): The job title for which to fetch salary data.
        location (str): The location where the job is based.

    Returns:
        dict: A dictionary containing the average salary and currency, or an error message.

    Raises:
        RuntimeError: If the API request fails.
        ValueError: If the API response is invalid or no salary data is found.
    """
    base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"  # US endpoint

    params = {
        "app_id": ADZUNA_API_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": 10,  # Get up to 10 results for averaging
        "what": job_title,
        "where": location,
        "content-type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                salaries = [
                    result["salary_is_predicted"]
                    for result in data["results"]
                    if result.get("salary_is_predicted") is not None
                ]

                if salaries:
                    average_salary = sum(salaries) / len(salaries)
                    return {
                        "average_salary": int(average_salary),  # Return as an integer
                        "currency": (
                            data["results"][0].get("currency")
                            if data["results"]
                            else "USD"
                        ),  # Default to USD
                    }
                else:
                    raise ValueError("No salary data found for this job and location.")
            elif response.status == 400:
                raise ValueError("Invalid request parameters.")
            elif response.status == 401:
                raise ValueError("Invalid API credentials.")
            elif response.status == 429:
                raise ValueError("Too many requests.")
            else:
                raise RuntimeError(
                    f"Adzuna API request failed: {response.status}, {response.text}"
                )
