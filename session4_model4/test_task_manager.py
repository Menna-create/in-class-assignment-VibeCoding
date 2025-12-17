"""
Test suite for Task Management API - Test-Driven Development (TDD) approach.

This file was written BEFORE any implementation code, following TDD principles:
1. Write tests first (Red)
2. Write minimal code to pass (Green)
3. Refactor while keeping tests green (Refactor)
"""

import pytest
import json
import tempfile
import os
from datetime import datetime


# ============================================================================
# PHASE 2: MODEL LAYER TESTS (Write these BEFORE implementing models.py)
# ============================================================================

class TestTaskModel:
    """Test the Task model and validation - Written FIRST before models.py exists."""

    def test_task_creation_with_defaults(self):
        """Test creating a task with minimal data (just title)."""
        from models import Task, TaskStatus, TaskPriority

        task = Task(title='Buy milk')

        assert task.title == 'Buy milk'
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM
        assert task.id is not None
        assert len(task.id) > 0
        assert task.created_at is not None

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields specified."""
        from models import Task, TaskStatus, TaskPriority

        task = Task(
            title='Complete project',
            description='Finish the TDD implementation',
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH
        )

        assert task.title == 'Complete project'
        assert task.description == 'Finish the TDD implementation'
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.priority == TaskPriority.HIGH
        assert task.id is not None
        assert task.created_at is not None

    def test_task_validation_empty_title(self):
        """Test that validation catches empty title."""
        from models import Task

        task = Task(title='')
        errors = task.validate()

        assert len(errors) > 0
        assert any('Title is required' in error for error in errors)

    def test_task_validation_title_too_long(self):
        """Test that validation catches title exceeding 200 characters."""
        from models import Task

        long_title = 'x' * 201
        task = Task(title=long_title)
        errors = task.validate()

        assert len(errors) > 0
        assert any('200 characters' in error for error in errors)

    def test_task_validation_description_too_long(self):
        """Test that validation catches description exceeding 1000 characters."""
        from models import Task

        long_description = 'x' * 1001
        task = Task(title='Valid title', description=long_description)
        errors = task.validate()

        assert len(errors) > 0
        assert any('1000 characters' in error for error in errors)

    def test_task_serialization_to_dict(self):
        """Test that task can be converted to dictionary."""
        from models import Task, TaskStatus, TaskPriority

        task = Task(
            title='Test Task',
            description='Test Description',
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH
        )

        task_dict = task.to_dict()

        assert task_dict['title'] == 'Test Task'
        assert task_dict['description'] == 'Test Description'
        assert task_dict['status'] == 'pending'
        assert task_dict['priority'] == 'high'
        assert 'id' in task_dict
        assert 'created_at' in task_dict
        assert isinstance(task_dict['created_at'], str)

    def test_task_deserialization_from_dict(self):
        """Test that task can be created from dictionary."""
        from models import Task, TaskStatus, TaskPriority

        task_dict = {
            'id': 'test-id-123',
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'in-progress',
            'priority': 'low',
            'created_at': '2024-01-01T12:00:00'
        }

        task = Task.from_dict(task_dict)

        assert task.id == 'test-id-123'
        assert task.title == 'Test Task'
        assert task.description == 'Test Description'
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.priority == TaskPriority.LOW

    def test_task_status_enum(self):
        """Test that TaskStatus enum has correct values."""
        from models import TaskStatus

        assert TaskStatus.PENDING.value == 'pending'
        assert TaskStatus.IN_PROGRESS.value == 'in-progress'
        assert TaskStatus.COMPLETED.value == 'completed'

        # Test that we have exactly 3 statuses
        assert len(list(TaskStatus)) == 3

    def test_task_priority_enum(self):
        """Test that TaskPriority enum has correct values."""
        from models import TaskPriority

        assert TaskPriority.LOW.value == 'low'
        assert TaskPriority.MEDIUM.value == 'medium'
        assert TaskPriority.HIGH.value == 'high'

        # Test that we have exactly 3 priorities
        assert len(list(TaskPriority)) == 3


# ============================================================================
# PHASE 3: STORAGE LAYER TESTS (Write these BEFORE implementing storage.py)
# ============================================================================

@pytest.fixture
def temp_storage_file():
    """Create temporary JSON file for testing."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def storage(temp_storage_file):
    """Create JSONStorage instance."""
    from storage import JSONStorage
    return JSONStorage(temp_storage_file)


