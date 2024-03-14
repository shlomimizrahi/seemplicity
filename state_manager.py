import logging
from typing import Dict, Union, Any

from models import TaskResult

logging.basicConfig(level=logging.INFO)

# Task states
PENDING: str = "PENDING"
DONE: str = "DONE"
FAILED: str = "FAILED"


async def create_or_update_task(task_id: str,
                                task_name: str,
                                parameters: Dict[str, Union[int, str]],
                                client_address: str = None,
                                state: str = PENDING,
                                result: Any = None) -> None:
    """Stores or updates the task result and metadata in the database."""
    try:
        defaults = {
            'task_name': task_name,
            'parameters': parameters,
            'state': state
        }

        # Only include 'result' and 'client_address' in defaults if they are provided
        if result is not None:
            defaults['result'] = result
        if client_address:
            defaults['client_address'] = client_address

        # Use update_or_create to either update an existing record or create a new one
        taskResult, _ = await TaskResult.update_or_create(defaults=defaults, task_id=task_id)
        if not taskResult:
            raise Exception("Error creating  / updating task entry in db")

    except Exception as e:
        logging.error(f"Error storing task result: {e}")
