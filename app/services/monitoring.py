"""Monitoring service for application health and metrics."""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import deque
import asyncio

logger = logging.getLogger(__name__)


class HealthMonitor:
    """Monitor application health and collect metrics."""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.request_history: deque = deque(maxlen=max_history)
        self.error_history: deque = deque(maxlen=max_history)
        self.start_time = datetime.utcnow()
    
    def record_request(self, endpoint: str, status_code: int, response_time: float):
        """Record a request for monitoring."""
        self.request_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time": response_time
        })
    
    def record_error(self, error_type: str, error_message: str, endpoint: str = None):
        """Record an error for monitoring."""
        self.error_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "endpoint": endpoint
        })
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics and statistics."""
        uptime = datetime.utcnow() - self.start_time
        total_requests = len(self.request_history)
        
        if total_requests > 0:
            avg_response_time = sum(r["response_time"] for r in self.request_history) / total_requests
            success_rate = sum(1 for r in self.request_history if 200 <= r["status_code"] < 300) / total_requests * 100
        else:
            avg_response_time = 0
            success_rate = 100
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "total_requests": total_requests,
            "total_errors": len(self.error_history),
            "average_response_time": avg_response_time,
            "success_rate": success_rate,
            "recent_errors": list(self.error_history)[-10:] if self.error_history else []
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check."""
        checks = {}
        
        # Check response times
        if self.request_history:
            recent_response_times = [r["response_time"] for r in list(self.request_history)[-10:]]
            avg_recent = sum(recent_response_times) / len(recent_response_times)
            if avg_recent > 1.0:  # 1 second threshold
                checks["response_time"] = {
                    "status": "warning",
                    "message": f"High average response time: {avg_recent:.2f}s"
                }
            else:
                checks["response_time"] = {"status": "healthy", "average": avg_recent}
        else:
            checks["response_time"] = {"status": "unknown", "message": "No requests recorded"}
        
        # Check error rate
        if self.request_history:
            recent_errors = sum(1 for r in list(self.request_history)[-100:] if r["status_code"] >= 500)
            error_rate = recent_errors / min(len(self.request_history), 100) * 100
            if error_rate > 5:  # 5% error rate threshold
                checks["error_rate"] = {
                    "status": "critical",
                    "message": f"High error rate: {error_rate:.1f}%"
                }
            elif error_rate > 1:
                checks["error_rate"] = {
                    "status": "warning",
                    "message": f"Elevated error rate: {error_rate:.1f}%"
                }
            else:
                checks["error_rate"] = {"status": "healthy", "rate": error_rate}
        else:
            checks["error_rate"] = {"status": "unknown", "message": "No requests recorded"}
        
        return {
            "status": "healthy" if all(c.get("status") == "healthy" for c in checks.values()) else "degraded",
            "checks": checks,
            "metrics": self.get_metrics()
        }


# Global health monitor instance
health_monitor = HealthMonitor()