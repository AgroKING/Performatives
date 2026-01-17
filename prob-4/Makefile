.PHONY: install test run migrate coverage clean format lint help

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
UVICORN := uvicorn
ALEMBIC := alembic

help:
	@echo "ATS API - Makefile Commands"
	@echo "============================"
	@echo "install       - Install dependencies"
	@echo "test          - Run tests"
	@echo "test-verbose  - Run tests with verbose output"
	@echo "coverage      - Run tests with coverage report"
	@echo "run           - Run development server"
	@echo "run-prod      - Run production server"
	@echo "migrate       - Run database migrations"
	@echo "migrate-create - Create new migration"
	@echo "format        - Format code with black and isort"
	@echo "lint          - Run linters (flake8, mypy, pylint)"
	@echo "clean         - Remove cache and build files"
	@echo "docker-up     - Start Docker containers"
	@echo "docker-down   - Stop Docker containers"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	$(PYTEST)

test-verbose:
	$(PYTEST) -v -s

coverage:
	$(PYTEST) --cov=app --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

run:
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

run-prod:
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --workers 4

migrate:
	$(ALEMBIC) upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	$(ALEMBIC) revision --autogenerate -m "$$msg"

migrate-downgrade:
	$(ALEMBIC) downgrade -1

format:
	black app tests
	isort app tests
	@echo "Code formatted successfully!"

lint:
	flake8 app tests --max-line-length=100 --exclude=alembic
	mypy app
	pylint app --max-line-length=100
	@echo "Linting complete!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	@echo "Cleaned up cache and build files!"

docker-up:
	docker-compose up -d
	@echo "Docker containers started!"

docker-down:
	docker-compose down
	@echo "Docker containers stopped!"

docker-logs:
	docker-compose logs -f

docker-rebuild:
	docker-compose up -d --build
	@echo "Docker containers rebuilt!"

# Database commands
db-shell:
	$(PYTHON) -c "from app.database import engine; import sqlalchemy; print(sqlalchemy.inspect(engine).get_table_names())"

# Development helpers
shell:
	$(PYTHON)

freeze:
	$(PIP) freeze > requirements.txt
	@echo "Requirements frozen!"

# All-in-one commands
setup: install migrate
	@echo "Setup complete! Run 'make run' to start the server."

check: format lint test
	@echo "All checks passed!"
