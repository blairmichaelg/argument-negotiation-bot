# File: tests/test_negotiation.py

from unittest import TestCase
from unittest.mock import patch, AsyncMock
from core.negotiation import generate_bot_response


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

        response = await generate_bot_response(request, scenario, user_offer, state)

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

        response = await generate_bot_response(request, scenario, user_offer, state)

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

        response = await generate_bot_response(request, scenario, user_offer, state)

        self.assertEqual(response, "No response generated.")
