"""
Flask API application for Task Management - TDD Implementation.

This module was implemented AFTER writing tests in test_task_manager.py,
following the Test-Driven Development (TDD) approach.
"""

from flask import Flask, request, jsonify
from datetime import datetime
from storage import JSONStorage
from task_manager import TaskManager

# Default storage path
DEFAULT_STORAGE_PATH = 'tasks.json'


def create_app(storage_path: str = DEFAULT_STORAGE_PATH) -> Flask:
    """
    Create and configure Flask application.

    Args:
        storage_path: Path to JSON storage file

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Initialize storage and task manager
    storage = JSONStorage(storage_path)
    task_manager = TaskManager(storage)

    # ========================================================================
    # API ENDPOINTS
    # ========================================================================

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'Task Management API',
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    @app.route('/api/tasks', methods=['GET'])
    def get_all_tasks():
        """
        Get all tasks with optional filtering.

        Query Parameters:
            status: Filter by task status (pending, in-progress, completed)
            priority: Filter by task priority (low, medium, high)

        Returns:
            JSON response with tasks list and count
        """
        try:
            # Get query parameters
            status_filter = request.args.get('status')
            priority_filter = request.args.get('priority')

            # Get filtered tasks
            tasks = task_manager.get_all_tasks(
                status_filter=status_filter,
                priority_filter=priority_filter
            )

            # Convert to dictionaries
            tasks_data = [task.to_dict() for task in tasks]

            return jsonify({
                'tasks': tasks_data,
                'count': len(tasks_data)
            }), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @app.route('/api/tasks/<task_id>', methods=['GET'])
    def get_task(task_id: str):
        """
        Get a specific task by ID.

        Args:
            task_id: UUID of the task

        Returns:
            JSON response with task data
        """
        try:
            task = task_manager.get_task(task_id)

            if task is None:
                return jsonify({'error': f'Task not found: {task_id}'}), 404

            return jsonify(task.to_dict()), 200

        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """
        Create a new task.

        Request Body:
            {
                "title": "Task title (required)",
                "description": "Task description (optional)",
                "status": "pending|in-progress|completed (optional, default: pending)",
                "priority": "low|medium|high (optional, default: medium)"
            }

        Returns:
            JSON response with created task data
        """
        try:
            data = request.get_json()

            if not data:
                return jsonify({'error': 'Request body is required'}), 400

            # Extract fields
            title = data.get('title')
            description = data.get('description')
            status = data.get('status', 'pending')
            priority = data.get('priority', 'medium')

            # Create task
            task = task_manager.create_task(
                title=title,
                description=description,
                status=status,
                priority=priority
            )

            return jsonify(task.to_dict()), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @app.route('/api/tasks/<task_id>', methods=['PUT'])
    def update_task(task_id: str):
        """
        Update an existing task.

        Args:
            task_id: UUID of the task to update

        Request Body:
            {
                "title": "New title (optional)",
                "description": "New description (optional)",
                "status": "new status (optional)",
                "priority": "new priority (optional)"
            }

        Returns:
            JSON response with updated task data
        """
        try:
            data = request.get_json()

            if not data:
                return jsonify({'error': 'Request body is required'}), 400

            # Update task
            task = task_manager.update_task(task_id, data)

            return jsonify(task.to_dict()), 200

        except ValueError as e:
            error_message = str(e)
            if 'not found' in error_message.lower():
                return jsonify({'error': error_message}), 404
            return jsonify({'error': error_message}), 400
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @app.route('/api/tasks/<task_id>', methods=['DELETE'])
    def delete_task(task_id: str):
        """
        Delete a task.

        Args:
            task_id: UUID of the task to delete

        Returns:
            JSON response with success message
        """
        try:
            result = task_manager.delete_task(task_id)

            if not result:
                return jsonify({'error': f'Task not found: {task_id}'}), 404

            return jsonify({
                'message': f'Task {task_id} deleted successfully'
            }), 200

        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    # ========================================================================
    # ERROR HANDLERS
    # ========================================================================

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({'error': 'Bad Request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error."""
        return jsonify({'error': 'Internal Server Error'}), 500

    return app


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
