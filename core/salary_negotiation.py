import logging
from typing import AsyncIterable

import os
import fastapi_poe as fp
import aiohttp
from cachetools import cached, TTLCache
from fastapi_poe import BotError
from modal import Secret

from utils.helpers import extract_job_details, format_salary_data
from utils.prompt_engineering import create_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                    (result.get("salary_min", 0) + result.get("salary_max", 0)) / 2
                    for result in data["results"]
                    if result.get("salary_min") is not None
                    and result.get("salary_max") is not None
                ]

                if salaries:
                    average_salary = sum(salaries) / len(salaries)
                    currency = (
                        data["results"][0].get("currency")
                        if data["results"] and "currency" in data["results"][0]
                        else "USD"
                    )
                    return {
                        "average_salary": int(average_salary),  # Return as an integer
                        "currency": currency,  # Default to USD if currency is not present
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


async def handle_salary_negotiation(
    request: fp.QueryRequest, user_input: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for salary negotiation advice.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input describing their job details.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses to the user regarding salary negotiation.
    """
    try:
        job_details = extract_job_details(user_input)
        job_title = job_details["job_title"]
        location = job_details["location"]

        if not job_title or not location:
            raise BotError(
                "Please provide both your job title and location for salary negotiation advice."
            )

        yield fp.PartialResponse(text="Fetching salary data for your job...\n\n")

        salary_data = await fetch_salary_data(job_title, location)
        formatted_salary_data = format_salary_data(salary_data)
        yield fp.PartialResponse(text=formatted_salary_data)

        # Provide additional negotiation advice
        yield fp.PartialResponse(
            text="\n\nHere are some additional tips for salary negotiation:\n\n"
        )
        request.query.append(
            fp.ProtocolMessage(
                content=create_prompt(
                    "salary_negotiation",
                    topic=f"Job title: {job_title}, Location: {location}, Average Salary: {formatted_salary_data}",
                ),
                role="user",
            )
        )
        async for msg in fp.stream_request(request, "GPT-4", request.access_key):
            yield fp.PartialResponse(text=msg.text)

        yield fp.PartialResponse(
            text="\n\nWould you like to: \n"
            "1. Explore specific negotiation strategies?\n"
            "2. Get advice on handling counter-offers?\n"
            "3. Do something else?"
        )

        # Handle user choice for further actions
        user_choice = request.query[-1].content.lower()
        if "1" in user_choice or "strategies" in user_choice:
            yield fp.PartialResponse(text="Okay, let's explore some strategies.\n\n")
            request.query.append(
                fp.ProtocolMessage(
                    content=create_prompt(
                        "salary_negotiation",
                        topic=f"Job title: {job_title}, Location: {location}, Average Salary: {formatted_salary_data}",
                    ),
                    role="user",
                )
            )
            async for msg in fp.stream_request(request, "GPT-4", request.access_key):
                yield fp.PartialResponse(text=msg.text)
        elif "2" in user_choice or "counter" in user_choice:
            yield fp.PartialResponse(
                text="Okay, here's some advice on handling counter-offers.\n\n"
            )
            request.query.append(
                fp.ProtocolMessage(
                    content=create_prompt(
                        "salary_negotiation",
                        topic=f"Job title: {job_title}, Location: {location}, Average Salary: {formatted_salary_data}",
                    ),
                    role="user",
                )
            )
            async for msg in fp.stream_request(request, "GPT-4", request.access_key):
                yield fp.PartialResponse(text=msg.text)
        else:
            yield fp.PartialResponse(text="Alright, what else would you like to do?")
    except Exception as e:
        logger.error(f"Error in handle_salary_negotiation: {e}")
        yield fp.PartialResponse(
            text="An error occurred while processing your request. Please try again."
        )
