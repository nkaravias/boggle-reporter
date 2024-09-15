# Default target
.DEFAULT_GOAL := help

# Environment variables
export PYTHON = python
export CONFIG_DIR = resources
export OUTPUT_TYPE ?= rich

# Help command
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Install dependencies
install: ## Install project dependencies
	$(PYTHON) -m pip install -r requirements.txt

# Install test dependencies
install-test: ## Install test dependencies
	$(PYTHON) -m pip install -r requirements-test.txt

# Run tests
test: ## Run pytest suites
	$(PYTHON) -m pytest --cov=src --cov-report=html -v tests/unit/

# Generate generic overview report
report-generic: ## Generate generic overview report
	$(PYTHON) src/boggle_tracker/main.py $(CONFIG_DIR)/config.json --report generic_overview --output $(OUTPUT_TYPE)

# Generate target allocation report
report-target: ## Generate target allocation report
	$(PYTHON) src/boggle_tracker/main.py $(CONFIG_DIR)/config.json --report target_allocation --target-allocation $(CONFIG_DIR)/target_allocation_config.json --output $(OUTPUT_TYPE)

# Generate total target allocation report
report-total-target: ## Generate total target allocation report
	$(PYTHON) src/boggle_tracker/main.py $(CONFIG_DIR)/config.json --report total_target_allocation --target-allocation $(CONFIG_DIR)/target_allocation_config.json --exchange-rates $(CONFIG_DIR)/exchange_rates.json --output $(OUTPUT_TYPE)

# Generate all reports
report-all: report-generic report-target report-total-target ## Generate all reports

# Clean up generated files
clean: ## Remove generated files
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: help install install-test test report-generic report-target report-total-target report-all clean