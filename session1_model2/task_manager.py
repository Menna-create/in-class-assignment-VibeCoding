"""
Task Manager module for Task Management API.

This module contains the business logic for task operations.
"""

from typing import List, Optional
from models import Task, TaskStatus, TaskPriority, validate_task_data
from storage import Storage


class TaskManager:
    """
    Business logic layer for task management operations.

    Handles CRUD operations, filtering, and business rules for tasks.
    """

    def __init__(self, storage: Storage):
        """
        Initialize TaskManager with storage implementation.

        Args:
            storage: Storage implementation for persistence
        """
        self.storage = storage

    def create_task(self, title: str, description: Optional[str] = None,
                   status: str = 'pending', priority: str = 'medium') -> Task:
        """
        Create a new task.

        Args:
            title: Title of the task (required)
            description: Optional description of the task
            status: Initial status of the task
            priority: Priority level of the task

        Returns:
            Created Task object

        Raises:
            ValueError: If input validation fails
        """
        # Validate input data
        task_data = {
            'title': title,
            'description': description,
            'status': status,
            'priority': priority
        }
        errors = validate_task_data(task_data)
        if errors:
            raise ValueError(f"Validation error: {'; '.join(errors)}")

        # Create task with enums
        try:
            task_status = TaskStatus(status)
            task_priority = TaskPriority(priority)
        except ValueError as e:
            raise ValueError(f"Invalid enum value: {str(e)}")

        task = Task(
            title=title,
            description=description,
            status=task_status,
            priority=task_priority
        )

        # Validate and save task
        self.storage.save(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID.

        Args:
            task_id: UUID of the task

        Returns:
            Task object if found, None otherwise
        """
        return self.storage.get_by_id(task_id)

    def get_all_tasks(self, status_filter: Optional[str] = None,
                     priority_filter: Optional[str] = None) -> List[Task]:
        """
        Get all tasks with optional filtering.

        Args:
            status_filter: Optional filter by task status
            priority_filter: Optional filter by task priority

        Returns:
            List of Task objects

        Raises:
            ValueError: If filter values are invalid
        """
        # Validate filter values
        if status_filter and status_filter not in [s.value for s in TaskStatus]:
            raise ValueError(f"Invalid status filter: {status_filter}")

        if priority_filter and priority_filter not in [p.value for p in TaskPriority]:
            raise ValueError(f"Invalid priority filter: {priority_filter}")

        tasks = self.storage.get_all()

        # Apply filters
        if status_filter:
            status_enum = TaskStatus(status_filter)
            tasks = [task for task in tasks if task.status == status_enum]

        if priority_filter:
            priority_enum = TaskPriority(priority_filter)
            tasks = [task for task in tasks if task.priority == priority_enum]

        return tasks

    def update_task(self, task_id: str, updates: dict) -> Task:
        """
        Update an existing task.

        Args:
            task_id: UUID of the task to update
            updates: Dictionary of fields to update

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found or validation fails
        """
        # Get existing task
        task = self.storage.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        # Validate update data
        errors = validate_task_data(updates, partial=True)
        if errors:
            raise ValueError(f"Validation error: {'; '.join(errors)}")

        # Apply updates
        if 'title' in updates:
            task.title = updates['title']

        if 'description' in updates:
            task.description = updates['description']

        if 'status' in updates:
            try:
                task.status = TaskStatus(updates['status'])
            except ValueError:
                raise ValueError(f"Invalid status: {updates['status']}")

        if 'priority' in updates:
            try:
                task.priority = TaskPriority(updates['priority'])
            except ValueError:
                raise ValueError(f"Invalid priority: {updates['priority']}")

        # Validate updated task
        validation_errors = task.validate()
        if validation_errors:
            raise ValueError(f"Validation error: {'; '.join(validation_errors)}")

        # Save updated task
        self.storage.save(task)
        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: UUID of the task to delete

        Returns:
            True if task was deleted, False if task was not found
        """
        return self.storage.delete(task_id)

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            Total number of tasks in storage
        """
        return len(self.storage.get_all())

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Get tasks filtered by status.

        Args:
            status: Status to filter by

        Returns:
            List of Task objects with specified status

        Raises:
            ValueError: If status is invalid
        """
        return self.get_all_tasks(status_filter=status)

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """
        Get tasks filtered by priority.

        Args:
            priority: Priority to filter by

        Returns:
            List of Task objects with specified priority

        Raises:
            ValueError: If priority is invalid
        """
        return self.get_all_tasks(priority_filter=priority)