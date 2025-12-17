"""
Models module for Task Management API - TDD Implementation.

This module was implemented AFTER writing tests in test_task_manager.py,
following the Test-Driven Development (TDD) approach.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import uuid


class TaskStatus(Enum):
    """Enum representing possible task statuses."""
    PENDING = 'pending'
    IN_PROGRESS = 'in-progress'
    COMPLETED = 'completed'


class TaskPriority(Enum):
    """Enum representing possible task priorities."""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


@dataclass
class Task:
    """
    Task model representing a task in the system.

    Attributes:
        id: Unique identifier for the task (UUID string)
        title: Title of the task (required, max 200 characters)
        description: Optional description of the task (max 1000 characters)
        status: Current status of the task
        priority: Priority level of the task
        created_at: Timestamp when the task was created
    """
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> list[str]:
        """
        Validate task data and return list of errors.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Title validation
        if not self.title:
            errors.append('Title is required')
        elif len(self.title) > 200:
            errors.append('Title must be less than 200 characters')

        # Description validation
        if self.description is not None and len(self.description) > 1000:
            errors.append('Description must be less than 1000 characters')

        return errors

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary representation.

        Returns:
            Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create task from dictionary representation.

        Args:
            data: Dictionary containing task data

        Returns:
            Task instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        try:
            # Handle status conversion
            status = TaskStatus.PENDING
            if 'status' in data and data['status']:
                status = TaskStatus(data['status'])

            # Handle priority conversion
            priority = TaskPriority.MEDIUM
            if 'priority' in data and data['priority']:
                priority = TaskPriority(data['priority'])

            # Handle created_at conversion
            created_at = datetime.utcnow()
            if 'created_at' in data and data['created_at']:
                created_at = datetime.fromisoformat(data['created_at'])

            return cls(
                id=data.get('id', str(uuid.uuid4())),
                title=data.get('title', ''),
                description=data.get('description'),
                status=status,
                priority=priority,
                created_at=created_at
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid task data: {str(e)}")


def validate_task_data(data: Dict[str, Any], partial: bool = False) -> list[str]:
    """
    Validate task data from request payload.

    Args:
        data: Dictionary containing task data
        partial: Whether this is a partial update (allows missing required fields)

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if not partial:
        if not data.get('title'):
            errors.append('Title is required')
        elif len(data.get('title', '')) > 200:
            errors.append('Title must be less than 200 characters')

    if 'status' in data and data['status'] not in [s.value for s in TaskStatus]:
        errors.append('Invalid status. Must be: pending, in-progress, or completed')

    if 'priority' in data and data['priority'] not in [p.value for p in TaskPriority]:
        errors.append('Invalid priority. Must be: low, medium, or high')

    if 'description' in data and data['description'] is not None and len(data['description']) > 1000:
        errors.append('Description must be less than 1000 characters')

    return errors
