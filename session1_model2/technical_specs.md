# Task Management API - Technical Specifications

## System Architecture

### Module Structure
1. **API Layer** (`app.py`)
   - Flask application setup
   - Route handlers for all endpoints
   - Request/response handling

2. **Business Logic Layer** (`task_manager.py`)
   - TaskManager class
   - CRUD operations logic
   - Filtering and querying logic

3. **Data Access Layer** (`storage.py`)
   - Storage interface/abstract class
   - JSONStorage implementation
   - Database operations (read/write)

4. **Models Layer** (`models.py`)
   - Task data model
   - Validation logic
   - Enums for status and priority

5. **Testing Layer** (`tests.py`)
   - Unit tests for each component
   - Integration tests for API endpoints

## Data Models

### Task Model
```python
{
    "id": "string (UUID)",
    "title": "string (required, max 200 chars)",
    "description": "string (optional, max 1000 chars)",
    "status": "enum (pending|in-progress|completed)",
    "priority": "enum (low|medium|high)",
    "created_at": "ISO 8601 timestamp"
}
```

### Validation Rules
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Status: Must be one of the three valid values
- Priority: Must be one of the three valid values
- ID: Auto-generated UUID
- Created_at: Auto-generated timestamp

## API Endpoints

1. **POST /tasks** - Create new task
2. **GET /tasks** - Get all tasks (with optional filters)
3. **GET /tasks/{id}** - Get specific task
4. **PUT /tasks/{id}** - Update task
5. **DELETE /tasks/{id}** - Delete task
6. **GET /health** - Health check endpoint

## Technology Stack
- Framework: Flask (lightweight, simple)
- Storage: JSON file-based
- Testing: pytest
- Validation: Built-in Python validation

## Error Handling Strategy
- Use HTTP status codes appropriately
- Return consistent error response format
- Validate all inputs before processing
- Handle file I/O errors gracefully