# MISW4304-Proyecto-DevOps

A Flask REST API project implementing hexagonal architecture with comprehensive health checks and DevOps best practices.

## Project Overview

This project is a Flask-based REST API that demonstrates hexagonal architecture (ports and adapters) with proper separation of concerns, dependency injection, and comprehensive testing. It includes health check endpoints for monitoring and a complete DevOps setup with Makefile automation.

## Architecture

The project follows **Hexagonal Architecture** (also known as Ports and Adapters architecture) principles:

- **Domain Layer**: Core business logic and entities (`src/domain/`)
- **Application Layer**: Use cases and application services (`src/application/`)
- **Infrastructure Layer**: Database repositories and external services (`src/infrastructure/`)
- **Adapters Layer**: HTTP controllers and external interfaces (`src/adapters/`)
- **Dependency Injection**: Clean dependency management (`src/container.py`)

## Technology Stack

- **Python**: 3.8 or higher (tested with 3.12.3)
- **Flask**: 3.0.0 - Web framework
- **Flask-SQLAlchemy**: 3.1.1 - ORM for database operations
- **Flask-RESTful**: 0.3.10 - REST API framework
- **Marshmallow**: 3.20.0 - Object serialization/deserialization
- **Flask-Marshmallow**: 1.2.0 - Flask integration for Marshmallow
- **Marshmallow-SQLAlchemy**: 1.0.0 - SQLAlchemy integration for Marshmallow
- **Flask-JWT-Extended**: 4.6.0 - JWT authentication
- **pytest**: 7.4.3 - Testing framework
- **pytest-cov**: 4.1.0 - Coverage reporting
- **black**: 23.9.1 - Code formatting
- **flake8**: 6.1.0 - Code linting

## Project Structure

```
MISW4304-Proyecto-DevOps/
├── src/                          # Source code organized by layers
│   ├── domain/                   # Domain layer (entities, business logic)
│   │   ├── entities.py          # Domain entities (HealthStatus)
│   │   └── ports.py             # Service interfaces
│   ├── application/              # Application layer (use cases)
│   │   └── health_service.py    # Health check operations
│   ├── infrastructure/           # Infrastructure layer (databases, external services)
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── repositories.py      # Future repository implementations
│   │   └── health_check.py      # Health check implementations
│   ├── adapters/                 # Adapters layer (HTTP, external APIs)
│   │   ├── health_controller.py # Health check HTTP controllers
│   │   └── schemas.py           # Request/response schemas
│   ├── container.py             # Dependency injection container
│   ├── app.py                   # Application factory
│   └── config.py                # Configuration management
├── tests/                        # Test suite
│   ├── test_health_service.py   # Unit tests for health service
│   ├── test_integration.py      # Integration tests
│   └── run_tests.py             # Test runner
├── main.py                       # Main application entry point
├── requirements.txt              # Python dependencies
├── Makefile                      # Automation commands
├── Dockerfile                    # Container configuration
├── .dockerignore                # Docker ignore file
└── README.md                     # This file
```

## Health Check Endpoints

The application provides comprehensive health checking capabilities:

### 1. Ping Endpoint
- **URL**: `/ping`
- **Method**: `GET`, `HEAD`
- **Description**: Simple connectivity check
- **Response**: 
  ```json
  {
    "status": "ok",
    "message": "pong",
    "timestamp": "2024-01-01T12:00:00.000Z"
  }
  ```

### 2. Health Check Endpoint
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Comprehensive health status including database connectivity
- **Response**:
  ```json
  {
    "status": "healthy|unhealthy|error",
    "message": "Status description",
    "timestamp": "2024-01-01T12:00:00.000Z"
  }
  ```

## Quick Start

### Using Makefile (Recommended)

**For new users - Complete setup in one command:**
```bash
make setup     # Creates virtual environment and installs all dependencies
```

**Alternative step-by-step setup:**

1. **Setup development environment:**
   ```bash
   make dev-setup
   ```

2. **Run the application:**
   ```bash
   make run
   ```

3. **Test the application:**
   ```bash
   make test
   ```

4. **Test health endpoints:**
   ```bash
   make ping
   make health
   ```

### Manual Setup

**With Virtual Environment (Recommended):**

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

**Without Virtual Environment:**

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**

   ```bash
   python main.py
   ```

3. **Run tests:**

   ```bash
   python tests/run_tests.py
   ```

## Docker Usage

```bash
# Build the Docker image
make docker-build

# Run the container
make docker-run
```

## API Endpoints

### Health Check

- **GET** `/ping` - Simple ping check

  ```bash
  curl http://localhost:5000/ping
  ```

- **GET** `/health` - Comprehensive health check

  ```bash
  curl http://localhost:5000/health
  ```

## Makefile Commands

The project includes a comprehensive Makefile for automation:

```bash
make help              # Show all available commands
make install           # Install dependencies
make dev               # Install development dependencies
make run               # Run the application
make test              # Run all tests
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
make test-coverage     # Run tests with coverage report
make lint              # Run code linting
make format            # Format code with black
make clean             # Clean up temporary files
make docker-build      # Build Docker image
make docker-run        # Run in Docker
make ping              # Test ping endpoint
make health            # Test health endpoint
make dev-setup         # Complete development setup
make check             # Run tests and linting
```

## Testing

The project includes comprehensive testing:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test the complete API endpoints
- **Coverage Reports**: Track test coverage

Run specific test types:

```bash
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test-coverage     # With coverage report
```

## Development

### Code Quality

The project enforces code quality through:

- **Black**: Code formatting
- **Flake8**: Code linting
- **pytest**: Testing framework
- **Coverage**: Test coverage tracking

### Development Workflow

1. Set up development environment:

   ```bash
   make dev-setup
   ```

2. Make your changes

3. Run quality checks:

   ```bash
   make check  # Runs tests and linting
   ```

4. Format code:

   ```bash
   make format
   ```

## Hexagonal Architecture Benefits

- **Testability**: Easy to unit test business logic without external dependencies
- **Flexibility**: Easy to swap implementations (database, external services)
- **Maintainability**: Clear separation of concerns
- **Domain Focus**: Business logic is isolated from technical concerns

## Configuration

The application supports multiple environments through configuration classes:

- **Development**: Debug mode enabled, SQLite database
- **Production**: Debug mode disabled, configurable database

Environment variables:

- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection URL
- `JWT_SECRET_KEY`: JWT signing key

## Docker Health Checks

The Docker container includes built-in health checks using the `/ping` endpoint, ensuring container orchestration platforms can properly monitor application health.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the hexagonal architecture patterns
4. Add tests for new functionality
5. Run `make check` to ensure quality
6. Submit a pull request

## License

This project is part of the MISW4304 DevOps course and is intended for educational purposes.