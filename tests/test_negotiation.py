# File: tests/test_negotiation.py

from unittest import TestCase
import pytest
from unittest.mock import AsyncMock, patch
from core.negotiation import (
    handle_negotiation,
    analyze_offer,
    provide_negotiation_tactics,
    continue_negotiation,
    generate_bot_response,
    NegotiationScenario,
)


@pytest.mark.asyncio
class TestNegotiation:
    @pytest.fixture
    def mock_request(self):
        return AsyncMock()

    @pytest.fixture
    def mock_db(self):
        return AsyncMock()

    async def test_handle_negotiation(
        self, mock_request: AsyncMock, mock_db: AsyncMock
    ):
        with patch(
            'core.negotiation.get_db',
            return_value=AsyncMock(__anext__=AsyncMock(return_value=mock_db)),
        ), patch(
            'core.negotiation.get_negotiation_scenario_by_id', return_value=None
        ), patch(
            'core.negotiation.create_negotiation_scenario'
        ) as mock_create:
            mock_create.return_value = AsyncMock(id=1, user_offers=[], bot_responses=[])

            responses = [
                r
                async for r in handle_negotiation(
                    mock_request, "negotiation test scenario"
                )
            ]

            assert len(responses) > 0
            assert "What's your opening offer or position?" in responses[-1].text

    async def test_analyze_offer(self, mock_request: AsyncMock):
        with patch('core.negotiation.get_db'), patch(
            'core.negotiation.get_negotiation_scenario_by_id',
            return_value=AsyncMock(user_offers=[], bot_responses=[]),
        ):
            responses = [
                r
                async for r in analyze_offer(
                    mock_request, "Test analysis", "Test scenario", "Test offer"
                )
            ]

            assert len(responses) > 0

    async def test_provide_negotiation_tactics(self, mock_request: AsyncMock):
        responses = [
            r async for r in provide_negotiation_tactics(mock_request, "Test scenario")
        ]

        assert len(responses) > 0

    async def test_continue_negotiation(self, mock_request: AsyncMock):
        with patch('core.negotiation.get_db'), patch(
            'core.negotiation.get_negotiation_scenario_by_id',
            return_value=AsyncMock(user_offers=[], bot_responses=[]),
        ):
            responses = [
                r
                async for r in continue_negotiation(
                    mock_request, "Test scenario", "Test offer"
                )
            ]

            assert len(responses) > 0


class TestGenerateBotResponse(TestCase):
    @patch('core.negotiation.fp.stream_request')
    @patch('core.negotiation.analyze_sentiment')
    async def test_generate_bot_response_success(
        self, mock_analyze_sentiment, mock_stream_request
    ):
        # Mock the stream_request to return a successful response
        mock_stream_request.return_value = AsyncMock()
        mock_stream_request.return_value.__aiter__.return_value = [
            AsyncMock(text="This is a bot response")
        ]

        # Mock the analyze_sentiment to return a sentiment analysis
        mock_analyze_sentiment.return_value = "Positive"

        request = AsyncMock()
        scenario = "Test Scenario"
        user_offer = "Test Offer"
        state = {"user_offers": ["Test Offer 1"], "bot_responses": ["Test Response 1"]}
        negotiation_scenario = NegotiationScenario(scenario, state)

        response = await generate_bot_response(
            request=request,
            negotiation_scenario=negotiation_scenario,
            user_offer=user_offer,
            scenario="Test Scenario",
        )

        self.assertIn("This is a bot response", response)
        self.assertIn("(Sentiment: Positive)", response)

    @patch('core.negotiation.fp.stream_request')
    @patch('core.negotiation.analyze_sentiment')
    async def test_generate_bot_response_exception(
        self, mock_analyze_sentiment, mock_stream_request
    ):
        # Mock the stream_request to raise an exception
        mock_stream_request.side_effect = Exception("Stream request failed")

        request = AsyncMock()
        scenario = "Test Scenario"
        user_offer = "Test Offer"
        state = {"user_offers": ["Test Offer 1"], "bot_responses": ["Test Response 1"]}
        negotiation_scenario = NegotiationScenario(scenario, state)

        response = await generate_bot_response(
            request=request,
            negotiation_scenario=negotiation_scenario,
            user_offer=user_offer,
            scenario="Test Scenario",
        )

        self.assertEqual(
            response, "I'm having trouble responding right now. Please try again later."
        )

    @patch('core.negotiation.fp.stream_request')
    @patch('core.negotiation.analyze_sentiment')
    async def test_generate_bot_response_no_response(
        self, mock_analyze_sentiment, mock_stream_request
    ):
        # Mock the stream_request to return an empty response
        mock_stream_request.return_value = AsyncMock()
        mock_stream_request.return_value.__aiter__.return_value = []

        request = AsyncMock()
        scenario = "Test Scenario"
        user_offer = "Test Offer"
        state = {"user_offers": ["Test Offer 1"], "bot_responses": ["Test Response 1"]}
        negotiation_scenario = NegotiationScenario(scenario, state)

        response = await generate_bot_response(
            request=request,
            negotiation_scenario=negotiation_scenario,
            user_offer=user_offer,
            scenario="Test Scenario",
        )

        self.assertEqual(response, "No response generated.")
