# File: tests/test_debate.py

from fastapi_poe import BotError
import pytest
from unittest.mock import AsyncMock, patch
from core.debate import handle_debate, generate_counterarguments


@pytest.mark.asyncio
class TestHandleDebate:
    async def test_handle_debate_valid_input(self):
        """
        Test case for the `handle_debate` function with valid input.
        This test case verifies the behavior of the `handle_debate` function when provided with valid input. It mocks the necessary dependencies and asserts the expected responses.
        """
        request = AsyncMock()
        request.get_next_message = AsyncMock(
            side_effect=[AsyncMock(content="pro"), AsyncMock(content="1")]
        )
        user_input = "debate climate change"

        with patch("core.debate.fp.stream_request") as mock_stream_request:
            mock_stream_request.return_value = AsyncMock(
                __aiter__=AsyncMock(
                    return_value=[
                        AsyncMock(text="Debate on climate change"),
                        AsyncMock(text="\n\nWhich side would you like to argue for?"),
                        AsyncMock(text="Arguments for pro side"),
                        AsyncMock(
                            text="\n\nWould you like to:\n1. Continue the debate?\n2. Explore counterarguments?\n3. Do something else?"
                        ),
                        AsyncMock(text="Counterarguments against pro side"),
                    ]
                )
            )

            responses = [
                response async for response in handle_debate(request, user_input)
            ]

        assert responses[0].text == "Debate on climate change"
        assert responses[1].text == "\n\nWhich side would you like to argue for?"
        assert responses[2].text == "Arguments for pro side"
        assert (
            responses[3].text
            == "\n\nWould you like to:\n1. Continue the debate?\n2. Explore counterarguments?\n3. Do something else?"
        )
        assert responses[4].text == "Counterarguments against pro side"

    async def test_handle_debate_invalid_input(self):
        request = AsyncMock()
        request.get_next_message = AsyncMock(
            side_effect=[AsyncMock(content="invalid"), AsyncMock(content="1")]
        )
        user_input = "debate climate change"

        with patch("core.debate.fp.stream_request") as mock_stream_request:
            mock_stream_request.return_value = AsyncMock(
                __aiter__=AsyncMock(
                    return_value=[
                        AsyncMock(text="Debate on climate change"),
                        AsyncMock(text="Invalid side selected"),
                    ]
                )
            )

            responses = [
                response async for response in handle_debate(request, user_input)
            ]

        assert responses[0].text == "Debate on climate change"
        assert responses[1].text == "Invalid side selected"

    async def test_generate_counterarguments(self):
        request = AsyncMock()
        topic = "climate change"
        side = "pro"

        with patch("core.debate.fp.stream_request") as mock_stream_request:
            mock_stream_request.return_value = AsyncMock(
                __aiter__=AsyncMock(
                    return_value=[AsyncMock(text="Counterargument against pro side")]
                )
            )

            responses = [
                response
                async for response in generate_counterarguments(request, topic, side)
            ]

        assert responses[0].text == "Counterargument against pro side"

        async def test_handle_debate_no_topic(self):
            request = AsyncMock()
            user_input = "debate"

            with pytest.raises(BotError, match="Please provide a debate topic."):
                async for _ in handle_debate(request, user_input):
                    pass
