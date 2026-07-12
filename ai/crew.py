from crewai import Crew, Process
from .agents import health_analyst
from .tasks import get_health_analysis_task, get_chat_analysis_task

def run_analysis_crew(patient_id: str, patient_data: str) -> str:
    """
    Assembles and runs the CrewAI process for the given patient_id.
    """
    analysis_task = get_health_analysis_task(patient_id, patient_data)
    
    healthcare_crew = Crew(
        agents=[health_analyst],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = healthcare_crew.kickoff()
    return str(result)

def run_chat_crew(patient_id: str, patient_data: str, user_message: str) -> str:
    """
    Assembles and runs the CrewAI process for conversational queries.
    """
    chat_task = get_chat_analysis_task(patient_id, patient_data, user_message)
    
    healthcare_crew = Crew(
        agents=[health_analyst],
        tasks=[chat_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = healthcare_crew.kickoff()
    return str(result)
