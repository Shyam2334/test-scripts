"""Unit tests for logging utilities."""
import logging
import os
import tempfile
import pytest
from app.utils.logging import setup_logging


def test_setup_logging_default():
    """Test default logging setup."""
    logger = setup_logging()
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO
    assert len(logger.handlers) >= 1


def test_setup_logging_custom_level():
    """Test logging setup with custom level."""
    logger = setup_logging(log_level="DEBUG")
    assert logger.level == logging.DEBUG


def test_setup_logging_with_file():
    """Test logging setup with file handler."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        logger = setup_logging(log_file=tmp_path)
        logger.info("Test message")
        
        # Close all handlers to release file handles
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
        
        # Check if log file was created and contains the message
        assert os.path.exists(tmp_path)
        with open(tmp_path, 'r') as f:
            content = f.read()
            assert "Test message" in content
    finally:
        # Clean up handlers before attempting to delete the file
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            if isinstance(handler, logging.FileHandler) and handler.baseFilename == tmp_path:
                handler.close()
                root_logger.removeHandler(handler)
        
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_setup_logging_without_file():
    """Test logging setup without file handler."""
    logger = setup_logging(log_file=None)
    # Should only have console handler
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 0