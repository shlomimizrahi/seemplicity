import logging
from typing import Any, Dict, Callable

from state_manager import create_or_update_task, DONE
from tasks import sum_numbers, concat_strings, multiply_numbers

# Define constants for task names
TASK_SUM: str = "Sum"
TASK_CONCAT: str = "Concat"
TASK_MULTIPLY: str = "Multiply"

# Mapping of task names to their respective functions
TASKS: Dict[str, Callable] = {
    TASK_SUM: sum_numbers,
    TASK_CONCAT: concat_strings,
    TASK_MULTIPLY: multiply_numbers,
}


async def execute_task(task_id: str, task_name: str, parameters: Dict[str, Any]) -> Any:
    """Executes the given task based on the task name and parameters."""
    try:
        if task_name in TASKS:
            # Retrieve the function based on task name and execute it with provided parameters
            func = TASKS[task_name]
            return func(**parameters)
        else:
            logging.error(f"Unsupported task: {task_name}")
    except Exception as e:
        logging.error(f"Error executing task {task_id}: {e}")
