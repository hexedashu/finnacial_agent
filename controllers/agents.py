import os
from dotenv import load_dotenv

# AI assistant imports
from agno.agent import Agent
from agno.models.nebius import Nebius
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

if not NEBIUS_API_KEY:
    raise ValueError("Please provide a NEBIUS API key")


web_search_agent = Agent(
    name="web_agent",
    role="search the web for reliable financial information with India-first relevance",
    model=Nebius(id="deepseek-ai/DeepSeek-R1-0528", api_key=NEBIUS_API_KEY),
    tools=[
        DuckDuckGoTools(search=True, news=True),

    ],
    instructions=[
        "You are a professional web research AI agent.",
        "Prioritize India-relevant sources and context (NSE, BSE, RBI, SEBI, Indian taxation updates).",
        "Provide exact and up-to-date information relevant to user questions.",
    ]
)

financial_agent = Agent(
    name="financial_agent",
    role="get financial information for Indian market users",
    model=Nebius(id="Qwen/Qwen3-32B", api_key=NEBIUS_API_KEY),
    tools=[
        YFinanceTools(stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True,
                    company_info=True,
                    technical_indicators=True,
                    historical_prices=True,
                    key_financial_ratios=True,
                    income_statements=True,
                    ),
    ],
    instructions=[
        "You are a professional financial advisor AI agent for Indian market queries.",
        "Prioritize NSE/BSE-listed tickers and INR context.",
        "If user gives bare Indian ticker symbols, interpret them as NSE by default (e.g., TCS -> TCS.NS).",
        "Explain risks and avoid overconfident guarantees.",
    ]
)

multi_ai = Agent(
    team=[web_search_agent, financial_agent],
    model=Nebius(id="meta-llama/Llama-3.3-70B-Instruct", api_key=NEBIUS_API_KEY),
    markdown=True,
)
