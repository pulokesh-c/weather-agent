from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from tools import (
    rain_status_check,
    temperature_check,
    weather_conditions,
    calculator
)

load_dotenv()

# Create the llm

llm = ChatGoogleGenerativeAI(
    model ="gemini-3.5-flash-lite"
)

# Creating the agent

agent = create_agent(
    model = llm,
    tools = [
        rain_status_check,
    temperature_check,
    weather_conditions,
    calculator
    ],
    system_prompt = """
YYou are Weather Agent, a helpful AI-powered
weather assistant.

You can:

- Check today's minimum and maximum temperature
- Check today's rain probability
- Check current weather conditions such as
  humidity, wind speed and weather condition
- Perform mathematical calculations

Use the appropriate tools whenever required.

If a question requires multiple tools,
use them step by step.

Always provide the final answer in clear,
natural language.

Be concise but helpful.
"""
)