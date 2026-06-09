# config/llms.py
from crewai import LLM
from dotenv import load_dotenv

# Ensure environment variables are loaded before model instantiation
load_dotenv()

# --- Extraction & Parsing Tier (Groq - Ultra Low Latency) ---
inventory_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1
)

route_llm = LLM(
    model="gemini/gemma-4-26b-a4b-it",
    temperature=0.1
)

# --- High-Reasoning Synthesis Tier (Google AI Studio - 31B Dense) ---
strategist_llm = LLM(
    model="gemini/gemma-4-31b-it",
    temperature=0.3  # Slight flexibility for weighing multi-variable tradeoffs
)

# --- Validation Tier (Google AI Studio - Lightweight Auditor) ---
critic_llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    temperature=0.1
)