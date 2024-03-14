"""Main module to run the FastAPI application and handle task requests."""

import logging
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4, UUID

from fastapi import BackgroundTasks
from fastapi import FastAPI, Request
from fastapi import HTTPException
from pydantic import BaseModel
from tortoise import Tortoise

from models import TaskResult
from state_manager import create_or_update_task, DONE
from task_manager import execute_task

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    try:
        await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['models']})
        await Tortoise.generate_schemas()
        logging.info("ORM initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize ORM: {e}")


@app.on_event("shutdown")
async def shutdown() -> None:
    try:
        await Tortoise.close_connections()
        logging.info("ORM connections closed successfully.")
    except Exception as e:
        logging.error(f"Failed to close ORM connections: {e}")


@app.post("/task/")
async def create_task(background_tasks: BackgroundTasks, payload: Dict[str, Any], request: Request) -> Dict[str, str]:
    """Endpoint to create and enqueue a task.

    Args:
        request (Request): The request context, injected by FastAPI
        background_tasks (BackgroundTasks): The FastAPI background task manager.
        payload (Dict): A dictionary containing "task_name" and "parameters".

    Returns:
        Dict: A dictionary containing the UUID of the created task.
    """
    try:
        client_address = request.client.host
        task_name = payload.get("task_name")
        parameters = payload.get("parameters")
        if not task_name or not parameters:
            raise HTTPException(status_code=400, detail="task_name and parameters are required")

        task_id: UUID = uuid4()
        await create_or_update_task(task_id=str(task_id), task_name=task_name, parameters=parameters,
                                    client_address=client_address)
        background_tasks.add_task(execute_task, task_id=str(task_id), task_name=task_name, parameters=parameters)
        return {"task_id": str(task_id)}
    except Exception as e:
        logging.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail="Task creation failed")


class TaskResultResponse(BaseModel):
    task_id: str
    task_name: str
    parameters: dict
    result: str = {}
    timestamp: datetime


@app.get("/task/{task_id}", response_model=TaskResultResponse)
async def get_task_result(task_id: str) -> TaskResultResponse:
    """Endpoint to retrieve the result of a task.

    Args:
        task_id (str): The UUID of the task.

    Returns:
        TaskResultResponse: The task result and metadata.
    """
    task_result = await TaskResult.filter(task_id=task_id).first()
    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")

    task_result_response: TaskResultResponse = TaskResultResponse(
        task_id=task_id,
        task_name=task_result.task_name,
        parameters=task_result.parameters,
        timestamp=task_result.timestamp,
        state=task_result.state,
    )

    if task_result.state == DONE:
        task_result_response.result = task_result.result

    return task_result_response
