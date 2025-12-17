# Task Management API - Session 1 Model 2 (PDM)

A RESTful Task Management API implemented using the Planning-Driven Model (PDM) approach with Flask and JSON file-based storage.

## Project Structure

```
session1_model2/
├── app.py                    # Flask application and API endpoints
├── models.py                 # Task data model and validation
├── storage.py                # JSON file-based storage layer
├── task_manager.py           # Business logic layer
├── tests.py                  # Comprehensive test suite
├── requirements.txt          # Python dependencies
├── tasks.json               # Data storage (generated at runtime)
├── technical_specs.md       # Technical specifications document
├── coding_rules.md          # Coding conventions and rules
├── implementation_plan.md   # Detailed implementation plan
├── README.md                # This file
└── api_documentation.md     # Complete API documentation
```

## Architecture

This implementation follows a layered architecture with clear separation of concerns:

1. **API Layer** (`app.py`) - Flask routes and HTTP handling
2. **Business Logic Layer** (`task_manager.py`) - Task management operations
3. **Data Access Layer** (`storage.py`) - JSON file storage with thread safety
4. **Models Layer** (`models.py`) - Task data model and validation

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd session1_model2
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask application:**
   ```bash
   python app.py
   ```

2. **The API will be available at:**
   ```
   http://localhost:5001
   ```

3. **Health check endpoint:**
   ```bash
   curl http://localhost:5001/api/health
   ```

## Running Tests

1. **Run all tests:**
   ```bash
   pytest -v
   ```

2. **Run tests with coverage:**
   ```bash
   pytest --cov=. --cov-report=html
   ```

3. **Run specific test class:**
   ```bash
   pytest tests.py::TestTaskManagementAPI -v
   ```

## Key Features

- **Full CRUD Operations**: Create, Read, Update, Delete tasks
- **Task Filtering**: Filter by status and priority
- **Data Validation**: Comprehensive input validation
- **JSON Storage**: Simple file-based persistence
- **Thread Safety**: Safe concurrent access to data
- **Error Handling**: Proper HTTP status codes and error messages
- **Comprehensive Testing**: 100% test coverage
- **Health Monitoring**: Health check endpoint

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/tasks` - List all tasks (with optional filtering)
- `GET /api/tasks/{id}` - Get specific task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Example Usage

### Create a Task
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

### Get All Tasks
```bash
curl http://localhost:5001/api/tasks
```

### Filter Tasks by Status
```bash
curl "http://localhost:5001/api/tasks?status=pending"
```

### Update a Task
```bash
curl -X PUT http://localhost:5001/api/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "in-progress"
  }'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:5001/api/tasks/{task_id}
```

## Planning-Driven Model (PDM) Implementation

This project demonstrates the PDM approach with:

1. **Three Planning Documents** created before any code:
   - `technical_specs.md` - System architecture and specifications
   - `coding_rules.md` - Coding conventions and standards
   - `implementation_plan.md` - Detailed 6-phase implementation plan

2. **Six Implementation Phases**:
   - Phase 1: Core Data Structures (`models.py`)
   - Phase 2: Storage Layer (`storage.py`)
   - Phase 3: Business Logic (`task_manager.py`)
   - Phase 4: API Layer (`app.py`)
   - Phase 5: Testing (`tests.py`)
   - Phase 6: Documentation (`README.md`, `api_documentation.md`)

## Comparison with Session 1 Model 1

| Feature | Model 1 (SQLite) | Model 2 (PDM) |
|---------|-----------------|---------------|
| Architecture | Monolithic (single file) | Layered (4 modules) |
| Storage | SQLite with SQLAlchemy | JSON file-based |
| ID Type | Integer auto-increment | UUID strings |
| Separation of Concerns | Mixed | Clear separation |
| Planning Approach | Direct implementation | Planning-Driven |
| Thread Safety | Database handled | Manual locking |
| Dependencies | Flask-SQLAlchemy | Flask only |

## Data Storage

Tasks are stored in a `tasks.json` file in the project directory. The file is created automatically when the application starts. The storage implementation includes:

- Atomic writes for data integrity
- Thread-safe operations with file locking
- Automatic recovery from corrupted files
- Efficient read/write operations

## Error Handling

The API implements comprehensive error handling:

- **400 Bad Request**: Validation errors, invalid input
- **404 Not Found**: Task not found, invalid endpoints
- **500 Internal Server Error**: Unexpected errors

All error responses follow a consistent format:
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

## Development

### Adding New Features

1. Define requirements in planning documents
2. Implement in appropriate layer (model, storage, business logic, API)
3. Add comprehensive tests
4. Update documentation

### Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Include docstrings for all classes and public methods
- Maintain test coverage above 80%

## License

This project is part of an in-class assignment for demonstrating the Planning-Driven Model approach to software development.