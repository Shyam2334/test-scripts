"""Unit tests for diagnostic utilities."""
import pytest
import logging
from app.utils.diagnostics import (
    log_execution_time,
    validate_input,
    DiagnosticContext,
    check_system_health
)


@pytest.fixture
def caplog_info(caplog):
    """Set logging level to INFO for tests."""
    caplog.set_level(logging.INFO)
    return caplog


def test_log_execution_time_sync_success(caplog_info):
    """Test execution time logging for successful sync function."""
    @log_execution_time
    def test_func():
        return "success"
    
    result = test_func()
    assert result == "success"
    assert "test_func executed successfully" in caplog_info.text


def test_log_execution_time_sync_failure(caplog_info):
    """Test execution time logging for failed sync function."""
    @log_execution_time
    def test_func():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        test_func()
    
    assert "test_func failed after" in caplog_info.text


@pytest.mark.asyncio
async def test_log_execution_time_async_success(caplog_info):
    """Test execution time logging for successful async function."""
    @log_execution_time
    async def test_func():
        return "success"
    
    result = await test_func()
    assert result == "success"
    assert "test_func executed successfully" in caplog_info.text


def test_validate_input_success():
    """Test input validation decorator with valid input."""
    @validate_input(lambda x: x > 0, "Value must be positive")
    def test_func(value):
        return value * 2
    
    result = test_func(5)
    assert result == 10


def test_validate_input_failure():
    """Test input validation decorator with invalid input."""
    @validate_input(lambda x: x > 0, "Value must be positive")
    def test_func(value):
        return value * 2
    
    with pytest.raises(ValueError, match="Value must be positive"):
        test_func(-5)


def test_diagnostic_context_success(caplog_info):
    """Test DiagnosticContext with successful operation."""
    with DiagnosticContext("test_operation") as ctx:
        assert ctx.operation_name == "test_operation"
        assert ctx.diagnostics["success"] is False
    
    assert ctx.diagnostics["success"] is True
    assert ctx.diagnostics["error"] is None
    assert "Starting operation: test_operation" in caplog_info.text
    assert "completed successfully" in caplog_info.text


def test_diagnostic_context_failure(caplog_info):
    """Test DiagnosticContext with failed operation."""
    with pytest.raises(ValueError):
        with DiagnosticContext("test_operation") as ctx:
            raise ValueError("Test error")
    
    assert ctx.diagnostics["success"] is False
    assert "Test error" in ctx.diagnostics["error"]
    assert ctx.diagnostics["traceback"] is not None
    assert "Operation test_operation failed" in caplog_info.text


def test_check_system_health():
    """Test system health check function."""
    health = check_system_health()
    
    assert "timestamp" in health
    assert "checks" in health
    assert "logging" in health["checks"]
    assert "file_system" in health["checks"]
    assert "memory" in health["checks"]
    
    # Logging should always work in tests
    assert health["checks"]["logging"]["status"] == "ok"