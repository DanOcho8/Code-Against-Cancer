# Makefile

# Composite target: Set up virtual environment, install dependencies, run migrations, and start the server
run: venv install migrate runserver

# Detect operating system
UNAME := $(shell uname)

# Define the virtual environment activation command and Python command based on OS
ifeq ($(UNAME), Linux)
    ACTIVATE_VENV = source venv/bin/activate
    PYTHON = python
else ifeq ($(UNAME), Darwin)  # macOS
    ACTIVATE_VENV = source venv/bin/activate
    PYTHON = python3
else ifeq ($(OS), Windows_NT)  # Windows
    ACTIVATE_VENV = venv\Scripts\activate
    PYTHON = python
endif

# Run migrations
migrate:
	@$(ACTIVATE_VENV) && $(PYTHON) manage.py migrate

# Run the Django development server
runserver:
	@$(ACTIVATE_VENV) && $(PYTHON) manage.py runserver

# Run tests
test:
	@$(ACTIVATE_VENV) && $(PYTHON) manage.py test

# Install dependencies from requirements.txt
install:
	@$(ACTIVATE_VENV) && pip install -r requirements.txt

# Set up virtual environment
venv:
	$(PYTHON) -m venv venv

# Activate virtual environment
activate:
	@$(ACTIVATE_VENV)

# Clean up __pycache__ files
clean:
	find . -name "__pycache__" -exec rm -rf {} +

.PHONY: run migrate runserver test install venv activate clean
