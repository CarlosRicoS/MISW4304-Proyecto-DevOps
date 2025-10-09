# Makefile for DevOps Project
# Python Flask application with hexagonal architecture

# Virtual environment settings
VENV_NAME = venv
VENV_PATH = ./$(VENV_NAME)
PYTHON = $(VENV_PATH)/bin/python
PIP = $(VENV_PATH)/bin/pip

.PHONY: help venv install dev test test-unit test-integration lint format clean run docker-build docker-run clean-venv

# Default target
help:
	@echo "Available commands:"
	@echo "  venv             - Create virtual environment"
	@echo "  install          - Install dependencies (creates venv if needed)"
	@echo "  dev              - Install development dependencies"
	@echo "  run              - Run the application in development mode"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint             - Run code linting"
	@echo "  format           - Format code with black"
	@echo "  clean            - Clean up temporary files"
	@echo "  clean-venv       - Remove virtual environment"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run application in Docker"
	@echo "  ping             - Test ping endpoint"
	@echo "  health           - Test health endpoint"
	@echo ""
	@echo "Quick start for new users:"
	@echo "  1. make install  - Sets up everything (venv + dependencies)"
	@echo "  2. make run      - Start the application"
	@echo "  3. make test     - Run tests"

# Virtual environment setup
venv:
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_NAME); \
		echo "Virtual environment created at $(VENV_PATH)"; \
		echo "To activate manually, run: source $(VENV_PATH)/bin/activate"; \
	else \
		echo "Virtual environment already exists at $(VENV_PATH)"; \
	fi

# Installation
install: venv
	@echo "Installing dependencies in virtual environment..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed successfully!"
	@echo "To activate the virtual environment manually: source $(VENV_PATH)/bin/activate"

dev: install
	@echo "Installing development dependencies..."
	$(PIP) install pytest pytest-cov black flake8 coverage

# Running the application
run: venv
	@if [ ! -f "$(VENV_PATH)/bin/python" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	$(PYTHON) main.py

# Testing
test: test-unit test-integration

test-unit: venv
	$(PYTHON) tests/run_tests.py

test-integration: venv
	$(PYTHON) tests/run_tests.py

test-coverage: venv
	$(PYTHON) -m coverage run tests/run_tests.py && $(PYTHON) -m coverage report && $(PYTHON) -m coverage html

# Code quality
lint: venv
	$(VENV_PATH)/bin/flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__

format: venv
	$(VENV_PATH)/bin/black src/ tests/ --line-length=100

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/

clean-venv:
	@if [ -d "$(VENV_PATH)" ]; then \
		echo "Removing virtual environment..."; \
		rm -rf $(VENV_PATH); \
		echo "Virtual environment removed."; \
	else \
		echo "No virtual environment found."; \
	fi

# Docker commands
docker-build:
	docker build -t devops-project .

docker-run:
	docker run -p 5000:5000 devops-project

# API testing
ping:
	curl -X GET http://localhost:5000/ping

health:
	curl -X GET http://localhost:5000/health

# Development workflow
dev-setup: dev
	@echo "Development environment setup complete!"
	@echo "Virtual environment created at: $(VENV_PATH)"
	@echo "To activate manually: source $(VENV_PATH)/bin/activate"
	@echo ""
	@echo "Quick commands:"
	@echo "  make run   - Start the application"
	@echo "  make test  - Run tests"
	@echo "  make ping  - Test the ping endpoint"

# Quick check - runs tests and linting
check: test lint
	@echo "All checks passed!"

# Setup command for new users
setup: install
	@echo ""
	@echo "🎉 Project setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make run' to start the application"
	@echo "  2. Run 'make test' to run tests"
	@echo "  3. Run 'make ping' to test the ping endpoint"
	@echo ""
	@echo "To manually activate the virtual environment:"
	@echo "  source $(VENV_PATH)/bin/activate"
