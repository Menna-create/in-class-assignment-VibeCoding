# Prompts Collection

## Initialize

This file contains all the prompts and instructions for the in-class assignment vibe coding project.

---

### Prompts will be added here as they are created

---
Prompt 1:  Unconstrained Automation Model (UAM)
```
Create a RESTful Task Management API with the following requirements:

CORE FEATURES:
- Full CRUD operations for tasks (Create, Read, Update, Delete)
- Each task must have: ID, title, description, status (pending/in-progress/completed), priority (low/medium/high), and created timestamp
- Ability to filter tasks by status and priority
- Data persistence using either file-based storage or SQLite

TECHNICAL REQUIREMENTS:
- RESTful design with proper HTTP methods (GET, POST, PUT, DELETE)
- Input validation and error handling
- Appropriate HTTP status codes
- Include API documentation describing all endpoints
- Implement at least 5 meaningful test cases

FILE STRUCTURE:
Organize the project with this structure:
session1_model1/
|---- app.py (or main.py)          # Main application file
|---- requirements.txt              # Dependencies
|---- README.md                     # Setup and usage instructions
|---- tests.py                      # Test cases
|---- tasks.db (or tasks.json)      # Data storage (generated at runtime)
|---- api_documentation.md          # API endpoint documentation

Please generate a complete, working implementation with all the files listed above. Include clear setup instructions and examples of how to run and test the API.

 i am getting the following Traceback (most recent call last):
  File "/Users/mennakhaled/Desktop/in-class-assignment-vibe-coding/session1_model1/app.py", line
 211, in <module>
    @app.before_first_request
     ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'Flask' object has no attribute 'before_first_request'. Did you mean: 
'_got_first_request'? 
```
Prompt 2 : Iterative Conversational Collaboration Model (ICCM)
```
Planning-Driven Model (PDM) - Implementation Guide
Step 1: Create Planning Documents First
Before writing any code, create these three documents in your session1_model2/ (or appropriate) folder:
Document 1: technical_specs.md
markdown# Task Management API - Technical Specifications

## System Architecture

### Module Structure
1. **API Layer** (`app.py`)
   - Flask/FastAPI application setup
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
Document 2: coding_rules.md
markdown# Coding Rules and Conventions

## General Guidelines
- Python 3.8+ syntax
- Type hints for all function signatures
- Docstrings for all classes and public methods
- Follow PEP 8 style guide

## Naming Conventions
- Classes: PascalCase (e.g., `TaskManager`)
- Functions/methods: snake_case (e.g., `create_task`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_TITLE_LENGTH`)
- Private methods: prefix with underscore (e.g., `_validate_task`)

## Error Handling Pattern
```python
try:
    # operation
    return {"success": True, "data": result}
except SpecificError as e:
    return {"success": False, "error": str(e)}, 400
```

## Response Format
Success:
```json
{
    "success": true,
    "data": {...}
}
```

Error:
```json
{
    "success": false,
    "error": "Error message"
}
```

## Documentation Requirements
- Each module must have a module-level docstring
- Each class must have a class docstring
- Each public method must have:
  - Description of purpose
  - Args: parameter descriptions
  - Returns: return value description
  - Raises: exceptions that may be raised

## Testing Requirements
- Test file organization matches source file organization
- Test functions named: `test_<functionality>`
- Use pytest fixtures for setup/teardown
- Minimum 80% code coverage goal
Document 3: implementation_plan.md
markdown# Implementation Plan

## Phase 1: Core Data Structures (Implement First)
**File**: `models.py`
- Create Status enum (pending, in-progress, completed)
- Create Priority enum (low, medium, high)
- Create Task dataclass/model
- Implement validation methods
- Add `to_dict()` and `from_dict()` methods

**Validation**:
- Can create Task instances
- Validation catches invalid inputs
- Serialization works correctly

---

