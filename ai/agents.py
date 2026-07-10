import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from .tools import fetch_patient_history

load_dotenv()

# Initialize the LLM via CrewAI's built-in support (which uses litellm under the hood)
llm = LLM(
    model="groq/llama3-70b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

# Agent 1: Medical Data Collector
data_collector = Agent(
    role='Medical Data Collector',
    goal='Retrieve the most recent and accurate glucose readings for the patient from the database.',
    backstory=(
        "You are an expert data assistant in a healthcare system. "
        "Your job is to securely fetch medical records for patients when requested "
        "and organize the data clearly so that the Health Analyst can review it."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[fetch_patient_history],
    llm=llm
)

# Agent 2: Health Analyst
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
