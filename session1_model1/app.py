from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import os

app = Flask(__name__)

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "tasks.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Enum definitions
class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in-progress'
    COMPLETED = 'completed'

class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    priority = db.Column(db.Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat()
        }

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': 'Task not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

# Validation functions
def validate_task_data(data, partial=False):
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

    return errors

# API Routes
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks with optional filtering
    Query parameters:
    - status: Filter by task status
    - priority: Filter by task priority
    """
    try:
        query = Task.query

        # Filter by status
        status_filter = request.args.get('status')
        if status_filter:
            if status_filter not in [s.value for s in TaskStatus]:
                return jsonify({'error': 'Invalid status filter'}), 400
            query = query.filter(Task.status == TaskStatus(status_filter))

        # Filter by priority
        priority_filter = request.args.get('priority')
        if priority_filter:
            if priority_filter not in [p.value for p in TaskPriority]:
                return jsonify({'error': 'Invalid priority filter'}), 400
            query = query.filter(Task.priority == TaskPriority(priority_filter))

        tasks = query.all()
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve tasks', 'message': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.to_dict())
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve task', 'message': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input
        errors = validate_task_data(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'errors': errors}), 400

        # Create new task
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=TaskStatus(data.get('status', 'pending')),
            priority=TaskPriority(data.get('priority', 'medium'))
        )

        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create task', 'message': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input
        errors = validate_task_data(data, partial=True)
        if errors:
            return jsonify({'error': 'Validation failed', 'errors': errors}), 400

        # Update task fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = TaskStatus(data['status'])
        if 'priority' in data:
            task.priority = TaskPriority(data['priority'])

        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task', 'message': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully', 'deleted_task': task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task', 'message': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Task Management API'
    })

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)