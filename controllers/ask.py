import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.nebius import Nebius

load_dotenv()

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

if not NEBIUS_API_KEY:
    raise ValueError("Please provide a NEBIUS API key")

# Create agent for chat functionality
chat_agent = Agent(
    model=Nebius(id="meta-llama/Llama-3.3-70B-Instruct", api_key=NEBIUS_API_KEY),
    instructions=[
        "You are an AI investment assistant focused on the Indian market.",
        "Prioritize NSE/BSE stocks, Indian mutual funds, ETFs, and Indian macro context.",
        "Use INR by default unless the user asks for another currency.",
        "Provide clear, helpful, and accurate financial guidance with balanced risk notes."
    ],
    markdown=True
)


def nebius_chat(query: str):
    if not query:
        return {"error": "Query parameter is required"}

    try:
        response = chat_agent.run(query)
        answer = response.content
        return {"question": query, "answer": answer}

    except Exception as e:
        return {"error": str(e)}
