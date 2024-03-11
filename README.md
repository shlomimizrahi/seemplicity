# Tasker API

## Description

Tasker is an asynchronous task-running server that executes tasks based on requests it receives from clients.
The server supports three types of tasks: summing numbers, concatenating strings, and multiplying numbers.
Each task is processed asynchronously, and results are stored in a database with relevant metadata.

## Setup and Installation

### Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Tortoise ORM
- aiohttp (if making async requests in tests or main.py)

### Installation

Clone the repository:

```bash
git clone https://yourrepository.com/tasker.git
cd tasker
```

Install dependencies using Pipenv:

```bash
pip install pipenv
pipenv install
```

If you'd like to install development dependencies for running tests and linting your code, run:

```bash
pipenv install --dev
```

### Running the Application

Activate the pipenv shell to enter the virtual environment:

```bash
pipenv shell
```

Start the server:

```bash
uvicorn server:app --reload
```

(The --reload flag enables hot reloading during development)

### API Usage

Once the server is running, you can create tasks and retrieve their results using the provided endpoints.

#### Create a Task

To submit a task to the server, use the following curl command:

```bash
curl -X POST "http://127.0.0.1:8000/task/" -H "Content-Type: application/json" -d '{"task_name": "Sum", "parameters": {"a": 10, "b": 5}}
```

#### Retrieve a Task Result

To get the result of a task, make a GET request with the task ID:

```bash
curl -X GET "http://127.0.0.1:8000/task/{task_id}" -H "Accept: application/json"
```

Note: Replace {task_id} with the actual ID of the task you want to retrieve

### Testing:

You can test the API endpoints manually using curl commands as shown above, or you can write automated tests in a tests
directory.
To run tests, execute:

```bash
pytest
```

### Docker Integration
A Dockerfile is included in the project to containerize the Tasker API.
To build and run the application using Docker:

#### Build the image:

```bash
docker build -t tasker-api .
```

#### Run the container:
```bash
docker run -p 8000:8000 tasker-api
```

This will expose the API on port 8000 of your machine.



