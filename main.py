import openai
import os
from pydantic import BaseModel
from typing import List
from time import sleep
from dotenv import load_dotenv

load_dotenv()

def call_openai(client, messages, response_format):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=messages,
        response_format=response_format,
    )
    return completion.choices[0].message.parsed


class BaseTask(BaseModel):
    instruction: str
    script: str


class openAI_InitTask(BaseModel):
    instructions: List[BaseTask]


class Agent():
    def __init__(self, task):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.main_task = task
        self.tasks = self.generate_tasks(task)
    
    def __str__(self):
        return f"Agent Object (main task: {self.main_task})"
        
    def generate_tasks(self, task):
        messages = [
            {"role": "system", "content": "You are a Generative AI Agent. You have been tasked with generating subtasks based on the main task. These subtasks should be detailed and easy to understand and must be accompanied by a bash script that fulfills the subtask."},
            {"role": "user", "content": task}
        ]
        return call_openai(openai, messages, openAI_InitTask).instructions
    
    def execute_tasks(self):
        print(f"Executing {len(self.tasks)} tasks for accomplishing the main task: {self.main_task}")
        for task in self.tasks:
            print(f"\tExecuting task: {task.instruction}")
            sleep(1)
            os.system(task.script)
    
if __name__ == "__main__":
    task = input("Task: ") 
    agent = Agent(task)
    print(agent.tasks)

    print("Ejecutando tasks...")
    agent.execute_tasks()