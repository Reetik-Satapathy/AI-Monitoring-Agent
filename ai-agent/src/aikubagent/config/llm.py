import os

from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


llm = LLM(
    model="openrouter/openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)