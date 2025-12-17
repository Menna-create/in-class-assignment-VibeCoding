# Task Management API

A complete RESTful API for task management with full CRUD operations, filtering, and data persistence.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Task filtering by status and priority
- ✅ Input validation and error handling
- ✅ SQLite database for data persistence
- ✅ Comprehensive test suite
- ✅ Detailed API documentation
- ✅ RESTful design with proper HTTP methods

## Project Structure

```
session1_model1/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── tests.py           # Test suite
├── api_documentation.md # API documentation
├── README.md          # This file
└── tasks.db           # SQLite database (created automatically)
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone or download the project**:
   ```bash
   # If you have the project files, navigate to the directory
   cd session1_model1
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # Unix/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **The API will be available at**: `http://localhost:5001`

## Quick Start Examples

### 1. Check API Health
```bash
curl http://localhost:5001/api/health
```

### 2. Create a Task
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive docs for the API",
    "priority": "high"
  }'
```

### 3. Get All Tasks
```bash
curl http://localhost:5001/api/tasks
```

### 4. Filter Tasks
```bash
# Get all pending tasks
curl "http://localhost:5001/api/tasks?status=pending"

# Get all high priority tasks
curl "http://localhost:5001/api/tasks?priority=high"
```

### 5. Update a Task
```bash
curl -X PUT http://localhost:5001/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### 6. Delete a Task
```bash
curl -X DELETE http://localhost:5001/api/tasks/1
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests with verbose output
python -m pytest tests.py -v

# Run specific test class
python -m pytest tests.py::TestTaskManagementAPI -v

# Run with coverage (if coverage is installed)
python -m pytest tests.py --cov=app -v
```

### Test Coverage

The test suite includes:
- ✅ CRUD operations testing (5 required test cases)
- ✅ Input validation testing
- ✅ Error handling testing
- ✅ Task filtering functionality
- ✅ Edge cases and boundary conditions
- ✅ Health check endpoint

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/tasks` | Get all tasks (with optional filtering) |
| GET | `/api/tasks/{id}` | Get specific task |
| POST | `/api/tasks` | Create new task |
| PUT | `/api/tasks/{id}` | Update existing task |
| DELETE | `/api/tasks/{id}` | Delete task |

## Data Model

Each task contains:
- **id**: Unique identifier (auto-generated)
- **title**: Task title (required, max 200 chars)
- **description**: Task description (optional)
- **status**: `pending`, `in-progress`, or `completed`
- **priority**: `low`, `medium`, or `high`
- **created_at**: Creation timestamp (ISO 8601 format)

## Example Workflow

1. **Create multiple tasks**:
   ```bash
   # Create a high-priority task
   curl -X POST http://localhost:5001/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Fix critical bug", "priority": "high"}'

   # Create a medium-priority task
   curl -X POST http://localhost:5001/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Write unit tests", "priority": "medium"}'
   ```

2. **List all pending tasks**:
   ```bash
   curl "http://localhost:5001/api/tasks?status=pending"
   ```

3. **Update task status to in-progress**:
   ```bash
   curl -X PUT http://localhost:5001/api/tasks/1 \
     -H "Content-Type: application/json" \
     -d '{"status": "in-progress"}'
   ```

4. **Mark task as completed**:
   ```bash
   curl -X PUT http://localhost:5001/api/tasks/1 \
     -H "Content-Type: application/json" \
     -d '{"status": "completed"}'
   ```

## Development Notes

### Database
- Uses SQLite for simplicity and portability
- Database file (`tasks.db`) is created automatically
- SQLAlchemy ORM for database operations

### Error Handling
- Consistent error response format
- Proper HTTP status codes
- Input validation with meaningful error messages

### Security Considerations
- No authentication currently implemented
- Consider adding API keys or JWT for production
- Input validation prevents injection attacks

### Performance
- Pagination not implemented (all tasks returned)
- Consider pagination for large datasets
- Database indexes on commonly filtered fields

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```
   OSError: [Errno 48] Address already in use
   ```
   Solution: Change port in `app.py` or kill process using port 5001

2. **Database connection error**:
   Ensure write permissions in the project directory

3. **Module import errors**:
   Make sure virtual environment is activated and dependencies installed

### Debug Mode

The application runs in debug mode by default. To disable:

```python
# In app.py, change the last line to:
app.run(debug=False, host='0.0.0.0', port=5001)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Documentation

For detailed API documentation, see [api_documentation.md](api_documentation.md).

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Run the test suite to verify functionality