class TestStorage:
    """Test the storage layer - Written FIRST before storage.py exists."""

    def test_save_task_to_storage(self, storage):
        """Test that we can save a task to storage."""
        from models import Task

        task = Task(title='Test Task', description='Test Description')
        storage.save(task)

        # Verify task was saved
        retrieved = storage.get_by_id(task.id)
        assert retrieved is not None
        assert retrieved.title == 'Test Task'
        assert retrieved.description == 'Test Description'

    def test_retrieve_task_by_id(self, storage):
        """Test that we can retrieve a specific task by ID."""
        from models import Task

        task = Task(title='Find Me')
        storage.save(task)

        retrieved = storage.get_by_id(task.id)

        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.title == 'Find Me'

    def test_retrieve_all_tasks(self, storage):
        """Test that we can retrieve all tasks."""
        from models import Task

        task1 = Task(title='Task 1')
        task2 = Task(title='Task 2')
        task3 = Task(title='Task 3')

        storage.save(task1)
        storage.save(task2)
        storage.save(task3)

        all_tasks = storage.get_all()

        assert len(all_tasks) == 3
        titles = [task.title for task in all_tasks]
        assert 'Task 1' in titles
        assert 'Task 2' in titles
        assert 'Task 3' in titles

    def test_update_existing_task(self, storage):
        """Test that we can update an existing task in storage."""
        from models import Task

        task = Task(title='Original Title')
        storage.save(task)

        # Modify and save again
        task.title = 'Updated Title'
        storage.save(task)

        retrieved = storage.get_by_id(task.id)
        assert retrieved.title == 'Updated Title'

    def test_delete_task(self, storage):
        """Test that we can delete a task from storage."""
        from models import Task

        task = Task(title='Delete Me')
        storage.save(task)

        # Verify it exists
        assert storage.get_by_id(task.id) is not None

        # Delete it
        result = storage.delete(task.id)
        assert result is True

        # Verify it's gone
        assert storage.get_by_id(task.id) is None

    def test_delete_nonexistent_task_returns_false(self, storage):
        """Test that deleting a non-existent task returns False."""
        result = storage.delete('non-existent-id-12345')
        assert result is False

    def test_storage_persists_to_file(self, temp_storage_file):
        """Test that data persists when storage object is destroyed."""
        from models import Task
        from storage import JSONStorage

        # Create storage and save task
        storage1 = JSONStorage(temp_storage_file)
        task = Task(title='Persistent Task')
        storage1.save(task)
        task_id = task.id

        # Destroy storage object and create new one
        del storage1
        storage2 = JSONStorage(temp_storage_file)

        # Verify task still exists
        retrieved = storage2.get_by_id(task_id)
        assert retrieved is not None
        assert retrieved.title == 'Persistent Task'

    def test_storage_handles_missing_file(self, temp_storage_file):
        """Test that storage creates file if it doesn't exist."""
        from storage import JSONStorage

        # Delete the file
        if os.path.exists(temp_storage_file):
            os.unlink(temp_storage_file)

        # Create storage - should not raise error
        storage = JSONStorage(temp_storage_file)

        # Should return empty list
        tasks = storage.get_all()
        assert tasks == []

    def test_storage_handles_corrupted_file(self, temp_storage_file):
        """Test that storage recovers from corrupted JSON file."""
        from storage import JSONStorage

        # Write corrupted JSON
        with open(temp_storage_file, 'w') as f:
            f.write('{ this is not valid json }')

        # Should not crash, should recover gracefully
        storage = JSONStorage(temp_storage_file)
        tasks = storage.get_all()

        # Should return empty list after recovery
        assert tasks == []


# ============================================================================
# PHASE 4: BUSINESS LOGIC TESTS (Write these BEFORE implementing task_manager.py)
# ============================================================================

@pytest.fixture
def task_manager(storage):
    """Create TaskManager with test storage."""
    from task_manager import TaskManager
    return TaskManager(storage)


@pytest.fixture
def sample_tasks(task_manager):
    """Create sample tasks for testing."""
    task1 = task_manager.create_task(
        title='Task 1',
        description='First task',
        status='pending',
        priority='high'
    )
    task2 = task_manager.create_task(
        title='Task 2',
        description='Second task',
        status='completed',
        priority='low'
    )
    return [task1, task2]


