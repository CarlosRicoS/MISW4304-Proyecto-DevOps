# MISW4304-Proyecto-DevOps

A Flask REST API project demonstrating modern Python web development practices.

## Project Overview

This project is a Flask-based REST API that showcases the integration of essential Flask extensions for building production-ready web applications.

## Technology Stack

- **Python**: 3.8 or higher (tested with 3.12.3)
- **Flask**: 3.0.0 - Web framework
- **Flask-SQLAlchemy**: 3.1.1 - ORM for database operations
- **Flask-RESTful**: 0.3.10 - REST API framework
- **Marshmallow**: 3.20.0 - Object serialization/deserialization
- **Flask-Marshmallow**: 1.2.0 - Flask integration for Marshmallow
- **Marshmallow-SQLAlchemy**: 1.0.0 - SQLAlchemy integration for Marshmallow
- **Flask-JWT-Extended**: 4.6.0 - JWT authentication

## Project Structure

```
.
├── app.py              # Main application file with Flask app factory
├── config.py           # Configuration settings for different environments
├── models.py           # SQLAlchemy database models
├── schemas.py          # Marshmallow schemas for serialization
├── resources.py        # Flask-RESTful API resources/endpoints
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CarlosRicoS/MISW4304-Proyecto-DevOps.git
   cd MISW4304-Proyecto-DevOps
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

**Development mode**:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health` - Check API status
  ```bash
  curl http://localhost:5000/health
  ```

### Authentication
- **POST** `/api/login` - Get JWT access token
  ```bash
  curl -X POST http://localhost:5000/api/login \
    -H "Content-Type: application/json" \
    -d '{"username":"your_username"}'
  ```

### Users
- **GET** `/api/users` - Get all users
  ```bash
  curl http://localhost:5000/api/users
  ```

- **POST** `/api/users` - Create a new user
  ```bash
  curl -X POST http://localhost:5000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username":"john_doe","email":"john@example.com","password_hash":"hashed_pass"}'
  ```

- **GET** `/api/users/<id>` - Get a specific user (requires JWT)
  ```bash
  curl http://localhost:5000/api/users/1 \
    -H "Authorization: Bearer YOUR_JWT_TOKEN"
  ```

- **DELETE** `/api/users/<id>` - Delete a user (requires JWT)
  ```bash
  curl -X DELETE http://localhost:5000/api/users/1 \
    -H "Authorization: Bearer YOUR_JWT_TOKEN"
  ```

## Configuration

The application supports different configurations for development and production environments. Configuration settings can be modified in `config.py`:

- `SECRET_KEY`: Flask secret key
- `SQLALCHEMY_DATABASE_URI`: Database connection string (default: SQLite)
- `JWT_SECRET_KEY`: JWT token secret key

Environment variables:
- `SECRET_KEY`: Override default secret key
- `DATABASE_URL`: Override default database URL
- `JWT_SECRET_KEY`: Override default JWT secret key

## Features Demonstrated

1. **Flask Application Factory Pattern**: Configurable app creation for different environments
2. **SQLAlchemy ORM**: Database models with relationships
3. **RESTful API**: Clean resource-based API design with Flask-RESTful
4. **Data Validation**: Marshmallow schemas for request/response validation
5. **JWT Authentication**: Secure endpoints with JWT tokens
6. **Configuration Management**: Environment-based configuration

## Development

The application uses SQLite as the default database for development. The database file (`app.db`) is automatically created when you first run the application.

## Security Notes

⚠️ **Important**: This is a demonstration project. For production use:
- Change all secret keys
- Use environment variables for sensitive data
- Implement proper password hashing
- Use a production WSGI server (e.g., Gunicorn)
- Configure HTTPS
- Implement rate limiting
- Add input validation and sanitization

## License

This project is for educational purposes.