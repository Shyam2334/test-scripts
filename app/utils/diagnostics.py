"""Diagnostic utilities for troubleshooting issues."""
import logging
import functools
import time
import asyncio
from typing import Any, Callable, Dict, Optional
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)


def log_execution_time(func: Callable) -> Callable:
    """Decorator to log function execution time."""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed successfully in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}", exc_info=True)
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed successfully in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}", exc_info=True)
            raise
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def validate_input(validation_func: Callable[[Any], bool], error_message: str) -> Callable:
    """Decorator to validate function inputs."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args and not validation_func(args[0]):
                logger.error(f"Input validation failed for {func.__name__}: {error_message}")
                raise ValueError(error_message)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class DiagnosticContext:
    """Context manager for diagnostic information collection."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time: Optional[float] = None
        self.diagnostics: Dict[str, Any] = {
            "operation": operation_name,
            "start_time": None,
            "end_time": None,
            "duration": None,
            "success": False,
            "error": None,
            "traceback": None
        }
    
    def __enter__(self):
        self.start_time = time.time()
        self.diagnostics["start_time"] = datetime.utcnow().isoformat()
        logger.info(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        self.diagnostics["end_time"] = datetime.utcnow().isoformat()
        self.diagnostics["duration"] = end_time - self.start_time
        
        if exc_type is None:
            self.diagnostics["success"] = True
            logger.info(f"Operation {self.operation_name} completed successfully in {self.diagnostics['duration']:.3f}s")
        else:
            self.diagnostics["success"] = False
            self.diagnostics["error"] = str(exc_val)
            self.diagnostics["traceback"] = traceback.format_exc()
            logger.error(f"Operation {self.operation_name} failed after {self.diagnostics['duration']:.3f}s: {exc_val}")
        
        return False  # Don't suppress exceptions


def check_system_health() -> Dict[str, Any]:
    """Perform basic system health checks."""
    health_status = {
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check if logging is working
    try:
        logger.info("Health check: Testing logging")
        health_status["checks"]["logging"] = {"status": "ok"}
    except Exception as e:
        health_status["checks"]["logging"] = {"status": "error", "message": str(e)}
    
    # Check file system access
    try:
        with open("app.log", "a") as f:
            f.write(f"Health check at {datetime.utcnow().isoformat()}\n")
        health_status["checks"]["file_system"] = {"status": "ok"}
    except Exception as e:
        health_status["checks"]["file_system"] = {"status": "error", "message": str(e)}
    
    # Check memory usage
    try:
        import psutil
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            health_status["checks"]["memory"] = {
                "status": "warning",
                "message": f"High memory usage: {memory.percent}%"
            }
        else:
            health_status["checks"]["memory"] = {"status": "ok", "usage_percent": memory.percent}
    except ImportError:
        health_status["checks"]["memory"] = {"status": "unknown", "message": "psutil not installed"}
    except Exception as e:
        health_status["checks"]["memory"] = {"status": "error", "message": str(e)}
    
    return health_status