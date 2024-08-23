# File: tests/test_bias_detection.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from core.bias_detection import handle_bias_detection, bias_cache
import fastapi_poe as fp


@pytest.mark.asyncio
class TestHandleBiasDetection:
    @pytest.fixture
    def mock_request(self):
        return AsyncMock()

    @pytest.fixture
    def mock_partial_response(self):
        with patch('core.bias_detection.fp.PartialResponse') as mock:
            yield mock

    @pytest.fixture
    def mock_create_prompt(self):
        with patch('core.bias_detection.create_prompt') as mock:
            yield mock

    @pytest.fixture
    def mock_stream_request(self):
        with patch('core.bias_detection.fp.stream_request') as mock:
            yield mock

    @pytest.fixture
    def mock_detect_specific_biases(self):
        with patch('core.bias_detection.detect_specific_biases') as mock:
            yield mock

    @pytest.fixture
    def mock_explain_bias(self):
        with patch('core.bias_detection.explain_bias') as mock:
            yield mock

    @pytest.fixture
    def mock_get_user_choice(self):
        with patch('core.bias_detection.get_user_choice') as mock:
            yield mock

    @pytest.fixture
    def mock_suggest_debiasing_strategies(self):
        with patch('core.bias_detection.suggest_debiasing_strategies') as mock:
            yield mock

    async def test_handle_bias_detection_valid_argument(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
        mock_detect_specific_biases: MagicMock | AsyncMock,
        mock_explain_bias: MagicMock | AsyncMock,
        mock_get_user_choice: MagicMock | AsyncMock,
        mock_suggest_debiasing_strategies: MagicMock | AsyncMock,
    ):
        user_input = "This is a test argument with cognitive bias"
        user_data = {}

        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Initial bias detection response"),
                ]
            )
        )
        mock_detect_specific_biases.return_value = ["Confirmation Bias"]
        mock_explain_bias.return_value = "Explanation of Confirmation Bias"
        mock_get_user_choice.return_value = "1"

        responses = [
            response
            async for response in handle_bias_detection(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        mock_detect_specific_biases.assert_called_once()
        mock_explain_bias.assert_called_once()
        mock_get_user_choice.assert_called_once()
        mock_suggest_debiasing_strategies.assert_called_once()
        assert responses[0].text == "Analyzing the argument for cognitive biases...\n\n"
        assert responses[1].text == "Initial bias detection response"
        assert responses[2].text == "\n\nDetailed bias analysis:\n\n"
        assert (
            responses[3].text
            == "Confirmation Bias:\nExplanation of Confirmation Bias\n\n"
        )
        assert (
            responses[4].text
            == "\n\nWould you like to: \n1. Explore strategies to mitigate these biases?\n2. Analyze another argument?\n3. Do something else?"
        )

    async def test_handle_bias_detection_empty_argument(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
        mock_detect_specific_biases: MagicMock | AsyncMock,
        mock_explain_bias: MagicMock | AsyncMock,
        mock_get_user_choice: MagicMock | AsyncMock,
        mock_suggest_debiasing_strategies: MagicMock | AsyncMock,
    ):
        user_input = "cognitive bias"
        user_data = {}

        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Initial bias detection response"),
                ]
            )
        )
        mock_detect_specific_biases.return_value = []
        mock_get_user_choice.return_value = "2"

        responses = [
            response
            async for response in handle_bias_detection(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        mock_detect_specific_biases.assert_called_once()
        mock_get_user_choice.assert_called_once()
        assert responses[0].text == "Analyzing the argument for cognitive biases...\n\n"
        assert responses[1].text == "Initial bias detection response"
        assert responses[2].text == "\n\nDetailed bias analysis:\n\n"
        assert (
            responses[3].text
            == "\n\nWould you like to: \n1. Explore strategies to mitigate these biases?\n2. Analyze another argument?\n3. Do something else?"
        )

    async def test_handle_bias_detection_argument_in_cache(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
        mock_detect_specific_biases: MagicMock | AsyncMock,
        mock_explain_bias: MagicMock | AsyncMock,
        mock_get_user_choice: MagicMock | AsyncMock,
        mock_suggest_debiasing_strategies: MagicMock | AsyncMock,
    ):
        user_input = "This is a cached argument"
        user_data = {}
        bias_cache[user_input] = ["Anchoring Bias"]

        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Initial bias detection response"),
                ]
            )
        )
        mock_explain_bias.return_value = "Explanation of Anchoring Bias"
        mock_get_user_choice.return_value = "1"

        responses = [
            response
            async for response in handle_bias_detection(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        mock_detect_specific_biases.assert_not_called()
        mock_explain_bias.assert_called_once()
        mock_get_user_choice.assert_called_once()
        mock_suggest_debiasing_strategies.assert_called_once()
        assert responses[0].text == "Analyzing the argument for cognitive biases...\n\n"
        assert responses[1].text == "Initial bias detection response"
        assert responses[2].text == "\n\nDetailed bias analysis:\n\n"
        assert responses[3].text == "Anchoring Bias:\nExplanation of Anchoring Bias\n\n"
        assert (
            responses[4].text
            == "\n\nWould you like to: \n1. Explore strategies to mitigate these biases?\n2. Analyze another argument?\n3. Do something else?"
        )

    async def test_handle_bias_detection_argument_not_in_cache(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
        mock_detect_specific_biases: MagicMock | AsyncMock,
        mock_explain_bias: MagicMock | AsyncMock,
        mock_get_user_choice: MagicMock | AsyncMock,
        mock_suggest_debiasing_strategies: MagicMock | AsyncMock,
    ):
        user_input = "This is a new argument"
        user_data = {}

        mock_stream_request.return_value = AsyncMock(
            __aiter__=AsyncMock(
                return_value=[
                    fp.PartialResponse(text="Initial bias detection response"),
                ]
            )
        )
        mock_detect_specific_biases.return_value = ["Framing Effect"]
        mock_explain_bias.return_value = "Explanation of Framing Effect"
        mock_get_user_choice.return_value = "1"

        responses = [
            response
            async for response in handle_bias_detection(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        mock_detect_specific_biases.assert_called_once()
        mock_explain_bias.assert_called_once()
        mock_get_user_choice.assert_called_once()
        mock_suggest_debiasing_strategies.assert_called_once()
        assert responses[0].text == "Analyzing the argument for cognitive biases...\n\n"
        assert responses[1].text == "Initial bias detection response"
        assert responses[2].text == "\n\nDetailed bias analysis:\n\n"
        assert responses[3].text == "Framing Effect:\nExplanation of Framing Effect\n\n"
        assert (
            responses[4].text
            == "\n\nWould you like to: \n1. Explore strategies to mitigate these biases?\n2. Analyze another argument?\n3. Do something else?"
        )

    async def test_handle_bias_detection_error_handling(
        self,
        mock_request: AsyncMock,
        mock_partial_response: MagicMock | AsyncMock,
        mock_create_prompt: MagicMock | AsyncMock,
        mock_stream_request: MagicMock | AsyncMock,
        mock_detect_specific_biases: MagicMock | AsyncMock,
        mock_explain_bias: MagicMock | AsyncMock,
        mock_get_user_choice: MagicMock | AsyncMock,
        mock_suggest_debiasing_strategies: MagicMock | AsyncMock,
    ):
        user_input = "This will cause an error"
        user_data = {}

        mock_stream_request.side_effect = Exception("Test Exception")

        responses = [
            response
            async for response in handle_bias_detection(
                mock_request, user_input, user_data
            )
        ]

        assert len(responses) > 0
        mock_create_prompt.assert_called_once()
        mock_detect_specific_biases.assert_not_called()
        mock_explain_bias.assert_not_called()
        mock_get_user_choice.assert_not_called()
        mock_suggest_debiasing_strategies.assert_not_called()
        assert "An error occurred while processing your request" in responses[-1].text
