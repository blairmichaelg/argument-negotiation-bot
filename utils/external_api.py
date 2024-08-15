import os
import requests

ADZUNA_API_ID = "9f61316b" 
ADZUNA_API_KEY = "2a2e81490507553905b7dbe578bf0912"

def fetch_salary_data(job_title: str, location: str) -> dict:
    """Fetches salary data from the Adzuna API."""

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
                "currency": data["results"][0].get("currency")
                if data["results"]
                else "USD",  # Default to USD
            }
        else:
            return {"error": "No salary data found for this job and location."}
    else:
        raise RuntimeError(
            f"Adzuna API request failed: {response.status_code}, {response.text}"
        )