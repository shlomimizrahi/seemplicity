"""Module defining ORM models for the tasker application."""

from tortoise import fields, models


class TaskResult(models.Model):
    """ORM model representing the result of a task."""
    task_id = fields.TextField(pk=True)
    task_name = fields.TextField()
    parameters = fields.JSONField()
    result = fields.TextField(null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)
    state = fields.TextField()
    client_address = fields.TextField()
