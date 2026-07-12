import os
import litellm
from crewai import Agent, LLM
from dotenv import load_dotenv

# Patch litellm to fix a bug where it sends unsupported 'cache_breakpoint' to Groq
_original_completion = litellm.completion
def patched_completion(*args, **kwargs):
    if 'messages' in kwargs:
        for msg in kwargs['messages']:
            msg.pop('cache_breakpoint', None)
    return _original_completion(*args, **kwargs)
litellm.completion = patched_completion

load_dotenv()

# Initialize the LLM via CrewAI's built-in support
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Agent: Health Analyst
health_analyst = Agent(
    role='Health Analyst',
    goal='Analyze the patient\'s glucose data and provide a clear, medically sound assessment and actionable recommendations.',
    backstory=(
        "You are a highly knowledgeable medical AI assistant. "
        "You specialize in endocrinology and diabetes management. "
        "You analyze glucose trends, identify high or low spikes (especially post-meal or fasting), "
        "and provide polite, clear, and actionable advice to the patient. "
        "You always remind the patient to consult a real doctor for critical issues."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)
