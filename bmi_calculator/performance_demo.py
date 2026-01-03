"""
Performance Dashboard Demo Client

This script demonstrates how to use the Agent Performance Dashboard
by simulating various agent tasks and displaying the metrics.
"""

import sys
import time
import random

# Simulated MCP function call
def call_mcp_function(function_name, params):
    """
    Simulate calling an MCP function.
    In a real application, this would make actual calls to the MCP server.
    """
    print(f"\n{'='*60}")
    print(f"Calling: {function_name}")
    print(f"Parameters: {params}")
    print(f"{'='*60}")


def demonstrate_performance_monitoring():
    """Demonstrate the performance monitoring capabilities."""

    print("\n" + "="*60)
    print("AGENT PERFORMANCE DASHBOARD DEMO")
    print("="*60)

    # 1. Get initial metrics
    print("\n1. Getting initial performance metrics...")
    call_mcp_function("get_performance_metrics", {})
    print("Expected: Metrics showing zero requests, 0% success/error rates")
    time.sleep(1)

    # 2. Simulate some successful tasks
    print("\n2. Simulating successful agent tasks...")
    for i in range(5):
        duration = random.uniform(0.05, 0.3)
        call_mcp_function("simulate_agent_task", {
            "task_name": f"data_processing_{i+1}",
            "duration": round(duration, 2),
            "should_fail": False
        })
        time.sleep(0.2)

    # 3. Get updated metrics
    print("\n3. Getting updated performance metrics...")
    call_mcp_function("get_performance_metrics", {})
    print("Expected: 5 total requests, 100% success rate, average response time")
    time.sleep(1)

    # 4. Simulate some failed tasks
    print("\n4. Simulating failed agent tasks...")
    for i in range(2):
        duration = random.uniform(0.05, 0.2)
        call_mcp_function("simulate_agent_task", {
            "task_name": f"risky_operation_{i+1}",
            "duration": round(duration, 2),
            "should_fail": True
        })
        time.sleep(0.2)

    # 5. Get request history
    print("\n5. Getting request history (last 10 requests)...")
    call_mcp_function("get_request_history", {"limit": 10})
    print("Expected: List of 7 requests (5 successful, 2 failed)")
    time.sleep(1)

    # 6. Get error log
    print("\n6. Getting error log...")
    call_mcp_function("get_error_log", {"limit": 5})
    print("Expected: 2 error entries from the failed tasks")
    time.sleep(1)

    # 7. Simulate mixed workload
    print("\n7. Simulating mixed workload (10 tasks)...")
    for i in range(10):
        should_fail = random.random() < 0.2  # 20% failure rate
        duration = random.uniform(0.05, 0.5)
        call_mcp_function("simulate_agent_task", {
            "task_name": f"mixed_task_{i+1}",
            "duration": round(duration, 2),
            "should_fail": should_fail
        })
        time.sleep(0.1)

    # 8. Get comprehensive dashboard data
    print("\n8. Getting comprehensive dashboard data...")
    call_mcp_function("get_dashboard_data", {})
    print("Expected: All metrics, recent requests, and error log in one response")
    time.sleep(1)

    # 9. Show final metrics
    print("\n9. Getting final performance metrics...")
    call_mcp_function("get_performance_metrics", {})
    print("Expected: ~17 total requests, ~70-80% success rate, various response times")
    time.sleep(1)

    # 10. Demonstrate reset
    print("\n10. Demonstrating metrics reset...")
    call_mcp_function("reset_performance_metrics", {})
    print("Expected: Confirmation of reset")
    time.sleep(1)

    print("\n11. Verifying metrics after reset...")
    call_mcp_function("get_performance_metrics", {})
    print("Expected: All metrics reset to zero")

    print("\n" + "="*60)
    print("DEMO COMPLETED")
    print("="*60)
    print("\nIn a real application, these calls would be processed by the")
    print("Performance Dashboard MCP server and you could view the results")
    print("in the web dashboard (dashboard.html).")
    print("\nTo run the actual server:")
    print("  python bmi_calculator/performance_dashboard_server.py")
    print("\nThen open dashboard.html in your web browser to view real-time metrics.")


