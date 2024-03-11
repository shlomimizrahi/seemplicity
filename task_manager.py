"""Module for managing task execution and result handling."""
import logging

from state_manager import store_task_result
from tasks import sum_numbers, concat_strings, multiply_numbers

logging.basicConfig(level=logging.INFO)


async def execute_task(task_id, task_name, parameters):
    """Executes the given task based on the task name and parameters."""
    try:
        result = None
        if task_name == "Sum":
            result = sum_numbers(parameters['a'], parameters['b'])
        elif task_name == "Concat":
            result = concat_strings(parameters['str1'], parameters['str2'], parameters['str3'])
        elif task_name == "Multiply":
            result = multiply_numbers(parameters['a'], parameters['b'])
        await store_task_result(task_id, task_name, parameters, result)
    except Exception as e:
        logging.error(f"Error executing task {task_id}: {e}")
