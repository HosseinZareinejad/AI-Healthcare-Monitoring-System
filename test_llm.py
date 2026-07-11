import os
from crewai import Agent, LLM, Task, Crew
from dotenv import load_dotenv

load_dotenv()

import litellm

_original_completion = litellm.completion
def patched_completion(*args, **kwargs):
    if 'messages' in kwargs:
        for msg in kwargs['messages']:
            msg.pop('cache_breakpoint', None)
    return _original_completion(*args, **kwargs)
litellm.completion = patched_completion
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

data_collector = Agent(
    role='Medical Data Collector',
    goal='Retrieve data',
    backstory='You fetch data.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

task = Task(
    description='Say hello',
    expected_output='A greeting',
    agent=data_collector
)

crew = Crew(
    agents=[data_collector],
    tasks=[task],
    verbose=True
)

try:
    print(crew.kickoff())
except Exception as e:
    import traceback
    traceback.print_exc()
