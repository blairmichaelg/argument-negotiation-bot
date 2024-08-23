import pytest
from unittest.mock import patch, AsyncMock
from core.salary_negotiation import (
    handle_salary_negotiation,
    extract_job_details,
    format_salary_data,
    fetch_salary_data,
)
import fastapi_poe as fp


@pytest.mark.asyncio
async def test_handle_salary_negotiation():
    request = AsyncMock(spec=fp.QueryRequest)
    user_input = "Software Engineer in San Francisco"
    user_data = {}

    with patch(
        "core.salary_negotiation.extract_job_details"
    ) as mock_extract_job_details:
        mock_extract_job_details.return_value = {
            "job_title": "Software Engineer",
            "location": "San Francisco",
        }

        with patch(
            "core.salary_negotiation.fetch_salary_data"
        ) as mock_fetch_salary_data:
            mock_fetch_salary_data.return_value = {
                "average_salary": 120000,
                "currency": "USD",
            }

            with patch(
                "core.salary_negotiation.format_salary_data"
            ) as mock_format_salary_data:
                mock_format_salary_data.return_value = "Average Salary: $120,000 USD"

                responses = []
                async for response in handle_salary_negotiation(
                    request, user_input, user_data
                ):
                    responses.append(response)

                assert len(responses) > 0
                assert "Average Salary: $120,000 USD" in responses[0].text


@pytest.mark.asyncio
async def test_extract_job_details():
    user_input = "Software Engineer in San Francisco"
    result = extract_job_details(user_input)
    assert result["job_title"] == "Software Engineer"
    assert result["location"] == "San Francisco"


@pytest.mark.asyncio
async def test_fetch_salary_data():
    job_title = "Software Engineer"
    location = "San Francisco"
    result = await fetch_salary_data(job_title, location)
    assert result["average_salary"] > 0
    assert result["currency"] == "USD"


@pytest.mark.asyncio
async def test_format_salary_data():
    salary_data = {"average_salary": 120000, "currency": "USD"}
    result = format_salary_data(salary_data)
    assert result == "Average Salary: $120,000 USD"
