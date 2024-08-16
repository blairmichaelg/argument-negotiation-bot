import os
import requests
from cachetools import cached, TTLCache

# Adzuna API credentials from environment variables
ADZUNA_API_ID = os.getenv("ADZUNA_API_ID", "your_default_id")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY", "your_default_key")

# Cache for API responses
cache = TTLCache(maxsize=100, ttl=300)


@cached(cache)
def fetch_salary_data(job_title: str, location: str) -> dict:
    """
    Fetches salary data from the Adzuna API.

    Parameters:
        job_title (str): The job title for which to fetch salary data.
        location (str): The location where the job is based.

    Returns:
        dict: A dictionary containing the average salary and currency, or an error message.

    Raises:
        RuntimeError: If the API request fails.
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

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
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
                    data["results"][0].get("currency") if data["results"] else "USD"
                ),  # Default to USD
            }
        else:
            return {"error": "No salary data found for this job and location."}
    else:
        raise RuntimeError(
            f"Adzuna API request failed: {response.status_code}, {response.text}"
        )
