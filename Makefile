# Makefile

# Create and activate virtual environment and install dependencies
setup:
	@echo "Creating virtual environment..."
	python3 -m venv env
	@echo "Activating virtual environment and installing dependencies..."
	${shell source env/bin/activate; pip install -r requirements.txt; deactivate;}

# Clean up the environment by removing it
clean:
	@echo "Cleaning up..."
	rm -rf env

.PHONY: setup clean
