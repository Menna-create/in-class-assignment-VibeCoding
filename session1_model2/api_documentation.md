# Task Management API Documentation - Session 1 Model 2 (PDM)

## Overview

This RESTful API provides complete task management functionality with CRUD operations, filtering, and data persistence using JSON file storage. This implementation follows the Planning-Driven Model (PDM) approach with layered architecture.

**Base URL**: `http://localhost:5001/api`

## Data Model

### Task Object

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "created_at": "2025-12-15T10:30:00.000Z"
}
```

#### Fields:
- **id** (string, UUID, read-only): Unique identifier
- **title** (string, required): Task title (max 200 characters)
- **description** (string, optional): Detailed task description (max 1000 characters)
- **status** (string, required): Task status - `pending`, `in-progress`, or `completed`
- **priority** (string, required): Task priority - `low`, `medium`, or `high`
- **created_at** (datetime, read-only): ISO 8601 timestamp of creation

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-15T10:30:00.000Z",
  "service": "Task Management API"
}
```

### 2. Get All Tasks
**GET** `/tasks`

Retrieve all tasks with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (`pending`, `in-progress`, `completed`)
- `priority` (optional): Filter by priority (`low`, `medium`, `high`)

**Examples:**
```
GET /api/tasks
GET /api/tasks?status=pending
GET /api/tasks?priority=high
GET /api/tasks?status=in-progress&priority=medium
```

**Response:**
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Complete project",
      "description": "Finish the implementation",
      "status": "in-progress",
      "priority": "high",
      "created_at": "2025-12-15T10:30:00.000Z"
    }
  ],
  "count": 1
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid filter parameters
- `500`: Server error

### 3. Get Single Task
**GET** `/tasks/{id}`

Retrieve a specific task by ID.

**Path Parameters:**
- `id`: Task ID (UUID string)

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project",
  "description": "Finish the implementation",
  "status": "in-progress",
  "priority": "high",
  "created_at": "2025-12-15T10:30:00.000Z"
}
```

**Status Codes:**
- `200`: Success
- `404`: Task not found
- `500`: Server error

### 4. Create Task
**POST** `/tasks`

Create a new task.

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "status": "pending",
  "priority": "medium"
}
```

**Required Fields:**
- `title`: Task title (1-200 characters)

**Optional Fields:**
- `description`: Task description (max 1000 characters)
- `status`: Default is `pending`
- `priority`: Default is `medium`

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "New task title",
  "description": "Optional task description",
  "status": "pending",
  "priority": "medium",
  "created_at": "2025-12-15T10:35:00.000Z"
}
```

**Status Codes:**
- `201`: Task created successfully
- `400`: Validation error
- `500`: Server error

### 5. Update Task
**PUT** `/tasks/{id}`

Update an existing task.

**Path Parameters:**
- `id`: Task ID (UUID string)

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed",
  "priority": "high"
}
```

**Partial Updates:**
You can update one or more fields:
```json
{
  "status": "completed"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed",
  "priority": "high",
  "created_at": "2025-12-15T10:30:00.000Z"
}
```

**Status Codes:**
- `200`: Task updated successfully
- `400`: Validation error
- `404`: Task not found
- `500`: Server error

### 6. Delete Task
**DELETE** `/tasks/{id}`

Delete a task.

**Path Parameters:**
- `id`: Task ID (UUID string)

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

**Status Codes:**
- `200`: Task deleted successfully
- `404`: Task not found
- `500`: Server error

## Error Handling

### Error Response Format

All error responses follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Error Scenarios

#### Validation Errors (400)
```json
{
  "error": "Validation failed",
  "errors": [
    "Title is required",
    "Title must be less than 200 characters"
  ]
}
```

#### Not Found Errors (404)
```json
{
  "error": "Task not found",
  "message": "Task not found"
}
```

#### Server Errors (500)
```json
{
  "error": "Failed to create task",
  "message": "Storage operation failed"
}
```

## Usage Examples

### Using curl

#### Create a task
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the API",
    "status": "pending",
    "priority": "high"
  }'
```

#### Get all tasks
```bash
curl http://localhost:5001/api/tasks
```

#### Get filtered tasks
```bash
curl "http://localhost:5001/api/tasks?status=pending&priority=high"
```

#### Get specific task
```bash
curl http://localhost:5001/api/tasks/550e8400-e29b-41d4-a716-446655440000
```

#### Update a task
```bash
curl -X PUT http://localhost:5001/api/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "in-progress"
  }'
```

#### Delete a task
```bash
curl -X DELETE http://localhost:5001/api/tasks/550e8400-e29b-41d4-a716-446655440000
```

### Using Python requests

```python
import requests
import json

base_url = "http://localhost:5001/api"

# Create a task
task_data = {
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the API",
    "status": "pending",
    "priority": "high"
}

response = requests.post(f"{base_url}/tasks", json=task_data)
if response.status_code == 201:
    task = response.json()
    print(f"Created task with ID: {task['id']}")

    # Get the task
    response = requests.get(f"{base_url}/tasks/{task['id']}")
    if response.status_code == 200:
        retrieved_task = response.json()
        print(f"Retrieved task: {retrieved_task['title']}")
```

## Data Storage

Tasks are persisted in a `tasks.json` file in the application directory. The storage implementation includes:

- **Atomic Writes**: Data is written to a temporary file first, then renamed
- **Thread Safety**: File locking prevents concurrent access issues
- **Data Integrity**: Automatic recovery from corrupted files
- **JSON Format**: Human-readable data storage

## Architecture

This API follows the Planning-Driven Model (PDM) with layered architecture:

1. **API Layer** (`app.py`): HTTP request/response handling
2. **Business Logic Layer** (`task_manager.py`): Task management operations
3. **Data Access Layer** (`storage.py`): JSON file storage with thread safety
4. **Models Layer** (`models.py`): Task data model and validation

## Testing

The API includes comprehensive tests covering:

- Model validation
- Storage operations
- Business logic
- API endpoints
- Error handling

Run tests with:
```bash
pytest -v
```

## Rate Limiting and Authentication

This implementation does not include rate limiting or authentication. For production use, consider adding:
- API key authentication
- JWT token authentication
- Rate limiting middleware
- HTTPS encryption
- Input sanitization

## Performance Considerations

- JSON file storage is suitable for small to medium datasets
- For large datasets, consider database storage (SQLite, PostgreSQL)
- File I/O operations are protected with threading locks
- Atomic writes prevent data corruption

## Versioning

This is version 1 of the API. Future versions may include:
- Pagination for large result sets
- Advanced filtering options
- Task dependencies
- User management
- Bulk operations