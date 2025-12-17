"""
Storage module for Task Management API.

This module defines the storage abstraction and JSON file-based implementation.
"""

import json
import os
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from models import Task


class Storage(ABC):
    """Abstract base class for storage implementations."""

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Retrieve all tasks from storage."""
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a specific task by ID."""
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """Save a task to storage (create or update)."""
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete a task by ID."""
        pass


class JSONStorage(Storage):
    """JSON file-based storage implementation with thread safety."""

    def __init__(self, filepath: str):
        """
        Initialize JSON storage with file path.

        Args:
            filepath: Path to the JSON storage file
        """
        self.filepath = filepath
        self._lock = threading.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensure the storage file exists and is properly initialized."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _load(self) -> List[Dict]:
        """
        Load tasks from JSON file.

        Returns:
            List of task dictionaries

        Raises:
            IOError: If file cannot be read
            json.JSONDecodeError: If file contains invalid JSON
        """
        with self._lock:
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                # If file doesn't exist or is corrupted, return empty list
                return []

    def _save(self, data: List[Dict]) -> None:
        """
        Save tasks to JSON file atomically.

        Args:
            data: List of task dictionaries to save

        Raises:
            IOError: If file cannot be written
        """
        with self._lock:
            # Write to temporary file first, then rename for atomic operation
            temp_filepath = f"{self.filepath}.tmp"
            try:
                with open(temp_filepath, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                # Atomic rename
                os.replace(temp_filepath, self.filepath)
            except Exception:
                # Clean up temp file if it exists
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
                raise

    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List of Task objects
        """
        try:
            data = self._load()
            tasks = []
            for task_data in data:
                try:
                    task = Task.from_dict(task_data)
                    tasks.append(task)
                except ValueError:
                    # Skip invalid task entries
                    continue
            return tasks
        except Exception as e:
            raise IOError(f"Failed to load tasks: {str(e)}")

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: UUID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        try:
            data = self._load()
            for task_data in data:
                if task_data.get('id') == task_id:
                    try:
                        return Task.from_dict(task_data)
                    except ValueError:
                        # Skip invalid task entry
                        continue
            return None
        except Exception as e:
            raise IOError(f"Failed to load task: {str(e)}")

    def save(self, task: Task) -> None:
        """
        Save a task to storage (create or update).

        Args:
            task: Task object to save

        Raises:
            ValueError: If task validation fails
            IOError: If save operation fails
        """
        # Validate task before saving
        errors = task.validate()
        if errors:
            raise ValueError(f"Invalid task data: {'; '.join(errors)}")

        try:
            data = self._load()
            task_dict = task.to_dict()

            # Find and update existing task or add new one
            found_index = None
            for i, existing_task in enumerate(data):
                if existing_task.get('id') == task.id:
                    found_index = i
                    break

            if found_index is not None:
                data[found_index] = task_dict
            else:
                data.append(task_dict)

            self._save(data)
        except Exception as e:
            raise IOError(f"Failed to save task: {str(e)}")

    def delete(self, task_id: str) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: UUID of the task to delete

        Returns:
            True if task was deleted, False if task was not found

        Raises:
            IOError: If delete operation fails
        """
        try:
            data = self._load()
            initial_length = len(data)

            # Filter out the task to delete
            data = [task for task in data if task.get('id') != task_id]

            if len(data) < initial_length:
                self._save(data)
                return True
            return False
        except Exception as e:
            raise IOError(f"Failed to delete task: {str(e)}")