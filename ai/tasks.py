from crewai import Task
from .agents import health_analyst

def get_health_analysis_task(patient_id: str, patient_data: str) -> Task:
    return Task(
        description=(
            f"Analyze the following glucose data for patient ID {patient_id}:\n\n"
            f"{patient_data}\n\n"
            "Identify any concerning trends (e.g., values consistently above 180 mg/dL post-meal, or fasting values above 130). "
            "Provide a short, easy-to-understand health report directly addressing the patient. "
            "Include an 'Assessment' section and a 'Recommendations' section."
        ),
        expected_output="A markdown-formatted medical assessment report with actionable recommendations.",
        agent=health_analyst
    )

def get_chat_analysis_task(patient_id: str, patient_data: str, user_message: str) -> Task:
    return Task(
        description=(
            f"Analyze the following glucose data for patient ID {patient_id}:\n\n"
            f"{patient_data}\n\n"
            f"In the context of this data, answer the user's specific query: '{user_message}'. "
            "Provide a short, easy-to-understand response addressing the user's question directly. "
            "Keep the response concise and suitable for text-to-speech reading."
        ),
        expected_output="A conversational, concise response directly answering the user's question based on their medical data.",
        agent=health_analyst
    )
