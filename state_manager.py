"""Module for managing database interactions."""

import logging
from typing import Dict, Union, Any

from models import TaskResult

logging.basicConfig(level=logging.INFO)


async def store_task_result(task_id :str, task_name:str, parameters: Dict[str,Union[int, str]], result: Any) -> None:
    """Stores the task result and metadata in the database."""
    try:
        await TaskResult.create(task_id=task_id, task_name=task_name, parameters=parameters, result=result)
    except Exception as e:
        # Depending on application's needs, we may want to re-raise the exception
        # or handle it in some other way.
        logging.error(f"Error storing task result: {e}")
