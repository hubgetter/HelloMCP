"""
Real-time Agent Performance Dashboard Server

This MCP server provides real-time performance monitoring capabilities
for tracking agent metrics including response times, success rates,
error tracking, and request counts.
"""

from fastmcp import FastMCP
import time
import threading
from datetime import datetime
from collections import deque
from typing import Dict, List, Any
import json

# Performance metrics storage
class PerformanceMetrics:
    """
    Tracks and manages agent performance metrics in real-time.
    """
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_response_time": 0.0,
            "average_response_time": 0.0,
            "min_response_time": float('inf'),
            "max_response_time": 0.0,
            "error_rate": 0.0,
            "success_rate": 0.0,
            "uptime_seconds": 0,
            "start_time": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        self.request_history = deque(maxlen=max_history)
        self.error_log = deque(maxlen=50)
        self.lock = threading.Lock()
        self.server_start_time = time.time()

    def record_request(self, endpoint: str, response_time: float, success: bool, error_message: str = None):
        """
        Record a single request's performance metrics.

        Args:
            endpoint: The API endpoint called
            response_time: Time taken to process the request in seconds
            success: Whether the request was successful
            error_message: Error message if the request failed
        """
        with self.lock:
            self.metrics["total_requests"] += 1

            if success:
                self.metrics["successful_requests"] += 1
            else:
                self.metrics["failed_requests"] += 1
                if error_message:
                    self.error_log.append({
                        "timestamp": datetime.now().isoformat(),
                        "endpoint": endpoint,
                        "error": error_message
                    })

            # Update response time metrics
            self.metrics["total_response_time"] += response_time
            self.metrics["min_response_time"] = min(
                self.metrics["min_response_time"],
                response_time
            )
            self.metrics["max_response_time"] = max(
                self.metrics["max_response_time"],
                response_time
            )
            self.metrics["average_response_time"] = (
                self.metrics["total_response_time"] / self.metrics["total_requests"]
            )

            # Calculate rates
            if self.metrics["total_requests"] > 0:
                self.metrics["success_rate"] = (
                    self.metrics["successful_requests"] / self.metrics["total_requests"] * 100
                )
                self.metrics["error_rate"] = (
                    self.metrics["failed_requests"] / self.metrics["total_requests"] * 100
                )

            # Update uptime
            self.metrics["uptime_seconds"] = int(time.time() - self.server_start_time)
            self.metrics["last_updated"] = datetime.now().isoformat()

            # Add to request history
            self.request_history.append({
                "timestamp": datetime.now().isoformat(),
                "endpoint": endpoint,
                "response_time": round(response_time, 4),
                "success": success,
                "error": error_message
            })

    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        with self.lock:
            # Handle edge case where no requests have been made
            metrics_copy = self.metrics.copy()
            if metrics_copy["min_response_time"] == float('inf'):
                metrics_copy["min_response_time"] = 0.0

            # Round floating point values for readability
            metrics_copy["average_response_time"] = round(metrics_copy["average_response_time"], 4)
            metrics_copy["min_response_time"] = round(metrics_copy["min_response_time"], 4)
            metrics_copy["max_response_time"] = round(metrics_copy["max_response_time"], 4)
            metrics_copy["success_rate"] = round(metrics_copy["success_rate"], 2)
            metrics_copy["error_rate"] = round(metrics_copy["error_rate"], 2)

            return metrics_copy

    def get_request_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get recent request history."""
        with self.lock:
            history = list(self.request_history)
            if limit:
                history = history[-limit:]
            return history

    def get_error_log(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get recent error log entries."""
        with self.lock:
            errors = list(self.error_log)
            if limit:
                errors = errors[-limit:]
            return errors

    def reset_metrics(self):
        """Reset all performance metrics."""
        with self.lock:
            self.metrics = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_response_time": 0.0,
                "average_response_time": 0.0,
                "min_response_time": float('inf'),
                "max_response_time": 0.0,
                "error_rate": 0.0,
                "success_rate": 0.0,
                "uptime_seconds": 0,
                "start_time": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            self.request_history.clear()
            self.error_log.clear()
            self.server_start_time = time.time()

# Global performance tracker
performance_tracker = PerformanceMetrics()

# API functions
def get_performance_metrics() -> Dict[str, Any]:
    """
    Retrieve current agent performance metrics.

    Returns:
        Dictionary containing performance metrics including:
        - total_requests: Total number of requests processed
        - successful_requests: Number of successful requests
        - failed_requests: Number of failed requests
        - average_response_time: Average response time in seconds
        - min_response_time: Minimum response time in seconds
        - max_response_time: Maximum response time in seconds
        - success_rate: Success rate as a percentage
        - error_rate: Error rate as a percentage
        - uptime_seconds: Server uptime in seconds
    """
    try:
        metrics = performance_tracker.get_metrics()
        return {
            "status": "success",
            "data": metrics
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve metrics: {str(e)}"
        }

