# Coding Rules and Conventions

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