# Task Management System API

A modern, feature-rich task management system built with FastAPI, SQLAlchemy, and Pydantic. This project demonstrates REST API development, authentication, database operations, and testing.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: CRUD operations for tasks with status tracking
- **RESTful API**: Clean, well-documented API endpoints
- **Database Integration**: SQLAlchemy ORM with SQLite database
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling and status codes
- **Testing**: Unit tests with pytest
- **Documentation**: Auto-generated API documentation with Swagger UI

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **bcrypt**: Password hashing
- **pytest**: Testing framework
- **Alembic**: Database migrations

## Project Structure

```
task_management_system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── crud.py              # Database operations
│   └── api/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       └── tasks.py         # Task endpoints
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_tasks.py
├── alembic/                 # Database migrations
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task_management_system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Tasks
- `GET /tasks/` - Get all tasks for authenticated user
- `POST /tasks/` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Testing

Run the test suite:
```bash
pytest
```

## Usage Examples

### Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "email": "john@example.com", "password": "securepassword"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "password": "securepassword"}'
```

### Create a task
```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Complete project", "description": "Finish the portfolio project", "priority": "high"}'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. 