class TestTaskManager:
    """Test the business logic layer - Written FIRST before task_manager.py exists."""

    def test_create_task_with_valid_data(self, task_manager):
        """Test creating a task with valid data."""
        task = task_manager.create_task(
            title='New Task',
            description='Task description',
            status='pending',
            priority='medium'
        )

        assert task is not None
        assert task.title == 'New Task'
        assert task.description == 'Task description'
        assert task.id is not None

    def test_create_task_validates_input(self, task_manager):
        """Test that create_task validates input and rejects invalid data."""
        with pytest.raises(ValueError):
            task_manager.create_task(title='')  # Empty title should fail

    def test_get_task_by_id(self, task_manager):
        """Test retrieving a specific task by ID."""
        created = task_manager.create_task(title='Find Me')

        retrieved = task_manager.get_task(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == 'Find Me'

    def test_get_task_nonexistent_returns_none(self, task_manager):
        """Test that getting a non-existent task returns None."""
        result = task_manager.get_task('non-existent-id')
        assert result is None

    def test_get_all_tasks_empty(self, task_manager):
        """Test getting all tasks when there are none."""
        tasks = task_manager.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_multiple(self, task_manager, sample_tasks):
        """Test getting all tasks when multiple exist."""
        tasks = task_manager.get_all_tasks()

        assert len(tasks) == 2
        titles = [task.title for task in tasks]
        assert 'Task 1' in titles
        assert 'Task 2' in titles

    def test_filter_tasks_by_status(self, task_manager, sample_tasks):
        """Test filtering tasks by status."""
        pending_tasks = task_manager.get_all_tasks(status_filter='pending')
        completed_tasks = task_manager.get_all_tasks(status_filter='completed')

        assert len(pending_tasks) == 1
        assert pending_tasks[0].title == 'Task 1'

        assert len(completed_tasks) == 1
        assert completed_tasks[0].title == 'Task 2'

    def test_filter_tasks_by_priority(self, task_manager, sample_tasks):
        """Test filtering tasks by priority."""
        high_tasks = task_manager.get_all_tasks(priority_filter='high')
        low_tasks = task_manager.get_all_tasks(priority_filter='low')

        assert len(high_tasks) == 1
        assert high_tasks[0].title == 'Task 1'

        assert len(low_tasks) == 1
        assert low_tasks[0].title == 'Task 2'

    def test_filter_tasks_by_status_and_priority(self, task_manager):
        """Test filtering tasks by both status and priority."""
        # Create tasks with specific combinations
        task_manager.create_task(title='Task A', status='pending', priority='high')
        task_manager.create_task(title='Task B', status='pending', priority='low')
        task_manager.create_task(title='Task C', status='completed', priority='high')

        # Filter by both
        tasks = task_manager.get_all_tasks(
            status_filter='pending',
            priority_filter='high'
        )

        assert len(tasks) == 1
        assert tasks[0].title == 'Task A'

    def test_update_task_title(self, task_manager):
        """Test updating a task's title."""
        task = task_manager.create_task(title='Original Title')

        updated = task_manager.update_task(task.id, {'title': 'New Title'})

        assert updated.title == 'New Title'
        assert updated.id == task.id

    def test_update_task_status(self, task_manager):
        """Test updating a task's status."""
        from models import TaskStatus

        task = task_manager.create_task(title='Task', status='pending')

        updated = task_manager.update_task(task.id, {'status': 'completed'})

        assert updated.status == TaskStatus.COMPLETED

    def test_update_task_validates_input(self, task_manager):
        """Test that update_task validates input."""
        task = task_manager.create_task(title='Task')

        # Try to update with invalid status
        with pytest.raises(ValueError):
            task_manager.update_task(task.id, {'status': 'invalid-status'})

    def test_update_nonexistent_task_raises_error(self, task_manager):
        """Test that updating a non-existent task raises an error."""
        with pytest.raises(ValueError):
            task_manager.update_task('non-existent-id', {'title': 'New Title'})

    def test_delete_task_existing(self, task_manager):
        """Test deleting an existing task."""
        task = task_manager.create_task(title='Delete Me')

        result = task_manager.delete_task(task.id)

        assert result is True
        assert task_manager.get_task(task.id) is None

    def test_delete_task_nonexistent_returns_false(self, task_manager):
        """Test that deleting a non-existent task returns False."""
        result = task_manager.delete_task('non-existent-id')
        assert result is False

    def test_get_task_count(self, task_manager, sample_tasks):
        """Test getting the total task count."""
        count = task_manager.get_task_count()
        assert count == 2


# ============================================================================
# PHASE 5: API LAYER TESTS (Write these BEFORE implementing app.py)
# ============================================================================

@pytest.fixture
def client(temp_storage_file):
    """Create Flask test client."""
    # Import here to avoid issues before app.py exists
    from app import create_app

    app = create_app(storage_path=temp_storage_file)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_task_via_api(client):
    """Create a task via API for testing."""
    response = client.post('/api/tasks',
                          json={'title': 'API Test Task', 'description': 'Created via API'},
                          content_type='application/json')
    return json.loads(response.data)


class TestAPI:
    """Test the API endpoints - Written FIRST before app.py exists."""

    def test_health_check_endpoint(self, client):
        """Test that health check endpoint returns 200."""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

    def test_create_task_endpoint(self, client):
        """Test creating a task via POST /api/tasks."""
        task_data = {
            'title': 'API Task',
            'description': 'Task created via API',
            'status': 'pending',
            'priority': 'high'
        }

        response = client.post('/api/tasks',
                              json=task_data,
                              content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'API Task'
        assert data['description'] == 'Task created via API'
        assert data['status'] == 'pending'
        assert data['priority'] == 'high'
        assert 'id' in data
        assert 'created_at' in data

    def test_create_task_missing_title_returns_400(self, client):
        """Test that creating a task without title returns 400."""
        task_data = {'description': 'No title'}

        response = client.post('/api/tasks',
                              json=task_data,
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_all_tasks_endpoint(self, client):
        """Test getting all tasks via GET /api/tasks."""
        # Create some tasks first
        client.post('/api/tasks', json={'title': 'Task 1'})
        client.post('/api/tasks', json={'title': 'Task 2'})

        response = client.get('/api/tasks')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tasks' in data
        assert 'count' in data
        assert data['count'] == 2
        assert len(data['tasks']) == 2

    def test_get_all_tasks_with_status_filter(self, client):
        """Test filtering tasks by status."""
        client.post('/api/tasks', json={'title': 'Task 1', 'status': 'pending'})
        client.post('/api/tasks', json={'title': 'Task 2', 'status': 'completed'})

        response = client.get('/api/tasks?status=pending')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['tasks'][0]['status'] == 'pending'

    def test_get_all_tasks_with_priority_filter(self, client):
        """Test filtering tasks by priority."""
        client.post('/api/tasks', json={'title': 'Task 1', 'priority': 'high'})
        client.post('/api/tasks', json={'title': 'Task 2', 'priority': 'low'})

        response = client.get('/api/tasks?priority=high')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['tasks'][0]['priority'] == 'high'

    def test_get_all_tasks_with_invalid_filter_returns_400(self, client):
        """Test that invalid filter returns 400."""
        response = client.get('/api/tasks?status=invalid-status')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_single_task_endpoint(self, client, sample_task_via_api):
        """Test getting a single task via GET /api/tasks/{id}."""
        task_id = sample_task_via_api['id']

        response = client.get(f'/api/tasks/{task_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == 'API Test Task'

    def test_get_nonexistent_task_returns_404(self, client):
        """Test that getting a non-existent task returns 404."""
        response = client.get('/api/tasks/non-existent-id-12345')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_task_endpoint(self, client, sample_task_via_api):
        """Test updating a task via PUT /api/tasks/{id}."""
        task_id = sample_task_via_api['id']
        update_data = {
            'title': 'Updated Title',
            'status': 'completed'
        }

        response = client.put(f'/api/tasks/{task_id}',
                             json=update_data,
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
        assert data['status'] == 'completed'

    def test_update_task_partial_update(self, client, sample_task_via_api):
        """Test that partial updates work (only updating one field)."""
        task_id = sample_task_via_api['id']

        response = client.put(f'/api/tasks/{task_id}',
                             json={'status': 'in-progress'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'in-progress'
        assert data['title'] == 'API Test Task'  # Original title preserved

    def test_update_nonexistent_task_returns_404(self, client):
        """Test that updating a non-existent task returns 404."""
        response = client.put('/api/tasks/non-existent-id',
                             json={'title': 'New Title'},
                             content_type='application/json')

        assert response.status_code == 404

    def test_delete_task_endpoint(self, client, sample_task_via_api):
        """Test deleting a task via DELETE /api/tasks/{id}."""
        task_id = sample_task_via_api['id']

        response = client.delete(f'/api/tasks/{task_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data

        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404

    def test_delete_nonexistent_task_returns_404(self, client):
        """Test that deleting a non-existent task returns 404."""
        response = client.delete('/api/tasks/non-existent-id')

        assert response.status_code == 404

    def test_response_format_consistency(self, client):
        """Test that all responses follow consistent format."""
        # Create task
        response = client.post('/api/tasks', json={'title': 'Test'})
        data = json.loads(response.data)
        assert isinstance(data, dict)

        # Get all tasks
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert 'tasks' in data
        assert 'count' in data

        # Error response
        response = client.get('/api/tasks/invalid')
        data = json.loads(response.data)
        assert 'error' in data


# ============================================================================
# PHASE 6: INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_task_lifecycle(self, client):
        """Test complete CRUD lifecycle: Create → Read → Update → Delete."""
        # Create
        create_response = client.post('/api/tasks',
                                     json={'title': 'Lifecycle Task', 'priority': 'high'})
        assert create_response.status_code == 201
        task_data = json.loads(create_response.data)
        task_id = task_data['id']

        # Read
        read_response = client.get(f'/api/tasks/{task_id}')
        assert read_response.status_code == 200
        read_data = json.loads(read_response.data)
        assert read_data['title'] == 'Lifecycle Task'

        # Update
        update_response = client.put(f'/api/tasks/{task_id}',
                                     json={'status': 'completed'})
        assert update_response.status_code == 200
        update_data = json.loads(update_response.data)
        assert update_data['status'] == 'completed'

        # Delete
        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 200

        # Verify deletion
        verify_response = client.get(f'/api/tasks/{task_id}')
        assert verify_response.status_code == 404

    def test_bulk_task_creation(self, client):
        """Test creating multiple tasks and retrieving them."""
        # Create 10 tasks
        for i in range(10):
            response = client.post('/api/tasks',
                                  json={'title': f'Bulk Task {i}', 'priority': 'medium'})
            assert response.status_code == 201

        # Retrieve all
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert data['count'] == 10

    def test_data_persistence_across_restarts(self, temp_storage_file):
        """Test that data persists across app restarts."""
        from app import create_app

        # Create app and add task
        app1 = create_app(storage_path=temp_storage_file)
        with app1.test_client() as client1:
            response = client1.post('/api/tasks',
                                   json={'title': 'Persistent Task'})
            task_data = json.loads(response.data)
            task_id = task_data['id']

        # Destroy app and create new one
        del app1
        app2 = create_app(storage_path=temp_storage_file)
        with app2.test_client() as client2:
            response = client2.get(f'/api/tasks/{task_id}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['title'] == 'Persistent Task'

    def test_error_recovery(self, client):
        """Test that app recovers gracefully from errors."""
        # Try to create invalid task
        response = client.post('/api/tasks', json={})
        assert response.status_code == 400

        # Verify app still works after error
        response = client.post('/api/tasks', json={'title': 'Valid Task'})
        assert response.status_code == 201

    def test_filter_combination_scenarios(self, client):
        """Test various filter combinations."""
        # Create tasks with different combinations
        tasks_data = [
            {'title': 'Task 1', 'status': 'pending', 'priority': 'high'},
            {'title': 'Task 2', 'status': 'pending', 'priority': 'low'},
            {'title': 'Task 3', 'status': 'completed', 'priority': 'high'},
            {'title': 'Task 4', 'status': 'completed', 'priority': 'low'},
        ]

        for task_data in tasks_data:
            client.post('/api/tasks', json=task_data)

        # Test various filter combinations
        response = client.get('/api/tasks?status=pending')
        assert json.loads(response.data)['count'] == 2

        response = client.get('/api/tasks?priority=high')
        assert json.loads(response.data)['count'] == 2

        response = client.get('/api/tasks?status=pending&priority=high')
        assert json.loads(response.data)['count'] == 1
