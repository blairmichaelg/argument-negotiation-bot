# File: tests/test_contract_analysis.py
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
import fastapi_poe as fp
from core.contract_analysis import (
    handle_contract_analysis,
    get_detailed_breakdown,
    get_legal_implications,
    get_sentiment_analysis,
    suggest_improvements,
)


@pytest.mark.asyncio
class TestHandleContractAnalysis:
    @pytest.fixture
    def mock_request(self):
        return AsyncMock()

    @pytest.fixture
    def mock_partial_response(self):
        with patch('core.contract_analysis.fp.PartialResponse') as mock:
            yield mock

    @pytest.fixture
    def mock_create_prompt(self):
        with patch('core.contract_analysis.create_prompt') as mock:
            yield mock

    @pytest.fixture
    def mock_stream_request(self):
        with patch('core.contract_analysis.fp.stream_request') as mock:
            yield mock

    async def test_handle_contract_analysis_valid_clause(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
    ):
        user_input = "Analyze contract clause This is a test clause"
        user_data = {}

        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Initial analysis response"),
                    fp.PartialResponse(text="Detailed breakdown response"),
                    fp.PartialResponse(text="Legal implications response"),
                    fp.PartialResponse(text="Sentiment analysis response"),
                ]
            )
        )

        responses = [
            response
            async for response in handle_contract_analysis(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        mock_stream_request.assert_called_once()
        assert responses[0].text == "Analyzing the contract clause...\n\n"
        assert responses[1].text == "Initial analysis response"
        assert responses[2].text == "\n\nProviding a detailed breakdown:\n\n"
        assert responses[3].text == "Detailed breakdown response"
        assert responses[4].text == "Potential legal implications:\n\n"
        assert responses[5].text == "Legal implications response"
        assert responses[6].text == "Sentiment analysis response"
        assert (
            responses[7].text
            == "\n\nWould you like to: \n1. Suggest improvements to the clause?\n2. Analyze another clause?\n3. Do something else?"
        )

    async def test_handle_contract_analysis_exception_handling(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
    ):
        user_input = "Analyze contract clause This is a test clause"
        user_data = {}

        mock_stream_request.side_effect = Exception("Test exception")

        responses = [
            response
            async for response in handle_contract_analysis(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        assert responses[0].text == "Analyzing the contract clause...\n\n"
        assert (
            responses[1].text
            == "An error occurred during the analysis. Please try again later."
        )

    async def test_get_detailed_breakdown(
        self, mock_request: AsyncMock, mock_stream_request: MagicMock | AsyncMock
    ):
        contract_clause = "This is a test clause for detailed breakdown"
        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(
                        text="Key Terms: Term 1, Term 2\n\nObligations: Obligation 1, Obligation 2\n\nPotential Risks: Risk 1, Risk 2"
                    ),
                ]
            )
        )

        breakdown = await get_detailed_breakdown(mock_request, contract_clause)

        assert breakdown == {
            "Key Terms": "Term 1, Term 2",
            "Obligations": "Obligation 1, Obligation 2",
            "Potential Risks": "Risk 1, Risk 2",
        }

    async def test_get_legal_implications(
        self, mock_request: AsyncMock, mock_stream_request: MagicMock | AsyncMock
    ):
        contract_clause = "This is a test clause for legal implications"
        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Legal implications response"),
                ]
            )
        )

        legal_analysis = await get_legal_implications(mock_request, contract_clause)

        assert legal_analysis == "Legal implications response"

    async def test_get_sentiment_analysis(
        self, mock_request: AsyncMock, mock_stream_request: MagicMock | AsyncMock
    ):
        contract_clause = "This is a test clause for sentiment analysis"
        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Sentiment analysis response"),
                ]
            )
        )

        sentiment = await get_sentiment_analysis(mock_request, contract_clause)

        assert sentiment == "Sentiment analysis response"

    async def test_suggest_improvements(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
    ):
        contract_clause = "This is a test clause for suggesting improvements"
        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(
                        text="Improvements: Improvement 1, Improvement 2"
                    ),
                ]
            )
        )

        responses = [
            response
            async for response in suggest_improvements(mock_request, contract_clause)
        ]

        assert len(responses) > 0
        assert responses[0].text == "Improvements: Improvement 1, Improvement 2"
        assert (
            responses[1].text
            == "\n\nWould you like to: \n1. Analyze another clause?\n2. Do something else?"
        )
