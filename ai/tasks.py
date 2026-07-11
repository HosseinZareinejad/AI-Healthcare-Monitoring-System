from crewai import Task
from .agents import data_collector, health_analyst

def get_data_retrieval_task(patient_id: str) -> Task:
    return Task(
        description=(
            f"Use your tool to fetch the recent glucose records for patient ID {patient_id}. "
            "Ensure you successfully retrieve the data and format it cleanly so the analyst can read it."
        ),
        expected_output="A structured list of recent glucose readings including timestamps, levels, and meal status.",
        agent=data_collector
    )

def get_health_analysis_task(patient_id: str) -> Task:
    return Task(
        description=(
            f"Analyze the glucose data retrieved for patient ID {patient_id}. "
            "Identify any concerning trends (e.g., values consistently above 180 mg/dL post-meal, or fasting values above 130). "
            "Provide a short, easy-to-understand health report directly addressing the patient. "
            "Include an 'Assessment' section and a 'Recommendations' section."
        ),
        expected_output="A markdown-formatted medical assessment report with actionable recommendations.",
        agent=health_analyst
    )

def get_chat_analysis_task(patient_id: str, user_message: str) -> Task:
    return Task(
        description=(
            f"Analyze the glucose data retrieved for patient ID {patient_id} in the context of the user's specific query: '{user_message}'. "
            "Provide a short, easy-to-understand response addressing the user's question directly. "
            "Keep the response concise and suitable for text-to-speech reading."
        ),
        expected_output="A conversational, concise response directly answering the user's question based on their medical data.",
        agent=health_analyst
    )
