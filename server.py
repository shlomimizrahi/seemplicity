"""Main module to run the FastAPI application and handle task requests."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from typing_extensions import TypedDict
from uuid import uuid4, UUID

from fastapi import FastAPI, BackgroundTasks
from fastapi import HTTPException
from tortoise import Tortoise

from models import TaskResult
from task_manager import execute_task

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@asynccontextmanager
async def lifespan():
    """Initializes Tortoise ORM at the application startup.
      Closes Tortoise ORM connections at the application shutdown."""
    try:
        await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['models']})
        await Tortoise.generate_schemas()
    except Exception as e:
        logging.error(f"Failed to initialize ORM: {e}")
        # We might want to stop the app from running if critical DB connection can't be established
        raise HTTPException(status_code=500, detail="Could not initialize database connection")
    yield

    try:
        await Tortoise.close_connections()
    except Exception as e:
        logging.error(f"Failed to close ORM connections: {e}")


@app.post("/task/")
async def create_task(background_tasks: BackgroundTasks, payload: Dict[str, Any]) -> Dict[str, str]:
    """Endpoint to create and enqueue a task.

    Args:
        background_tasks (BackgroundTasks): The FastAPI background task manager.
        payload (dict): A dictionary containing "task_name" and "parameters".

    Returns:
        dict: A dictionary containing the UUID of the created task.
    """
    try:
        task_name = payload.get("task_name")
        parameters = payload.get("parameters")
        if not task_name or not parameters:
            raise HTTPException(status_code=400, detail="task_name and parameters are required")

        task_id: UUID = uuid4()
        background_tasks.add_task(execute_task, task_id=str(task_id), task_name=task_name, parameters=parameters)
        return {"task_id": str(task_id)}
    except Exception as e:
        logging.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail="Task creation failed")


class TaskResultResponse(TypedDict):
    task_id: str
    task_name: str
    parameters: dict
    result: str
    timestamp: datetime


@app.get("/task/{task_id}", response_model=TaskResultResponse)
async def get_task_result(task_id: str) -> TaskResultResponse:
    """Endpoint to retrieve the result of a task.

    Args:
        task_id (str): The UUID of the task.

    Returns:
        TaskResultResponse: A dictionary containing the task result and metadata.
    """
    task_result = await TaskResult.filter(task_id=task_id).first()
    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task_id,
        "task_name": task_result.task_name,
        "parameters": task_result.parameters,
        "result": task_result.result,
        "timestamp": task_result.timestamp
    }
