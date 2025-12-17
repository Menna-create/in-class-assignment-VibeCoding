"""
Test suite for Task Management API.

This module contains comprehensive tests for all API endpoints and business logic.
"""

import pytest
import json
import tempfile
import os
from app import app
from storage import JSONStorage
from task_manager import TaskManager
from models import Task, TaskStatus, TaskPriority


@pytest.fixture
def temp_file():
    """Create a temporary file for JSON storage."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    os.unlink(path)


@pytest.fixture
def test_storage(temp_file):
    """Create a JSONStorage instance with temporary file."""
    return JSONStorage(temp_file)


@pytest.fixture
def test_manager(test_storage):
    """Create a TaskManager instance with test storage."""
    return TaskManager(test_storage)


@pytest.fixture
def client():
    """Create a test client for Flask app."""
    app.config['TESTING'] = True

    # Create temporary storage file for testing
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(fd)

    # Override the storage path in app
    import app as app_module
    original_path = app_module.storage_path
    app_module.storage_path = temp_path

    with app.test_client() as client:
        yield client

    # Cleanup
    app_module.storage_path = original_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_task(client):
    """Create a sample task for testing."""
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'status': 'pending',
        'priority': 'medium'
    }
    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    return json.loads(response.data)


class TestTaskModel:
    """Test the Task model and validation."""

    def test_task_creation(self):
        """Test creating a valid task."""
        task = Task(
            title='Test Task',
            description='Test Description',
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM
        )
        assert task.title == 'Test Task'
        assert task.description == 'Test Description'
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM
        assert len(task.id) > 0  # UUID should be generated

    def test_task_validation(self):
        """Test task validation."""
        # Valid task
        task = Task(title='Valid Task')
        errors = task.validate()
        assert len(errors) == 0

        # Invalid task (empty title)
        task = Task(title='')
        errors = task.validate()
        assert len(errors) > 0
        assert 'Title is required' in errors

        # Invalid task (title too long)
        task = Task(title='x' * 201)
        errors = task.validate()
        assert len(errors) > 0
        assert 'Title must be less than 200 characters' in errors

    def test_task_serialization(self):
        """Test task to_dict serialization."""
        task = Task(
            title='Test Task',
            description='Test Description',
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM
        )
        task_dict = task.to_dict()
        assert task_dict['title'] == 'Test Task'
        assert task_dict['description'] == 'Test Description'
        assert task_dict['status'] == 'pending'
        assert task_dict['priority'] == 'medium'
        assert 'id' in task_dict
        assert 'created_at' in task_dict

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        task_dict = {
            'id': 'test-id',
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'pending',
            'priority': 'medium',
            'created_at': '2024-01-01T00:00:00'
        }
        task = Task.from_dict(task_dict)
        assert task.id == 'test-id'
        assert task.title == 'Test Task'
        assert task.description == 'Test Description'
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM


class TestStorage:
    """Test the storage layer."""

    def test_save_and_get_task(self, test_storage):
        """Test saving and retrieving a task."""
        task = Task(title='Test Task', description='Test Description')
        test_storage.save(task)

        retrieved = test_storage.get_by_id(task.id)
        assert retrieved is not None
        assert retrieved.title == 'Test Task'
        assert retrieved.description == 'Test Description'

    def test_get_all_tasks(self, test_storage):
        """Test retrieving all tasks."""
        task1 = Task(title='Task 1')
        task2 = Task(title='Task 2')
        test_storage.save(task1)
        test_storage.save(task2)

        all_tasks = test_storage.get_all()
        assert len(all_tasks) == 2
        assert all_tasks[0].title == 'Task 1'
        assert all_tasks[1].title == 'Task 2'

    def test_delete_task(self, test_storage):
        """Test deleting a task."""
        task = Task(title='Test Task')
        test_storage.save(task)

        deleted = test_storage.delete(task.id)
        assert deleted is True

        retrieved = test_storage.get_by_id(task.id)
        assert retrieved is None

    def test_delete_nonexistent_task(self, test_storage):
        """Test deleting a non-existent task."""
        deleted = test_storage.delete('non-existent-id')
        assert deleted is False


class TestTaskManager:
    """Test the business logic layer."""

    def test_create_task(self, test_manager):
        """Test creating a task through TaskManager."""
        task = test_manager.create_task(
            title='New Task',
            description='New Description',
            status='pending',
            priority='high'
        )
        assert task.title == 'New Task'
        assert task.description == 'New Description'
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.HIGH

    def test_get_task(self, test_manager):
        """Test getting a task through TaskManager."""
        created = test_manager.create_task(title='Test Task')
        retrieved = test_manager.get_task(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == 'Test Task'

    def test_update_task(self, test_manager):
        """Test updating a task through TaskManager."""
        task = test_manager.create_task(title='Original Title')
        updated = test_manager.update_task(task.id, {'title': 'Updated Title'})
        assert updated.title == 'Updated Title'

    def test_delete_task(self, test_manager):
        """Test deleting a task through TaskManager."""
        task = test_manager.create_task(title='Test Task')
        deleted = test_manager.delete_task(task.id)
        assert deleted is True

        retrieved = test_manager.get_task(task.id)
        assert retrieved is None

    def test_filter_tasks_by_status(self, test_manager):
        """Test filtering tasks by status."""
        task1 = test_manager.create_task(title='Task 1', status='pending')
        task2 = test_manager.create_task(title='Task 2', status='completed')

        pending_tasks = test_manager.get_all_tasks(status_filter='pending')
        completed_tasks = test_manager.get_all_tasks(status_filter='completed')

        assert len(pending_tasks) == 1
        assert pending_tasks[0].id == task1.id
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task2.id

    def test_filter_tasks_by_priority(self, test_manager):
        """Test filtering tasks by priority."""
        task1 = test_manager.create_task(title='Task 1', priority='low')
        task2 = test_manager.create_task(title='Task 2', priority='high')

        low_tasks = test_manager.get_all_tasks(priority_filter='low')
        high_tasks = test_manager.get_all_tasks(priority_filter='high')

        assert len(low_tasks) == 1
        assert low_tasks[0].id == task1.id
        assert len(high_tasks) == 1
        assert high_tasks[0].id == task2.id


class TestTaskManagementAPI:
    """Test the API endpoints."""

    # Test 1: Create a new task
    def test_create_task(self, client):
        """Test creating a new task via API."""
        task_data = {
            'title': 'Complete project documentation',
            'description': 'Write comprehensive documentation for the API',
            'status': 'pending',
            'priority': 'high'
        }

        response = client.post('/api/tasks',
                              data=json.dumps(task_data),
                              content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == task_data['title']
        assert data['description'] == task_data['description']
        assert data['status'] == task_data['status']
        assert data['priority'] == task_data['priority']
        assert 'id' in data
        assert 'created_at' in data

    # Test 2: Get all tasks with filters
    def test_get_all_tasks_with_filters(self, client):
        """Test retrieving tasks with status and priority filters."""
        # Create test tasks
        task1 = {
            'title': 'Task 1',
            'status': 'pending',
            'priority': 'high'
        }
        task2 = {
            'title': 'Task 2',
            'status': 'completed',
            'priority': 'low'
        }
        client.post('/api/tasks', data=json.dumps(task1), content_type='application/json')
        client.post('/api/tasks', data=json.dumps(task2), content_type='application/json')

        # Test status filter
        response = client.get('/api/tasks?status=pending')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['tasks'][0]['status'] == 'pending'

        # Test priority filter
        response = client.get('/api/tasks?priority=low')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['tasks'][0]['priority'] == 'low'

    # Test 3: Update task
    def test_update_task(self, client, sample_task):
        """Test updating an existing task."""
        update_data = {
            'title': 'Updated Task Title',
            'status': 'completed'
        }

        response = client.put(f'/api/tasks/{sample_task["id"]}',
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['status'] == update_data['status']

    # Test 4: Delete task
    def test_delete_task(self, client, sample_task):
        """Test deleting a task."""
        response = client.delete(f'/api/tasks/{sample_task["id"]}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data

        # Verify task is deleted
        response = client.get(f'/api/tasks/{sample_task["id"]}')
        assert response.status_code == 404

    # Test 5: Error handling (invalid input)
    def test_error_handling(self, client):
        """Test error handling for invalid input."""
        # Test creating task with missing title
        invalid_task = {
            'description': 'Task without title'
        }
        response = client.post('/api/tasks',
                              data=json.dumps(invalid_task),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation failed' in data['error']

        # Test getting non-existent task
        response = client.get('/api/tasks/non-existent-id')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Task not found' in data['error']

        # Test invalid status filter
        response = client.get('/api/tasks?status=invalid')
        assert response.status_code == 400

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'service' in data