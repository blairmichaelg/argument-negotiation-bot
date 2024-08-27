import unittest

from prompt_engineering import PROMPT_TEMPLATES, create_prompt


class TestCreatePrompt(unittest.TestCase):
    def setUp(self):
        # This method will run before each test
        self.templates = PROMPT_TEMPLATES

    def test_valid_functionality(self):
        # Test with valid functionality and arguments
        result = create_prompt("debate", topic="Climate Change")
        expected = "Generate two opposing viewpoints on the topic: Climate Change. Provide clear arguments for both sides, citing relevant facts or examples."
        self.assertEqual(result, expected)

    def test_invalid_functionality(self):
        # Test with invalid functionality
        with self.assertRaises(ValueError):
            create_prompt("invalid_functionality", topic="Climate Change")

    def test_missing_arguments(self):
        # Test with missing arguments
        with self.assertRaises(KeyError):
            create_prompt("debate")

    def test_additional_arguments(self):
        # Test with additional arguments
        result = create_prompt("debate", topic="Climate Change", extra="extra_argument")
        expected = "Generate two opposing viewpoints on the topic: Climate Change. Provide clear arguments for both sides, citing relevant facts or examples."
        self.assertEqual(result, expected)

    def test_negotiation_functionality(self):
        # Test negotiation functionality
        result = create_prompt("negotiation", topic="Salary Increase")
        expected = "Create a realistic negotiation scenario based on: Salary Increase. Outline the interests, positions, and potential areas for compromise for both parties involved."
        self.assertEqual(result, expected)

    def test_fact_check_functionality(self):
        # Test fact-check functionality
        result = create_prompt("fact-check", topic="The Earth is flat.")
        expected = "Fact-check the following statement, providing a clear verdict and citing credible sources to support your conclusion: The Earth is flat."
        self.assertEqual(result, expected)

    def test_bias_detection_functionality(self):
        # Test bias detection functionality
        result = create_prompt("bias_detection", topic="All politicians are corrupt.")
        expected = "Analyze the following argument for cognitive biases: All politicians are corrupt. Identify specific biases, explain how they manifest in the argument, and suggest ways to mitigate their influence."
        self.assertEqual(result, expected)

    def test_contract_analysis_functionality(self):
        # Test contract analysis functionality
        result = create_prompt("contract_analysis", topic="Non-compete clause")
        expected = "Analyze the following contract clause, highlighting key terms, potential risks, and suggesting improvements for clarity and fairness: Non-compete clause."
        self.assertEqual(result, expected)

    def test_salary_negotiation_functionality(self):
        # Test salary negotiation functionality
        result = create_prompt(
            "salary_negotiation", topic="Software Engineer with 5 years experience"
        )
        expected = "Provide comprehensive salary negotiation advice for someone with these job details: Software Engineer with 5 years experience. Include market data, effective negotiation strategies, potential talking points, and how to handle common counter-offers."
        self.assertEqual(result, expected)

    def test_continue_negotiation_functionality(self):
        # Test continue negotiation functionality
        result = create_prompt(
            "continue_negotiation",
            topic="Salary Increase",
            user_offer="70,000 USD",
            user_offers=["60,000 USD", "65,000 USD"],
            bot_responses=["We can offer 62,000 USD", "We can offer 68,000 USD"],
        )
        expected = (
            "You are negotiating in the following scenario: Salary Increase\n\n"
            "The user has made the following offer: 70,000 USD\n\n"
            "Previous offers: ['60,000 USD', '65,000 USD']\n\n"
            "Previous bot responses: ['We can offer 62,000 USD', 'We can offer 68,000 USD']\n\n"
            "Generate a realistic and strategic response to the user's offer, considering the negotiation context and previous interactions."
        )
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
