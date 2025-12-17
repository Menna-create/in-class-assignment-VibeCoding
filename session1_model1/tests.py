import pytest
import json
from app import app, db, Task, TaskStatus, TaskPriority

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_task(client):
    """Create a sample task for testing"""
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

class TestTaskManagementAPI:

    # Test 1: Create a new task
    def test_create_task(self, client):
        """Test creating a new task"""
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

    # Test 2: Get all tasks
    def test_get_all_tasks(self, client, sample_task):
        """Test retrieving all tasks"""
        # Create another task
        task_data2 = {
            'title': 'Second Task',
            'description': 'Another test task',
            'status': 'in-progress',
            'priority': 'low'
        }
        client.post('/api/tasks',
                   data=json.dumps(task_data2),
                   content_type='application/json')

        response = client.get('/api/tasks')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 2
        assert data['count'] == 2

    # Test 3: Get task by ID
    def test_get_task_by_id(self, client, sample_task):
        """Test retrieving a specific task by ID"""
        task_id = sample_task['id']

        response = client.get(f'/api/tasks/{task_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == sample_task['title']

    # Test 4: Update task
    def test_update_task(self, client, sample_task):
        """Test updating an existing task"""
        task_id = sample_task['id']
        update_data = {
            'title': 'Updated Task Title',
            'description': 'Updated description',
            'status': 'completed',
            'priority': 'high'
        }

        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['description'] == update_data['description']
        assert data['status'] == update_data['status']
        assert data['priority'] == update_data['priority']

    # Test 5: Delete task
    def test_delete_task(self, client, sample_task):
        """Test deleting a task"""
        task_id = sample_task['id']

        response = client.delete(f'/api/tasks/{task_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Task deleted successfully'
        assert data['deleted_task']['id'] == task_id

        # Verify task is actually deleted
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404

class TestTaskFiltering:
    """Additional test class for filtering functionality"""

    def test_filter_by_status(self, client):
        """Test filtering tasks by status"""
        # Create tasks with different statuses
        pending_task = {
            'title': 'Pending Task',
            'status': 'pending',
            'priority': 'medium'
        }
        completed_task = {
            'title': 'Completed Task',
            'status': 'completed',
            'priority': 'medium'
        }

        client.post('/api/tasks', data=json.dumps(pending_task), content_type='application/json')
        client.post('/api/tasks', data=json.dumps(completed_task), content_type='application/json')

        # Filter by pending status
        response = client.get('/api/tasks?status=pending')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert all(task['status'] == 'pending' for task in data['tasks'])

    def test_filter_by_priority(self, client):
        """Test filtering tasks by priority"""
        # Create tasks with different priorities
        low_priority = {
            'title': 'Low Priority Task',
            'status': 'pending',
            'priority': 'low'
        }
        high_priority = {
            'title': 'High Priority Task',
            'status': 'pending',
            'priority': 'high'
        }

        client.post('/api/tasks', data=json.dumps(low_priority), content_type='application/json')
        client.post('/api/tasks', data=json.dumps(high_priority), content_type='application/json')

        # Filter by high priority
        response = client.get('/api/tasks?priority=high')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert all(task['priority'] == 'high' for task in data['tasks'])

class TestErrorHandling:
    """Test error handling and validation"""

    def test_create_task_validation(self, client):
        """Test validation when creating a task"""
        # Test missing title
        invalid_data = {
            'description': 'Task without title',
            'status': 'pending'
        }

        response = client.post('/api/tasks',
                              data=json.dumps(invalid_data),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
        assert 'Title is required' in data['errors']

    def test_invalid_status_update(self, client, sample_task):
        """Test updating task with invalid status"""
        task_id = sample_task['id']
        invalid_data = {
            'status': 'invalid_status'
        }

        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps(invalid_data),
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data

    def test_get_nonexistent_task(self, client):
        """Test getting a task that doesn't exist"""
        response = client.get('/api/tasks/99999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'Task not found'

    def test_update_nonexistent_task(self, client):
        """Test updating a task that doesn't exist"""
        update_data = {'title': 'Updated Title'}

        response = client.put('/api/tasks/99999',
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 404

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist"""
        response = client.delete('/api/tasks/99999')

        assert response.status_code == 404

class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['service'] == 'Task Management API'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])