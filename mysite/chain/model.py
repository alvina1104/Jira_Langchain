from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from mysite.config import OPENROUTER_MODEL, OPENROUTER_API_KEY, OPENROUTER_URL


ai_model = ChatOpenAI(
    model=OPENROUTER_MODEL or "openrouter/free",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_URL,
    temperature=0,
    max_completion_tokens=2000
)


def check_answer(response: AIMessage):
    if response.response_metadata.get("finish_reason") == "length":
        raise ValueError("Ответ модели был обоезан из-за ограничения токенов")

    return response