def demonstrate_edge_cases():
    """Demonstrate edge cases and error handling."""

    print("\n" + "="*60)
    print("EDGE CASES AND ERROR HANDLING DEMO")
    print("="*60)

    # Invalid limit parameter
    print("\n1. Testing invalid limit parameter...")
    call_mcp_function("get_request_history", {"limit": -5})
    print("Expected: Error - limit must be a positive integer")
    time.sleep(1)

    # Invalid task name
    print("\n2. Testing invalid task name...")
    call_mcp_function("simulate_agent_task", {
        "task_name": "",
        "duration": 0.1,
        "should_fail": False
    })
    print("Expected: Error - task name must be non-empty string")
    time.sleep(1)

    # Invalid duration
    print("\n3. Testing invalid duration...")
    call_mcp_function("simulate_agent_task", {
        "task_name": "test_task",
        "duration": -1.0,
        "should_fail": False
    })
    print("Expected: Error - duration must be non-negative")
    time.sleep(1)

    # Large history request
    print("\n4. Testing large history request...")
    call_mcp_function("get_request_history", {"limit": 500})
    print("Expected: Capped at maximum of 100 entries")
    time.sleep(1)

    # Zero duration task
    print("\n5. Testing zero duration task...")
    call_mcp_function("simulate_agent_task", {
        "task_name": "instant_task",
        "duration": 0,
        "should_fail": False
    })
    print("Expected: Success with minimal response time")
    time.sleep(1)

    print("\n" + "="*60)
    print("EDGE CASES DEMO COMPLETED")
    print("="*60)


def demonstrate_performance_patterns():
    """Demonstrate different performance patterns."""

    print("\n" + "="*60)
    print("PERFORMANCE PATTERNS DEMO")
    print("="*60)

    # Pattern 1: High-frequency low-latency tasks
    print("\n1. Simulating high-frequency low-latency pattern (20 fast tasks)...")
    for i in range(20):
        call_mcp_function("simulate_agent_task", {
            "task_name": f"fast_task_{i+1}",
            "duration": 0.01,
            "should_fail": False
        })
    print("Expected: High request count, low average response time")
    time.sleep(1)

    # Pattern 2: Low-frequency high-latency tasks
    print("\n2. Simulating low-frequency high-latency pattern (5 slow tasks)...")
    for i in range(5):
        call_mcp_function("simulate_agent_task", {
            "task_name": f"slow_task_{i+1}",
            "duration": 1.0,
            "should_fail": False
        })
    print("Expected: Higher average response time, higher max response time")
    time.sleep(1)

    # Pattern 3: Degrading performance
    print("\n3. Simulating degrading performance (increasing failure rate)...")
    for i in range(10):
        failure_probability = i * 0.1  # 0%, 10%, 20%, ..., 90%
        should_fail = random.random() < failure_probability
        call_mcp_function("simulate_agent_task", {
            "task_name": f"degrading_task_{i+1}",
            "duration": 0.1,
            "should_fail": should_fail
        })
    print("Expected: Increasing error rate over time")
    time.sleep(1)

    print("\n" + "="*60)
    print("PERFORMANCE PATTERNS DEMO COMPLETED")
    print("="*60)


if __name__ == "__main__":
    print("\nPerformance Dashboard Demo Client")
    print("==================================")

    if len(sys.argv) > 1:
        demo_type = sys.argv[1]
        if demo_type == "edge":
            demonstrate_edge_cases()
        elif demo_type == "patterns":
            demonstrate_performance_patterns()
        else:
            print(f"Unknown demo type: {demo_type}")
            print("Available demos: edge, patterns")
            print("Running default demo...")
            demonstrate_performance_monitoring()
    else:
        demonstrate_performance_monitoring()

    print("\n" + "="*60)
    print("Additional demo options:")
    print("  python bmi_calculator/performance_demo.py edge     - Edge cases demo")
    print("  python bmi_calculator/performance_demo.py patterns - Performance patterns demo")
    print("="*60)
