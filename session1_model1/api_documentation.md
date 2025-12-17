# Task Management API Documentation

## Overview

This RESTful API provides complete task management functionality with CRUD operations, filtering, and data persistence using SQLite.

**Base URL**: `http://localhost:5001/api`

## Data Model

### Task Object

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "created_at": "2025-12-15T10:30:00.000Z"
}
```

#### Fields:
- **id** (integer, read-only): Unique identifier
- **title** (string, required): Task title (max 200 characters)
- **description** (string, optional): Detailed task description
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
      "id": 1,
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
- `id`: Task ID (integer)

**Response:**
```json
{
  "id": 1,
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
  "title": "New Task",
  "description": "Task description",
  "status": "pending",
  "priority": "medium"
}
```

**Required Fields:**
- `title`: Task title

**Optional Fields:**
- `description`: Task description (default: empty string)
- `status`: Task status (default: `pending`)
- `priority`: Task priority (default: `medium`)

**Response:**
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "created_at": "2025-12-15T10:35:00.000Z"
}
```

**Status Codes:**
- `201`: Task created successfully
- `400`: Validation error or missing required fields
- `500`: Server error

### 5. Update Task
**PUT** `/tasks/{id}`

Update an existing task.

**Path Parameters:**
- `id`: Task ID (integer)

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "status": "completed",
  "priority": "high"
}
```

**Optional Fields:**
- `title`: Updated task title
- `description`: Updated task description
- `status`: Updated task status
- `priority`: Updated task priority

**Response:**
```json
{
  "id": 1,
  "title": "Updated Task",
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
- `id`: Task ID (integer)

**Response:**
```json
{
  "message": "Task deleted successfully",
  "deleted_task": {
    "id": 1,
    "title": "Task to delete",
    "description": "This task will be deleted",
    "status": "pending",
    "priority": "low",
    "created_at": "2025-12-15T10:30:00.000Z"
  }
}
```

**Status Codes:**
- `200`: Task deleted successfully
- `404`: Task not found
- `500`: Server error

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

For validation errors:
```json
{
  "error": "Validation failed",
  "errors": [
    "Title is required",
    "Invalid status. Must be: pending, in-progress, or completed"
  ]
}
```

## Usage Examples

### Create a task using curl:
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write comprehensive API docs",
    "priority": "high"
  }'
```

### Get all pending tasks:
```bash
curl "http://localhost:5001/api/tasks?status=pending"
```

### Update a task:
```bash
curl -X PUT http://localhost:5001/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Delete a task:
```bash
curl -X DELETE http://localhost:5001/api/tasks/1
```

## Testing

The API includes comprehensive test cases. Run tests with:
```bash
python -m pytest tests.py -v
```

## Rate Limiting

No rate limiting is currently implemented. Consider adding rate limiting for production use.

## Authentication

This API does not implement authentication. For production use, add authentication middleware.

## Data Persistence

Tasks are stored in a SQLite database file (`tasks.db`) that is automatically created when the API first runs.