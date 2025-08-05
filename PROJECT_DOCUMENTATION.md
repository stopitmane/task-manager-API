# Task Management System API - Project Documentation

## Project Overview

This is a comprehensive **Task Management System API** built with modern Python technologies. It demonstrates full-stack development skills including REST API design, authentication, database operations, testing, and documentation.

## Key Features Demonstrated

### 1. **Modern Python Development**
- **FastAPI**: High-performance web framework with automatic API documentation
- **SQLAlchemy**: Advanced ORM with relationship management
- **Pydantic**: Data validation and serialization
- **Type Hints**: Full type annotation throughout the codebase

### 2. **Security & Authentication**
- **JWT Tokens**: Secure authentication with JSON Web Tokens
- **Password Hashing**: bcrypt for secure password storage
- **OAuth2**: Standard authentication flow
- **Input Validation**: Comprehensive request/response validation

### 3. **Database Design**
- **SQLAlchemy ORM**: Object-relational mapping
- **Relationship Management**: User-Task relationships
- **Enum Support**: Priority and status enums
- **Migration System**: Alembic for database versioning

### 4. **API Design**
- **RESTful Endpoints**: Standard HTTP methods and status codes
- **Pagination**: Efficient data retrieval
- **Filtering**: Tasks by status and priority
- **Error Handling**: Comprehensive error responses

### 5. **Testing**
- **Unit Tests**: Comprehensive test coverage
- **Integration Tests**: API endpoint testing
- **Test Isolation**: In-memory database for testing
- **Authentication Testing**: Token-based auth testing

### 6. **Development Practices**
- **Environment Configuration**: .env file management
- **Dependency Management**: requirements.txt
- **Code Organization**: Modular structure
- **Documentation**: Auto-generated API docs

## Technical Architecture

### Project Structure
```
task_management_system/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Authentication logic
│   ├── crud.py            # Database operations
│   └── api/               # API endpoints
│       ├── __init__.py
│       ├── auth.py        # Authentication endpoints
│       └── tasks.py       # Task management endpoints
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_auth.py      # Authentication tests
│   └── test_tasks.py     # Task management tests
├── alembic/               # Database migrations
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── run.py                # Application runner
└── test_runner.py        # Test runner
```

### Database Schema

#### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `created_at`: Timestamp
- `updated_at`: Timestamp

#### Tasks Table
- `id`: Primary key
- `title`: Task title (required)
- `description`: Task description (optional)
- `priority`: Enum (low, medium, high)
- `status`: Enum (pending, in_progress, completed)
- `due_date`: Optional due date
- `owner_id`: Foreign key to users table
- `created_at`: Timestamp
- `updated_at`: Timestamp

### API Endpoints

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

#### Task Management
- `GET /tasks/` - List user's tasks (paginated)
- `POST /tasks/` - Create new task
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `GET /tasks/status/{status}` - Filter by status
- `GET /tasks/priority/{priority}` - Filter by priority

## Development Skills Demonstrated

### 1. **Backend Development**
- **FastAPI**: Modern async web framework
- **SQLAlchemy**: Advanced ORM usage
- **Pydantic**: Data validation and serialization
- **JWT Authentication**: Secure token-based auth
- **Database Design**: Proper schema design with relationships

### 2. **API Design**
- **RESTful Principles**: Proper HTTP methods and status codes
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Proper error responses
- **Documentation**: Auto-generated API docs with Swagger UI

### 3. **Testing**
- **Unit Testing**: Comprehensive test coverage
- **Integration Testing**: API endpoint testing
- **Test Organization**: Proper test structure
- **Mocking**: Database mocking for tests

### 4. **DevOps & Deployment**
- **Environment Management**: .env configuration
- **Dependency Management**: requirements.txt
- **Database Migrations**: Alembic integration
- **Documentation**: Comprehensive README and docs

### 5. **Code Quality**
- **Type Hints**: Full type annotation
- **Modular Design**: Clean separation of concerns
- **Error Handling**: Comprehensive error management
- **Security**: Password hashing, JWT tokens

## Portfolio Value

This project demonstrates:

1. **Full-Stack Development**: Complete backend API with database
2. **Modern Technologies**: FastAPI, SQLAlchemy, Pydantic
3. **Security Implementation**: JWT authentication, password hashing
4. **Testing**: Comprehensive test suite
5. **Documentation**: Auto-generated API docs
6. **Best Practices**: Clean code, proper structure, error handling

## Running the Project

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd task_management_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your configuration

# Run the application
python run.py
```

### Testing
```bash
# Run all tests
python test_runner.py

# Or use pytest directly
pytest tests/ -v
```

### API Documentation
Once running, visit:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Future Enhancements

This project can be extended with:

1. **Frontend**: React/Vue.js frontend
2. **Real-time**: WebSocket support for live updates
3. **File Upload**: Task attachments
4. **Notifications**: Email/SMS notifications
5. **Analytics**: Task completion statistics
6. **Team Features**: Multi-user task sharing
7. **Mobile API**: Mobile app support
8. **Deployment**: Docker containerization

## Learning Outcomes

This project demonstrates proficiency in:

- **Modern Python Development**: FastAPI, async/await
- **Database Design**: SQLAlchemy ORM, relationships
- **API Development**: RESTful design, validation
- **Security**: Authentication, authorization
- **Testing**: Unit and integration tests
- **Documentation**: Auto-generated API docs
- **Project Structure**: Clean, maintainable code

This project showcases the skills needed for modern backend development and would be an excellent addition to any developer's portfolio. 