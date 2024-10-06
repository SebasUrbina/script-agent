# Task Automation Agent using OpenAI GPT-4

This Python project uses OpenAI's API to generate and execute a series of subtasks based on a given main task. The system creates an AI agent that interprets a task description, breaks it down into smaller tasks, and provides bash scripts to fulfill each of them.

## Features

- Generates subtasks using GPT-4.
- Automatically creates bash scripts for subtasks.
- Executes generated bash scripts to accomplish the main task.
- Modular and easy to extend for various automation tasks.

## Requirements

- Python 3.x
- OpenAI API key
- Required libraries:
  - `openai`
  - `pydantic`
  - `python-dotenv`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SebasUrbina/script-agent
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## How to Use

1. Run the script:
    ```bash
    python main.py
    ```

2. Enter the main task when prompted. For example:
    ```
    Task: Create a python script that implements a ball bouncing using the pygame library and execute it.
    ```

3. The agent will generate the required subtasks, bash scripts, and execute them to fulfill the main task.

## License

This project is licensed under the MIT License.