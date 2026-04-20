"""
Pytest configuration file for test execution
Provides fixtures and configurations for all tests
"""

import pytest
import logging
import os
from datetime import datetime


# Create logs directory if not exists
logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(logs_dir, f'test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def pytest_configure(config):
    """
    Pytest hook - runs before test collection

    Creates necessary directories for logs and screenshots
    """
    # Create logs directory if not exists
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Create screenshots directory if not exists
    screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)

    logger.info("Test execution started")


def pytest_runtest_setup(item):
    """
    Pytest hook - runs before each test

    Logs test name and description
    """
    logger.info(f"Setting up test: {item.name}")


def pytest_runtest_teardown(item):
    """
    Pytest hook - runs after each test

    Logs test completion
    """
    logger.info(f"Tearing down test: {item.name}")


@pytest.fixture(scope="session")
def test_session_info():
    """
    Fixture providing test session information

    Returns:
        dict: Session information
    """
    session_info = {
        "start_time": datetime.now(),
        "test_environment": "UAT",
        "app_url": "https://uatamrit.piramalswasthya.org/aam/"
    }
    return session_info


@pytest.fixture(scope="function")
def test_data():
    """
    Fixture providing test data for login tests

    Returns:
        dict: Test data
    """
    data = {
        "valid_username": "mokrong",
        "valid_password": "Test@123",
        "invalid_username": "invaliduser",
        "invalid_password": "invalidpass",
        "app_url": "https://uatamrit.piramalswasthya.org/aam/"
    }
    return data
