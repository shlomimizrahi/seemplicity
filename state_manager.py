"""Module for managing database interactions."""

import logging
from models import TaskResult

logging.basicConfig(level=logging.INFO)


async def store_task_result(task_id, task_name, parameters, result):
    """Stores the task result and metadata in the database."""
    try:
        await TaskResult.create(task_id=task_id, task_name=task_name, parameters=parameters, result=result)
    except Exception as e:
        # Depending on application's needs, we may want to re-raise the exception
        # or handle it in some other way.
        logging.error(f"Error storing task result: {e}")
