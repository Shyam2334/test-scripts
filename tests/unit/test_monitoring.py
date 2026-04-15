"""Unit tests for monitoring service."""
import pytest
from datetime import datetime
from app.services.monitoring import HealthMonitor


@pytest.fixture
def monitor():
    """Create a fresh HealthMonitor instance."""
    return HealthMonitor(max_history=10)


def test_record_request(monitor):
    """Test recording requests."""
    monitor.record_request("/test", 200, 0.1)
    monitor.record_request("/test", 500, 0.5)
    
    assert len(monitor.request_history) == 2
    assert monitor.request_history[0]["endpoint"] == "/test"
    assert monitor.request_history[0]["status_code"] == 200
    assert monitor.request_history[1]["status_code"] == 500


def test_record_error(monitor):
    """Test recording errors."""
    monitor.record_error("ValueError", "Test error", "/test")
    
    assert len(monitor.error_history) == 1
    assert monitor.error_history[0]["error_type"] == "ValueError"
    assert monitor.error_history[0]["error_message"] == "Test error"


def test_get_metrics_empty(monitor):
    """Test getting metrics with no data."""
    metrics = monitor.get_metrics()
    
    assert metrics["total_requests"] == 0
    assert metrics["total_errors"] == 0
    assert metrics["average_response_time"] == 0
    assert metrics["success_rate"] == 100
    assert metrics["recent_errors"] == []


def test_get_metrics_with_data(monitor):
    """Test getting metrics with recorded data."""
    monitor.record_request("/test1", 200, 0.1)
    monitor.record_request("/test2", 200, 0.2)
    monitor.record_request("/test3", 500, 0.3)
    monitor.record_error("TestError", "Something went wrong")
    
    metrics = monitor.get_metrics()
    
    assert metrics["total_requests"] == 3
    assert metrics["total_errors"] == 1
    assert metrics["average_response_time"] == pytest.approx(0.2, 0.01)
    assert metrics["success_rate"] == pytest.approx(66.67, 0.01)
    assert len(metrics["recent_errors"]) == 1


@pytest.mark.asyncio
async def test_health_check_healthy(monitor):
    """Test health check with healthy metrics."""
    # Record some healthy requests
    for i in range(5):
        monitor.record_request(f"/test{i}", 200, 0.1)
    
    health = await monitor.health_check()
    
    assert health["status"] == "healthy"
    assert health["checks"]["response_time"]["status"] == "healthy"
    assert health["checks"]["error_rate"]["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_check_degraded(monitor):
    """Test health check with degraded metrics."""
    # Record slow requests
    for i in range(5):
        monitor.record_request(f"/test{i}", 200, 1.5)
    
    health = await monitor.health_check()
    
    assert health["status"] == "degraded"
    assert health["checks"]["response_time"]["status"] == "warning"


@pytest.mark.asyncio
async def test_health_check_critical(monitor):
    """Test health check with critical metrics."""
    # Record many errors
    for i in range(10):
        monitor.record_request(f"/test{i}", 500, 0.1)
    
    health = await monitor.health_check()
    
    assert health["status"] == "degraded"
    assert health["checks"]["error_rate"]["status"] == "critical"


def test_max_history_limit(monitor):
    """Test that history respects max_history limit."""
    # Record more than max_history requests
    for i in range(15):
        monitor.record_request(f"/test{i}", 200, 0.1)
    
    assert len(monitor.request_history) == 10  # Should not exceed max_history