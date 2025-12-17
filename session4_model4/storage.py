"""
Storage module for Task Management API - TDD Implementation.

This module was implemented AFTER writing tests in test_task_manager.py,
following the Test-Driven Development (TDD) approach.
"""

import json
import os
import threading
from abc import ABC, abstractmethod
from typing import List, Optional
from models import Task


class Storage(ABC):
    """
    Abstract base class defining the storage interface.

    This interface ensures that different storage implementations
    can be swapped without affecting the business logic.
    """

    @abstractmethod
    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List of all Task objects
        """
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: Unique identifier of the task

        Returns:
            Task object if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """
        Save a task to storage (create or update).

        Args:
            task: Task object to save
        """
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """
        Delete a task from storage.

        Args:
            task_id: Unique identifier of the task to delete

        Returns:
            True if task was deleted, False if task was not found
        """
        pass


class JSONStorage(Storage):
    """
    JSON file-based storage implementation.

    Stores tasks in a JSON file with thread-safe operations.
    """

    def __init__(self, filepath: str):
        """
        Initialize JSON storage with filepath.

        Args:
            filepath: Path to the JSON file for storage
        """
        self.filepath = filepath
        self._lock = threading.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Ensure the storage file exists, create if it doesn't.
        """
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _load(self) -> List[Task]:
        """
        Load tasks from JSON file.

        Returns:
            List of Task objects

        Handles corrupted files gracefully by returning empty list.
        """
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task_dict) for task_dict in data]
        except (json.JSONDecodeError, FileNotFoundError, ValueError):
            # If file is corrupted or doesn't exist, return empty list
            # and overwrite with empty array
            with open(self.filepath, 'w') as f:
                json.dump([], f)
            return []

    def _save(self, tasks: List[Task]) -> None:
        """
        Save tasks to JSON file.

        Args:
            tasks: List of Task objects to save

        Uses atomic write operation (write to temp file, then rename).
        """
        # Convert tasks to dictionaries
        data = [task.to_dict() for task in tasks]

        # Atomic write: write to temp file, then rename
        temp_filepath = self.filepath + '.tmp'
        with open(temp_filepath, 'w') as f:
            json.dump(data, f, indent=2)

        # Atomic rename
        os.replace(temp_filepath, self.filepath)

    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List of all Task objects
        """
        with self._lock:
            return self._load()

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: Unique identifier of the task

        Returns:
            Task object if found, None otherwise
        """
        with self._lock:
            tasks = self._load()
            for task in tasks:
                if task.id == task_id:
                    return task
            return None

    def save(self, task: Task) -> None:
        """
        Save a task to storage (create or update).

        If a task with the same ID exists, it will be updated.
        Otherwise, a new task will be added.

        Args:
            task: Task object to save
        """
        with self._lock:
            tasks = self._load()

            # Check if task already exists (update case)
            task_exists = False
            for i, existing_task in enumerate(tasks):
                if existing_task.id == task.id:
                    tasks[i] = task
                    task_exists = True
                    break

            # If task doesn't exist, add it (create case)
            if not task_exists:
                tasks.append(task)

            self._save(tasks)

    def delete(self, task_id: str) -> bool:
        """
        Delete a task from storage.

        Args:
            task_id: Unique identifier of the task to delete

        Returns:
            True if task was deleted, False if task was not found
        """
        with self._lock:
            tasks = self._load()
            initial_count = len(tasks)

            # Filter out the task with matching ID
            tasks = [task for task in tasks if task.id != task_id]

            # Save and return whether a task was actually deleted
            if len(tasks) < initial_count:
                self._save(tasks)
                return True
            return False