def get_request_history(limit: int = 20) -> Dict[str, Any]:
    """
    Retrieve recent request history.

    Args:
        limit: Maximum number of recent requests to return (default: 20, max: 100)

    Returns:
        Dictionary containing request history with timestamp, endpoint,
        response time, success status, and error messages if any
    """
    try:
        if not isinstance(limit, int) or limit < 1:
            return {
                "status": "error",
                "message": "Limit must be a positive integer"
            }

        # Cap limit at 100
        limit = min(limit, 100)

        history = performance_tracker.get_request_history(limit)
        return {
            "status": "success",
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve request history: {str(e)}"
        }

def get_error_log(limit: int = 10) -> Dict[str, Any]:
    """
    Retrieve recent error log entries.

    Args:
        limit: Maximum number of recent errors to return (default: 10, max: 50)

    Returns:
        Dictionary containing error log entries with timestamp,
        endpoint, and error message
    """
    try:
        if not isinstance(limit, int) or limit < 1:
            return {
                "status": "error",
                "message": "Limit must be a positive integer"
            }

        # Cap limit at 50
        limit = min(limit, 50)

        errors = performance_tracker.get_error_log(limit)
        return {
            "status": "success",
            "data": errors,
            "count": len(errors)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve error log: {str(e)}"
        }

def simulate_agent_task(task_name: str = "default_task", duration: float = 0.1, should_fail: bool = False) -> Dict[str, Any]:
    """
    Simulate an agent task for testing the performance dashboard.

    Args:
        task_name: Name of the task to simulate
        duration: Simulated task duration in seconds (default: 0.1)
        should_fail: Whether the task should fail (default: False)

    Returns:
        Dictionary containing task execution result and recorded metrics
    """
    start_time = time.time()

    try:
        # Validate inputs
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string")

        if not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError("Duration must be a non-negative number")

        if not isinstance(should_fail, bool):
            raise ValueError("should_fail must be a boolean")

        # Simulate task execution
        time.sleep(min(duration, 5.0))  # Cap at 5 seconds for safety

        # Simulate failure if requested
        if should_fail:
            raise RuntimeError(f"Simulated failure for task: {task_name}")

        response_time = time.time() - start_time
        performance_tracker.record_request(
            endpoint=f"simulate_agent_task:{task_name}",
            response_time=response_time,
            success=True
        )

        return {
            "status": "success",
            "task_name": task_name,
            "duration": round(response_time, 4),
            "message": f"Task '{task_name}' completed successfully"
        }

    except Exception as e:
        response_time = time.time() - start_time
        error_message = str(e)

        performance_tracker.record_request(
            endpoint=f"simulate_agent_task:{task_name}",
            response_time=response_time,
            success=False,
            error_message=error_message
        )

        return {
            "status": "error",
            "task_name": task_name,
            "duration": round(response_time, 4),
            "message": error_message
        }

def reset_performance_metrics() -> Dict[str, Any]:
    """
    Reset all performance metrics to initial state.

    Returns:
        Dictionary confirming the reset operation
    """
    try:
        performance_tracker.reset_metrics()
        return {
            "status": "success",
            "message": "Performance metrics have been reset",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to reset metrics: {str(e)}"
        }

def get_dashboard_data() -> Dict[str, Any]:
    """
    Get comprehensive dashboard data including metrics, recent history, and errors.

    Returns:
        Dictionary containing all dashboard data in a single response
    """
    try:
        return {
            "status": "success",
            "data": {
                "metrics": performance_tracker.get_metrics(),
                "recent_requests": performance_tracker.get_request_history(10),
                "recent_errors": performance_tracker.get_error_log(5)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve dashboard data: {str(e)}"
        }

if __name__ == "__main__":
    # Create the MCP server
    server_name = "Agent Performance Dashboard Server"
    print(f"Starting {server_name}...")
    server = FastMCP(server_name)

    # Register performance monitoring functions
    server.add_tool("get_performance_metrics", get_performance_metrics)
    server.add_tool("get_request_history", get_request_history)
    server.add_tool("get_error_log", get_error_log)
    server.add_tool("simulate_agent_task", simulate_agent_task)
    server.add_tool("reset_performance_metrics", reset_performance_metrics)
    server.add_tool("get_dashboard_data", get_dashboard_data)

    print(f"{server_name} is ready!")
    print("Available endpoints:")
    print("  - get_performance_metrics: Get current performance metrics")
    print("  - get_request_history: Get recent request history")
    print("  - get_error_log: Get recent error entries")
    print("  - simulate_agent_task: Simulate agent tasks for testing")
    print("  - reset_performance_metrics: Reset all metrics")
    print("  - get_dashboard_data: Get all dashboard data at once")

    # Run the server
    server.run()
