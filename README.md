# MISW4304-Proyecto-DevOps

A Flask REST API project implementing hexagonal architecture with comprehensive health checks, DevOps best practices, and AWS Elastic Beanstalk deployment automation.

## Project Overview

This project is a Flask-based REST API that demonstrates hexagonal architecture (ports and adapters) with proper separation of concerns, dependency injection, and comprehensive testing. It includes health check endpoints for monitoring, blacklist management functionality, and complete AWS Elastic Beanstalk deployment automation with various deployment strategies.

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
├── src/                                    # Source code organized by layers
│   ├── domain/                             # Domain layer (entities, business logic)
│   │   ├── entities.py                    # Domain entities (HealthStatus, Blacklist)
│   │   └── ports.py                       # Service interfaces
│   ├── application/                        # Application layer (use cases)
│   │   ├── health_service.py              # Health check operations
│   │   └── blacklist_service.py           # Blacklist management operations
│   ├── infrastructure/                     # Infrastructure layer (databases, external services)
│   │   ├── models.py                      # SQLAlchemy database models
│   │   ├── repositories.py                # Repository implementations
│   │   ├── health_check.py                # Health check implementations
│   │   └── migrations.py                  # Database migrations
│   ├── adapters/                           # Adapters layer (HTTP, external APIs)
│   │   ├── health_controller.py           # Health check HTTP controllers
│   │   ├── blacklist_controller.py        # Blacklist HTTP controllers
│   │   └── schemas.py                     # Request/response schemas
│   ├── utils/                              # Utility functions
│   │   └── jwt_utils.py                   # JWT authentication utilities
│   ├── container.py                       # Dependency injection container
│   ├── app.py                             # Application factory
│   └── config.py                          # Configuration management
├── tests/                                  # Test suite
│   ├── test_health_service.py             # Unit tests for health service
│   ├── test_blacklist_service.py          # Unit tests for blacklist service
│   └── run_tests.py                       # Test runner
├── .ebextensions/                          # AWS Elastic Beanstalk configurations
│   ├── app.config                         # Application configuration
│   ├── deployment.config                  # Deployment policies
│   ├── blue_green.config                  # Blue/Green deployment settings
│   ├── monitoring.config                  # CloudWatch monitoring setup
│   └── scaling.config                     # Auto-scaling configuration
├── .elasticbeanstalk/                      # EB CLI configuration
│   └── config.yml                         # Environment configuration
├── application.py                          # Main application entry point (WSGI)
├── requirements.txt                        # Python dependencies
├── .ebignore                              # EB deployment ignore patterns
├── .gitignore                             # Git ignore patterns
├── eb_init.sh                             # EB environment initialization script
├── eb_deploy_all_at_once.sh               # All-at-once deployment script
├── eb_deploy_rolling.sh                   # Rolling deployment script
├── eb_deploy_rolling_with_batch.sh        # Rolling with batch deployment script
├── eb_deploy_immutable.sh                 # Immutable deployment script
└── README.md                              # This file
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

## Quick Start
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
   python application.py
   ```

### API Endpoints - Blacklist Management

The application provides blacklist management capabilities for email blocking:

- **POST** `/blacklists` - Add email to blacklist
  - Requires JWT authentication
  - Request body: `{"email": "user@example.com", "app_uuid": "uuid", "blocked_reason": "reason"}`

- **GET** `/blacklists/<email>` - Check if email is blacklisted
  - Requires JWT authentication
  - Returns blacklist status and details

## Testing

The project includes comprehensive testing:

- **Unit Tests**:
    ```bash
    python3 tests/run_tests.py
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

## AWS Elastic Beanstalk Deployment

The project includes comprehensive AWS Elastic Beanstalk deployment automation with five different deployment strategies:

### Deployment Strategies

1. **All at Once**: Deploy to all instances simultaneously (fastest, brief downtime)
2. **Rolling**: Deploy in batches without additional instances
3. **Rolling with Additional Batch**: Deploy with extra capacity maintained
4. **Immutable**: Deploy to new instances, then swap (zero downtime, safest)

### Deployment Scripts

- `eb_init.sh` - Initialize and create EB environment
- `eb_deploy_*.sh` - Deploy using specific strategies

### Configuration Files

The `.ebextensions/` directory contains configuration for:
- Application settings and environment variables
- Deployment policies and strategies
- Auto-scaling rules
- CloudWatch monitoring and alarms
- Blue/Green deployment settings
- Traffic splitting configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the hexagonal architecture patterns
4. Add tests for new functionality
5. Run `make check` to ensure quality
6. Submit a pull request

## License

This project is part of the MISW4304 DevOps course and is intended for educational purposes.