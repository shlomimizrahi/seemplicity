import logging
from typing import Any, Dict, Callable

from state_manager import store_task_result
from tasks import sum_numbers, concat_strings, multiply_numbers

# Define constants for task names
TASK_SUM = "Sum"
TASK_CONCAT = "Concat"
TASK_MULTIPLY = "Multiply"

# Mapping of task names to their respective functions
TASKS: Dict[str, Callable] = {
    TASK_SUM: sum_numbers,
    TASK_CONCAT: concat_strings,
    TASK_MULTIPLY: multiply_numbers,
}


async def execute_task(task_id: str, task_name: str, parameters: Dict[str, Any]) -> None:
    """Executes the given task based on the task name and parameters."""
    try:
        if task_name in TASKS:
            # Retrieve the function based on task name and execute it with provided parameters
            func = TASKS[task_name]
            result = func(**parameters)
            await store_task_result(task_id, task_name, parameters, result)
        else:
            logging.error(f"Unsupported task: {task_name}")
    except Exception as e:
        logging.error(f"Error executing task {task_id}: {e}")
