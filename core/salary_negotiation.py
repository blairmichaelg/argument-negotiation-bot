from typing import AsyncIterable
import fastapi_poe as fp
from utils.prompt_engineering import create_prompt
from utils.external_api import fetch_salary_data
import re


async def handle_salary_negotiation(
    request: fp.QueryRequest, user_input: str, user_data: dict
) -> AsyncIterable[fp.PartialResponse]:
    """
    Handles user requests for salary negotiation advice.

    Parameters:
        request (fp.QueryRequest): The request object containing user input and context.
        user_input (str): The user's input regarding salary negotiation details.
        user_data (dict): User-specific data for personalized responses.

    Yields:
        AsyncIterable[fp.PartialResponse]: Responses providing salary negotiation advice.
    """
    job_details = user_input.replace("salary", "").strip()
    prompt = create_prompt("salary_negotiation", topic=job_details)

    yield fp.PartialResponse(
        text="Analyzing the job details and preparing negotiation advice...\n\n"
    )

    # Initial advice
    async for msg in fp.stream_request(request, "GPT-4", prompt=prompt):
        yield fp.PartialResponse(text=msg.text)

    # Fetch and provide salary data
    try:
        job_title, location = extract_job_and_location(job_details)
        salary_data = await asyncio.to_thread(fetch_salary_data, job_title, location)

        if "error" in salary_data:
            yield fp.PartialResponse(text=f"Salary Insights: {salary_data['error']}")
        else:
            yield fp.PartialResponse(
                text=f"Salary Insights:\nAverage Salary: ${salary_data['average_salary']} {salary_data['currency']}"
            )
    except Exception as e:
        yield fp.PartialResponse(
            text=f"Sorry, there was an error fetching salary data: {e}"
        )

    yield fp.PartialResponse(
        text="\n\nWould you like to:\n"
        "1. Practice a negotiation scenario?\n"
        "2. Get advice on specific negotiation points?\n"
        "3. Do something else?"
    )

    # Handle user choice
    user_choice = await request.get_next_message()
    if "1" in user_choice.content or "practice" in user_choice.content.lower():
        yield fp.PartialResponse(
            text="Okay, let's practice. What's your proposed salary?"
        )
        user_proposal = await request.get_next_message()
        async for msg in await simulate_negotiation(
            request, job_details, user_proposal.content
        ):
            yield msg
    elif "2" in user_choice.content or "advice" in user_choice.content.lower():
        yield fp.PartialResponse(
            text="Sure, tell me about the specific negotiation point you need advice on."
        )
    else:
        yield fp.PartialResponse(text="Alright, what else would you like to do?")


def extract_job_and_location(job_details: str) -> tuple[str, str]:
    """
    Extracts job title and location from user input.

    Parameters:
        job_details (str): The user input containing job details.

    Returns:
        tuple[str, str]: A tuple containing the job title and location.
    """
    job_title = ""
    location = ""

    match = re.search(r"job title is\s*([^\.]+)", job_details, re.IGNORECASE)
    if match:
        job_title = match.group(1).strip()

    match = re.search(r"location is\s*([^\.]+)", job_details, re.IGNORECASE)
    if match:
        location = match.group(1).strip()

    return job_title, location


async def simulate_negotiation(
    request: fp.QueryRequest, job_details: str, user_proposal: str
) -> AsyncIterable[fp.PartialResponse]:
    """
    Simulates a salary negotiation based on job details and the user's proposal.

    Parameters:
        request (fp.QueryRequest): The request object.
        job_details (str): The job details relevant to the negotiation.
        user_proposal (str): The user's proposed salary.

    Yields:
        AsyncIterable[fp.PartialResponse]: The simulated responses from the employer.
    """
    simulation_prompt = f"Simulate a salary negotiation for this job: {job_details}\n\nThe candidate has proposed: {user_proposal}\n\nProvide a realistic employer response and potential counter-offer."
    async for msg in fp.stream_request(request, "GPT-4", prompt=simulation_prompt):
        yield fp.PartialResponse(text=msg.text)