## Phase 2: Storage Layer (Implement Second)
**File**: `storage.py`
- Create abstract Storage interface
- Implement JSONStorage class
  - `__init__(filepath)`
  - `_load()` - private method to read from file
  - `_save(data)` - private method to write to file
  - `get_all()` - return all tasks
  - `get_by_id(task_id)` - return single task
  - `save(task)` - add/update task
  - `delete(task_id)` - remove task

**Validation**:
- Can save and load tasks
- Handles missing file gracefully
- Thread-safe operations

---

## Phase 3: Business Logic (Implement Third)
**File**: `task_manager.py`
- Create TaskManager class
  - `__init__(storage)`
  - `create_task(title, description, status, priority)` - returns Task
  - `get_task(task_id)` - returns Task or None
  - `get_all_tasks(status_filter=None, priority_filter=None)` - returns list
  - `update_task(task_id, **updates)` - returns updated Task
  - `delete_task(task_id)` - returns boolean

**Validation**:
- All CRUD operations work
- Filtering works correctly
- Invalid operations raise appropriate errors

---

## Phase 4: API Layer (Implement Fourth)
**File**: `app.py`
- Set up Flask application
- Initialize TaskManager
- Implement routes:
  1. POST /tasks
  2. GET /tasks (with query params: status, priority)
  3. GET /tasks/<id>
  4. PUT /tasks/<id>
  5. DELETE /tasks/<id>
- Add error handlers
- Add request validation

**Validation**:
- All endpoints respond correctly
- Error handling works
- HTTP status codes are appropriate

---

## Phase 5: Testing (Implement Fifth)
**File**: `tests.py`
- Test Task model validation
- Test Storage layer operations
- Test TaskManager business logic
- Test API endpoints (at least 5 tests):
  1. Test create task successfully
  2. Test get all tasks with filters
  3. Test update task
  4. Test delete task
  5. Test error handling (invalid input)

---

## Phase 6: Documentation (Implement Last)
**Files**: `README.md`, `api_documentation.md`
- Setup instructions
- How to run the application
- API endpoint documentation
- Example requests and responses
```

---

## Step 2: Implement Phase by Phase

Now use these prompts **one at a time**, in order:

### Prompt 1 - Models Layer
```
I am implementing a Task Management API using a Planning-Driven approach. I have created detailed specifications.

Please implement Phase 1 (Core Data Structures) according to these specifications:

[Paste content from technical_specs.md - Data Models section]
[Paste content from coding_rules.md]
[Paste content from implementation_plan.md - Phase 1 section]

Create the models.py file with the Task model, enums, and validation logic as specified.
```

### Prompt 2 - Storage Layer
```
Now implement Phase 2 (Storage Layer) according to these specifications:

[Paste relevant sections from your planning documents]

Create the storage.py file with the JSONStorage implementation as specified. It should work with the Task model from models.py.
```

### Prompt 3 - Business Logic
```
Now implement Phase 3 (Business Logic) according to these specifications:

[Paste relevant sections]

Create the task_manager.py file with the TaskManager class as specified.
```

### Prompt 4 - API Layer
```
Now implement Phase 4 (API Layer) according to these specifications:

[Paste relevant sections]

Create the app.py file with all the Flask routes as specified.
```

### Prompt 5 - Testing
```
Now implement Phase 5 (Testing) according to these specifications:

[Paste relevant sections]

Create the tests.py file with at least 5 meaningful test cases covering the requirements.
```

### Prompt 6 - Documentation
```
Now implement Phase 6 (Documentation) according to these specifications:

[Paste relevant sections]

Create README.md and api_documentation.md files with setup instructions and API documentation.

Step 3: Document Your Process
In prompts.md, record:

All three planning documents (technical_specs.md, coding_rules.md, implementation_plan.md)
Each prompt you used for each phase
AI responses and any adjustments you made
Time spent on planning vs. implementation
Whether the implementation followed your specifications


Step 4: Git Commit
bashgit add session1_model2/
git commit -m "Session 1 - Planning-Driven Model (PDM) approach"
```




*Last updated: December 15, 2025*