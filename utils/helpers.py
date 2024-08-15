import openai
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def analyze_sentiment(text: str) -> str:
    """Analyzes the sentiment of the given text using OpenAI."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=f"Analyze the sentiment of the following text:\n\n{text}\n\nSentiment:",
            max_tokens=10,
            temperature=0.0, 
        )
        sentiment = response.choices[0].text.strip().lower()
        return sentiment
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return "neutral"  

async def generate_dynamic_follow_up_questions(
    functionality: str, user_input: str, interaction_history: str
) -> list[str]:
    """Generates context-aware follow-up questions using OpenAI."""
    try:
        context_prompt = f"""
        The user is interacting with a bot specializing in argument and negotiation.
        The user's current input is: {user_input}
        The previous conversation history is: {interaction_history}
        The bot's functionality being used is: {functionality}

        Generate 3 relevant and engaging follow-up questions based on this context.
        Provide the questions as a numbered list.
        """

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=context_prompt,
            max_tokens=100,
            temperature=0.7,  
            n=1,
            stop=None,
        )

        questions_text = response.choices[0].text.strip()
        questions_list = questions_text.split("\n")
        return [question.strip() for question in questions_list if question.strip()]

    except Exception as e:
        logger.error(f"Error generating follow-up questions: {e}")
        return []