# Makefile for Unix-like systems
VENV := env
REQUIREMENTS := requirements.txt

.PHONY: setup env clean

# Default target
setup: env

# Setup virtual environment and install dependencies
env:
	@echo "Setting up Python virtual environment and installing dependencies..."
	@python3 -m venv $(VENV) && \
		. $(VENV)/bin/activate && \
		pip install -r $(REQUIREMENTS) && \
		python app.py

# Clean up the environment by removing it
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)