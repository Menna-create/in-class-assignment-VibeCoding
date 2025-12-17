"""
Flask application for Task Management API.

This module contains the Flask application with all API endpoints.
"""

from datetime import datetime
from flask import Flask, jsonify, request
from models import validate_task_data, TaskStatus, TaskPriority
from task_manager import TaskManager
from storage import JSONStorage
import os

# Initialize Flask application
app = Flask(__name__)

# Initialize storage and task manager
storage_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
storage = JSONStorage(storage_path)
task_manager = TaskManager(storage)

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({'error': 'Not found', 'message': 'Task not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error errors."""
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

# API Routes
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks with optional filtering.

    Query parameters:
    - status: Filter by task status
    - priority: Filter by task priority
    """
    try:
        # Get query parameters
        status_filter = request.args.get('status')
        priority_filter = request.args.get('priority')

        # Get tasks with filters
        tasks = task_manager.get_all_tasks(
            status_filter=status_filter,
            priority_filter=priority_filter
        )

        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve tasks', 'message': str(e)}), 500

@app.route('/api/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID."""
    try:
        task = task_manager.get_task(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.to_dict())
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve task', 'message': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input
        errors = validate_task_data(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'errors': errors}), 400

        # Create new task
        task = task_manager.create_task(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium')
        )

        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create task', 'message': str(e)}), 500

@app.route('/api/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input for partial update
        errors = validate_task_data(data, partial=True)
        if errors:
            return jsonify({'error': 'Validation failed', 'errors': errors}), 400

        # Update task
        task = task_manager.update_task(task_id, data)
        return jsonify(task.to_dict())
    except ValueError as e:
        if 'not found' in str(e).lower():
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update task', 'message': str(e)}), 500

@app.route('/api/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        deleted = task_manager.delete_task(task_id)
        if not deleted:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'error': 'Failed to delete task', 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Task Management API'
    })

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5001)