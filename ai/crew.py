from crewai import Crew, Process
from .agents import data_collector, health_analyst
from .tasks import get_data_retrieval_task, get_health_analysis_task

def run_analysis_crew(patient_id: str) -> str:
    """
    Assembles and runs the CrewAI process for the given patient_id.
    """
    
    # 1. Instantiate tasks for this specific run
    retrieval_task = get_data_retrieval_task(patient_id)
    analysis_task = get_health_analysis_task(patient_id)
    
    # 2. Form the Crew
    healthcare_crew = Crew(
        agents=[data_collector, health_analyst],
        tasks=[retrieval_task, analysis_task],
        process=Process.sequential, # Tasks execute sequentially
        verbose=True # or 2 for more debug logs
    )
    
    # 3. Execute
    result = healthcare_crew.kickoff()
    
    return str(result)

def run_chat_crew(patient_id: str, user_message: str) -> str:
    """
    Assembles and runs the CrewAI process for conversational queries.
    """
    from .tasks import get_chat_analysis_task
    
    retrieval_task = get_data_retrieval_task(patient_id)
    chat_task = get_chat_analysis_task(patient_id, user_message)
    
    healthcare_crew = Crew(
        agents=[data_collector, health_analyst],
        tasks=[retrieval_task, chat_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = healthcare_crew.kickoff()
    return str(result)
