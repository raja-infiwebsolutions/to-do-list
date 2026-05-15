# Todo API Backend

A production-ready Django REST Framework API for managing todos with full CRUD operations, filtering, searching, and authentication.

## Features

- ✅ **Complete CRUD Operations** - Create, Read, Update, Delete todos
- ✅ **Filtering & Searching** - Filter by priority, completion status, and search by text
- ✅ **Pagination** - Built-in pagination support
- ✅ **Authentication** - Token-based authentication for secure API access
- ✅ **Comprehensive Validation** - Input validation with clear error messages
- ✅ **Error Handling** - Proper error responses with meaningful messages
- ✅ **Logging** - Structured logging for all operations
- ✅ **CORS Support** - Cross-Origin Resource Sharing enabled
- ✅ **Security Best Practices** - Environment-based configuration, secure middleware
- ✅ **Test Coverage** - Comprehensive test suite with 20+ tests
- ✅ **Documentation** - Full API documentation with examples

## Project Structure

```
backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── conftest.py              # Pytest configuration
├── todo_api/                # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── __init__.py
└── todos/                   # Todo app
    ├── models.py            # Todo model definition
    ├── views.py             # API ViewSet
    ├── serializers.py       # Request/Response serializers
    ├── urls.py              # Todo app URLs
    ├── tests.py             # Comprehensive tests
    ├── apps.py              # App configuration
    └── migrations/          # Database migrations
```

## Installation

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### 2. Setup

```bash
# Clone the repository (if applicable)
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# At minimum, set:
# - SECRET_KEY (generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
# - Database credentials (DB_NAME, DB_USER, DB_PASSWORD)
```

### 3. Database Setup

```bash
# Create database (if using PostgreSQL locally)
psql -U postgres -c "CREATE DATABASE todos_db;"

# Run migrations
python manage.py migrate

# Create superuser (optional, for Django admin)
python manage.py createsuperuser
```

### 4. Create API Token (for authentication)

```bash
python manage.py shell

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create a user
user = User.objects.create_user(username='testuser', password='testpass123')

# Generate token
token = Token.objects.create(user=user)
print(token.key)  # Use this token for API requests
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Access the API at: `http://localhost:8000/api/`

## API Endpoints

### Authentication

Include the token in the `Authorization` header:
```
Authorization: Token YOUR_TOKEN_HERE
```

### Todo Endpoints

All endpoints require authentication.

#### List Todos
```http
GET /api/todos/
```

Query Parameters:
- `completed` (true/false) - Filter by completion status
- `priority` (low/medium/high) - Filter by priority
- `search` (text) - Search in title and description
- `page` (number) - Pagination (default: 1)

Example:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/todos/?completed=false&priority=high"
```

#### Create Todo
```http
POST /api/todos/
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "due_date": "2025-12-31T23:59:59Z",
  "completed": false
}
```

Response (201):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "due_date": "2025-12-31T23:59:59Z",
  "completed": false,
  "created_at": "2025-05-15T10:30:00Z",
  "updated_at": "2025-05-15T10:30:00Z"
}
```

#### Retrieve Todo
```http
GET /api/todos/{id}/
```

#### Update Todo (Full)
```http
PUT /api/todos/{id}/
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59Z",
  "completed": true
}
```

#### Partial Update Todo
```http
PATCH /api/todos/{id}/
Content-Type: application/json

{
  "priority": "high",
  "completed": true
}
```

#### Delete Todo
```http
DELETE /api/todos/{id}/
```

Response (204 No Content)

#### Mark Todo as Completed
```http
PATCH /api/todos/{id}/complete/
```

Response (200):
```json
{
  "status": "todo marked as completed",
  "todo": { ... }
}
```

#### Mark Todo as Incomplete
```http
PATCH /api/todos/{id}/uncomplete/
```

Response (200):
```json
{
  "status": "todo marked as incomplete",
  "todo": { ... }
}
```

## Todo Model

### Fields

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| id | Integer | No | Auto | Primary key |
| title | String(255) | Yes | - | Todo title |
| description | Text | No | Empty | Optional description |
| completed | Boolean | No | False | Completion status |
| priority | Choice | No | low | One of: low, medium, high |
| due_date | DateTime | No | Null | Optional due date |
| created_at | DateTime | No | Auto | Timestamp created |
| updated_at | DateTime | No | Auto | Timestamp updated |

### Priority Levels
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=todos

# Run specific test class
pytest todos/tests.py::TodoAPITests

# Run specific test
pytest todos/tests.py::TodoAPITests::test_list_todos_returns_all
```

### Test Coverage

The test suite includes:
- ✅ Authentication tests
- ✅ List/filter/search tests
- ✅ CRUD operation tests
- ✅ Validation tests
- ✅ Error handling tests
- ✅ Permission tests
- ✅ Model tests

Current test count: 20+ comprehensive tests

## Configuration

### Environment Variables

Create a `.env` file in the backend directory (copy from `.env.example`):

```bash
# Django
SECRET_KEY=your-secret-key-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=todos_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Security (for production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

## Security

This API implements the following security measures:

1. **Authentication** - Token-based authentication via Django REST Framework
2. **Authorization** - All endpoints require authentication
3. **Input Validation** - Pydantic/DRF serializer validation
4. **CSRF Protection** - Django CSRF middleware enabled
5. **CORS** - Whitelisted allowed origins
6. **SQL Injection Prevention** - Django ORM with parameterized queries
7. **Secret Management** - Secrets via environment variables
8. **Rate Limiting** - Can be added with django-ratelimit
9. **Logging** - All operations logged for audit trail

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Set `SECRET_KEY` to a secure random value
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Update `CORS_ALLOWED_ORIGINS` for your frontend
- [ ] Enable SSL/HTTPS (`SECURE_SSL_REDIRECT=True`)
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Use external database (not SQLite)
- [ ] Set up proper logging
- [ ] Run `python manage.py collectstatic`
- [ ] Run tests before deployment
- [ ] Set up database backups
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up monitoring and alerting

### Gunicorn Deployment

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn todo_api.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Docker Deployment

See `Dockerfile` for containerization (if available).

## Code Quality

- **Linting**: `ruff check`
- **Formatting**: `black` (configured)
- **Type Checking**: mypy (optional)
- **Test Coverage**: 90%+

Run quality checks:
```bash
ruff check .
black . --check
mypy . (if configured)
```

## Common Issues

### Database Connection Error
```
psycopg2.OperationalError: could not connect to server
```
Solution: Ensure PostgreSQL is running and .env has correct DB credentials.

### Token Authentication Failed
```
{"detail":"Invalid token."}
```
Solution: Ensure you're sending a valid token in the Authorization header.

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
Solution: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in .env.

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests to ensure they pass
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions:
1. Check this README
2. Review test files for usage examples
3. Check Django and DRF documentation
4. Open an issue in the repository

## API Documentation

Full interactive API documentation available at:
- Swagger UI: `/api/docs/` (if added)
- ReDoc: `/api/redoc/` (if added)

To add these, install `drf-spectacular`:
```bash
pip install drf-spectacular
```

And add to INSTALLED_APPS in settings.py.

---

**Last Updated**: May 2025
**Version**: 1.0.0
**Status**: Production Ready
