# File: tests/test_salary_negotiation.py
import pytest
from unittest.mock import patch, AsyncMock
from core.salary_negotiation import (
    handle_salary_negotiation,
    extract_job_and_location,
    simulate_negotiation,
)
import fastapi_poe as fp


def test_handle_salary_negotiation_success():
    mock_data = {"average_salary": 70000, "currency": "USD"}
    with patch('core.salary_negotiation.fetch_salary_data', return_value=mock_data):
        result = handle_salary_negotiation("Software Engineer", "New York")
        assert result == mock_data


def test_handle_salary_negotiation_api_failure():
    with patch(
        'core.salary_negotiation.fetch_salary_data',
        side_effect=RuntimeError("API request failed"),
    ):
        result = handle_salary_negotiation("Software Engineer", "New York")
        assert result == {"error": "API request failed"}


def test_handle_salary_negotiation_no_salary_data():
    mock_data = {"error": "No salary data found for this job and location."}
    with patch('core.salary_negotiation.fetch_salary_data', return_value=mock_data):
        result = handle_salary_negotiation("Software Engineer", "Nowhere")
        assert result == mock_data


def test_extract_job_and_location_success():
    job_details = "The job title is Software Engineer and the location is New York."
    job_title, location = extract_job_and_location(job_details)
    assert job_title == "Software Engineer"
    assert location == "New York"


def test_extract_job_and_location_missing_details():
    job_details = "The job title is Software Engineer."
    job_title, location = extract_job_and_location(job_details)
    assert job_title == "Software Engineer"
    assert location == ""


def test_extract_job_and_location_invalid_format():
    job_details = "Software Engineer in New York."
    job_title, location = extract_job_and_location(job_details)
    assert job_title == ""
    assert location == ""


@pytest.mark.asyncio
class TestSimulateNegotiation:
    @pytest.fixture
    def mock_request(self):
        return AsyncMock()

    @pytest.fixture
    def mock_partial_response(self):
        with patch('core.salary_negotiation.fp.PartialResponse') as mock:
            yield mock

    @pytest.fixture
    def mock_stream_request(self):
        with patch('core.salary_negotiation.fp.stream_request') as mock:
            yield mock

    async def test_simulate_negotiation(
        self, mock_request, mock_partial_response, mock_stream_request
    ):
        job_details = "Software Engineer in New York"
        user_proposal = "100000"

        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Simulated negotiation response"),
                ]
            )
        )

        responses = [
            response
            async for response in simulate_negotiation(
                mock_request, job_details, user_proposal
            )
        ]

        assert len(responses) > 0
        mock_stream_request.assert_called_once()
        assert responses[0].text == "Simulated negotiation response"
