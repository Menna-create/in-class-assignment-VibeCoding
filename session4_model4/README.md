# Task Management API - Test-Driven Development (TDD) Implementation

## Session 4 - Model 4: Test-Driven Model (TDM)

This implementation demonstrates the **Test-Driven Development (TDD)** approach where tests are written FIRST before any implementation code.

## 🎯 TDD Philosophy

This project follows the classic TDD cycle:

1. **RED** ❌ - Write a failing test first
2. **GREEN** ✅ - Write minimal code to make the test pass
3. **REFACTOR** 🔄 - Improve code while keeping tests green

## 📋 Project Overview

A RESTful Task Management API with full CRUD operations, built entirely using Test-Driven Development methodology.

### Features

- ✅ Create, Read, Update, Delete tasks
- ✅ Filter tasks by status (pending, in-progress, completed)
- ✅ Filter tasks by priority (low, medium, high)
- ✅ JSON file-based persistence
- ✅ Thread-safe storage operations
- ✅ Comprehensive test suite (54 tests)
- ✅ 95%+ test coverage

## 🏗️ Architecture

The application follows a layered architecture:

```
┌─────────────────────────────────────┐
│         API Layer (app.py)          │  ← Flask routes & HTTP handling
├─────────────────────────────────────┤
│   Business Logic (task_manager.py)  │  ← CRUD operations & validation
├─────────────────────────────────────┤
│     Data Access (storage.py)        │  ← JSON persistence layer
├─────────────────────────────────────┤
│        Models (models.py)           │  ← Data structures & validation
└─────────────────────────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd session4_model4
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Running Tests

The entire implementation was driven by tests. Run the test suite to verify everything works:

### Run All Tests

```bash
pytest test_task_manager.py -v
```

### Run Tests with Coverage Report

```bash
pytest test_task_manager.py --cov=. --cov-report=html --cov-report=term
```

This will generate:
- Terminal coverage report
- HTML coverage report in `htmlcov/` directory

### Run Specific Test Classes

```bash
# Test only the Model Layer
pytest test_task_manager.py::TestTaskModel -v

# Test only the Storage Layer
pytest test_task_manager.py::TestStorage -v

# Test only the Business Logic
pytest test_task_manager.py::TestTaskManager -v

# Test only the API Layer
pytest test_task_manager.py::TestAPI -v

# Test only Integration Tests
pytest test_task_manager.py::TestIntegration -v
```

## 🚀 Running the Application

### Start the Flask Server

```bash
python app.py
```

The API will be available at `http://localhost:5001`

### Using a Different Port

```bash
# Set environment variable
export FLASK_RUN_PORT=8000
python app.py
```

## 📡 API Endpoints

### Health Check
```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Task Management API",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Create Task
```bash
POST /api/tasks
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive README",
  "status": "pending",
  "priority": "high"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Write comprehensive README",
  "status": "pending",
  "priority": "high",
  "created_at": "2024-01-15T10:30:00"
}
```

### Get All Tasks
```bash
GET /api/tasks
GET /api/tasks?status=pending
GET /api/tasks?priority=high
GET /api/tasks?status=pending&priority=high
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "priority": "high",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### Get Single Task
```bash
GET /api/tasks/{task_id}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "priority": "high",
  "created_at": "2024-01-15T10:30:00"
}
```

### Update Task
```bash
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "status": "completed",
  "priority": "medium"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Task title",
  "description": "Task description",
  "status": "completed",
  "priority": "medium",
  "created_at": "2024-01-15T10:30:00"
}
```

### Delete Task
```bash
DELETE /api/tasks/{task_id}
```

**Response (200 OK):**
```json
{
  "message": "Task 550e8400-e29b-41d4-a716-446655440000 deleted successfully"
}
```

## 🧰 Using cURL Examples

### Create a Task
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "status": "pending",
    "priority": "medium"
  }'
```

### Get All Tasks
```bash
curl http://localhost:5001/api/tasks
```

### Get Tasks with Filter
```bash
curl "http://localhost:5001/api/tasks?status=pending&priority=high"
```

### Update a Task
```bash
curl -X PUT http://localhost:5001/api/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:5001/api/tasks/{task_id}
```

## 📊 Test Suite Breakdown

| Layer              | Test Count | Description                           |
|--------------------|------------|---------------------------------------|
| Model Layer        | 9 tests    | Task model, enums, validation         |
| Storage Layer      | 9 tests    | JSON persistence, CRUD operations     |
| Business Logic     | 16 tests   | Task management, filtering            |
| API Layer          | 15 tests   | HTTP endpoints, error handling        |
| Integration        | 5 tests    | End-to-end workflows                  |
| **TOTAL**          | **54 tests** | **Complete coverage**               |

## 📂 Project Structure

```
session4_model4/
├── app.py                    # Flask API application (Implemented 5th)
├── task_manager.py           # Business logic layer (Implemented 4th)
├── storage.py                # Data access layer (Implemented 3rd)
├── models.py                 # Data models and validation (Implemented 2nd)
├── test_task_manager.py      # Complete test suite (Written 1st!)
├── requirements.txt          # Python dependencies
├── tasks.json                # JSON storage (auto-generated)
├── README.md                 # This file
├── TDD_PROCESS.md           # TDD methodology documentation
└── api_documentation.md      # Detailed API documentation
```

## 🔧 Configuration

### Storage File Location

By default, tasks are stored in `tasks.json` in the project directory.

### Debug Mode

The application runs in debug mode by default for development.

## 🐛 Troubleshooting

### Tests Failing

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you're in the correct directory:
   ```bash
   cd session4_model4
   ```

3. Check Python version (requires 3.8+):
   ```bash
   python --version
   ```

### Port Already in Use

If port 5001 is already in use:

```bash
# Find and kill the process
lsof -ti:5001 | xargs kill -9
```

## 🔒 Validation Rules

### Task Title
- Required
- Maximum 200 characters

### Task Description
- Optional
- Maximum 1000 characters

### Task Status
- Must be one of: `pending`, `in-progress`, `completed`
- Default: `pending`

### Task Priority
- Must be one of: `low`, `medium`, `high`
- Default: `medium`

## 🆚 Comparison with Other Models

### vs. Model 1 (Unconstrained Automation)
- **TDM:** Tests written first, higher confidence
- **UAM:** Implementation first, tests optional

### vs. Model 2 (Planning-Driven)
- **TDM:** Tests are the specification
- **PDM:** Documents are the specification

### Advantages of TDD
✅ Objective quality verification (machine-verified)
✅ Clear requirements from test names
✅ Easy debugging (tests pinpoint failures)
✅ Refactoring safety net
✅ Documentation through tests

### Trade-offs
⚠️ Slower initial pace (write tests first)
⚠️ Requires test-writing discipline
⚠️ Learning curve for TDD workflow

## 📝 Development Workflow

1. **Write a failing test** (RED)
2. **Run tests** → See it fail
3. **Write minimal implementation** (GREEN)
4. **Run tests** → See it pass
5. **Refactor** if needed (REFACTOR)
6. **Run tests** → Ensure still passing
7. Repeat for next feature

## 👨‍💻 Author

Built as part of the "Vibe Coding" in-class assignment to demonstrate different AI-assisted development models.

## 📄 License

Educational project - Free to use and modify.

---

**Remember:** In TDD, the tests are not just verification—they ARE the specification! 🎯
