# File: tests/test_fact_check.py

from fastapi_poe import BotError
import pytest
from unittest.mock import AsyncMock, patch
from core.fact_check import handle_fact_check


@pytest.mark.asyncio
class TestFactCheck:
    async def test_handle_fact_check_valid_input(self):
        """
        Test case for the `handle_fact_check` function with valid input.
        This test case verifies the behavior of the `handle_fact_check` function when provided with valid input. It mocks the necessary dependencies and asserts the expected responses.
        """
        request = AsyncMock()
        request.get_next_message = AsyncMock(
            side_effect=[AsyncMock(content="fact check this statement")]
        )
        user_input = "fact check this statement"

        with patch("core.fact_check.fp.stream_request") as mock_stream_request:
            mock_stream_request.return_value = AsyncMock(
                __aiter__=AsyncMock(
                    return_value=[
                        AsyncMock(text="Fact check result: True"),
                    ]
                )
            )

            responses = [
                response
                async for response in handle_fact_check(
                    request=request, user_input=user_input
                )
            ]

        assert responses[0].text == "Fact check result: True"

    async def test_handle_fact_check_invalid_input(self):
        request = AsyncMock()
        request.get_next_message = AsyncMock(
            side_effect=[AsyncMock(content="invalid input")]
        )
        user_input = "invalid input"

        with patch("core.fact_check.fp.stream_request") as mock_stream_request:
            mock_stream_request.return_value = AsyncMock(
                __aiter__=AsyncMock(
                    return_value=[
                        AsyncMock(text="Invalid input for fact checking"),
                    ]
                )
            )

            responses = [
                response
                async for response in handle_fact_check(
                    request=request, user_input=user_input
                )
            ]

        assert responses[0].text == "Invalid input for fact checking"


async def test_handle_fact_check_no_statement(self):
    request = AsyncMock()
    user_input = "fact-check"

    with pytest.raises(BotError, match="Please provide a statement to fact-check."):
        async for _ in handle_fact_check(request, user_input):
            pass
        request = AsyncMock()
        user_input = "fact-check"

        with pytest.raises(BotError, match="Please provide a statement to fact-check."):
            async for _ in handle_fact_check(request, user_input):
                pass
