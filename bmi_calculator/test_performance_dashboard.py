"""
Unit tests for the Agent Performance Dashboard

This test suite covers:
- Performance metrics tracking
- Request history management
- Error logging
- Task simulation
- Metrics reset
- Edge cases and error handling
"""

import unittest
import time
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions and classes from the performance dashboard server
from performance_dashboard_server import (
    PerformanceMetrics,
    get_performance_metrics,
    get_request_history,
    get_error_log,
    simulate_agent_task,
    reset_performance_metrics,
    get_dashboard_data,
    performance_tracker
)


class TestPerformanceMetrics(unittest.TestCase):
    """Test cases for the PerformanceMetrics class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.metrics = PerformanceMetrics(max_history=10)

    def test_initial_metrics(self):
        """Test that metrics are initialized correctly."""
        metrics = self.metrics.get_metrics()

        self.assertEqual(metrics['total_requests'], 0)
        self.assertEqual(metrics['successful_requests'], 0)
        self.assertEqual(metrics['failed_requests'], 0)
        self.assertEqual(metrics['average_response_time'], 0.0)
        self.assertEqual(metrics['min_response_time'], 0.0)  # Should handle inf
        self.assertEqual(metrics['max_response_time'], 0.0)
        self.assertEqual(metrics['success_rate'], 0.0)
        self.assertEqual(metrics['error_rate'], 0.0)

    def test_record_successful_request(self):
        """Test recording a successful request."""
        self.metrics.record_request("test_endpoint", 0.123, True)

        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['successful_requests'], 1)
        self.assertEqual(metrics['failed_requests'], 0)
        self.assertEqual(metrics['success_rate'], 100.0)
        self.assertEqual(metrics['error_rate'], 0.0)

    def test_record_failed_request(self):
        """Test recording a failed request."""
        self.metrics.record_request("test_endpoint", 0.234, False, "Test error")

        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics['total_requests'], 1)
        self.assertEqual(metrics['successful_requests'], 0)
        self.assertEqual(metrics['failed_requests'], 1)
        self.assertEqual(metrics['success_rate'], 0.0)
        self.assertEqual(metrics['error_rate'], 100.0)

    def test_response_time_calculations(self):
        """Test response time metric calculations."""
        self.metrics.record_request("endpoint1", 0.1, True)
        self.metrics.record_request("endpoint2", 0.2, True)
        self.metrics.record_request("endpoint3", 0.3, True)

        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics['min_response_time'], 0.1)
        self.assertEqual(metrics['max_response_time'], 0.3)
        self.assertEqual(metrics['average_response_time'], 0.2)

    def test_success_rate_calculation(self):
        """Test success rate percentage calculation."""
        # Record 7 successful and 3 failed requests
        for i in range(7):
            self.metrics.record_request(f"endpoint_{i}", 0.1, True)
        for i in range(3):
            self.metrics.record_request(f"endpoint_{i+7}", 0.1, False, "Error")

        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics['total_requests'], 10)
        self.assertEqual(metrics['success_rate'], 70.0)
        self.assertEqual(metrics['error_rate'], 30.0)

    def test_request_history_limit(self):
        """Test that request history respects the maximum size."""
        # Record more requests than the limit
        for i in range(15):
            self.metrics.record_request(f"endpoint_{i}", 0.1, True)

        history = self.metrics.get_request_history()
        self.assertEqual(len(history), 10)  # Should be capped at max_history

    def test_error_log(self):
        """Test error logging functionality."""
        self.metrics.record_request("endpoint1", 0.1, False, "Error 1")
        self.metrics.record_request("endpoint2", 0.1, False, "Error 2")

        errors = self.metrics.get_error_log()
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0]['error'], "Error 1")
        self.assertEqual(errors[1]['error'], "Error 2")

    def test_reset_metrics(self):
        """Test resetting metrics."""
        # Record some requests
        self.metrics.record_request("endpoint1", 0.1, True)
        self.metrics.record_request("endpoint2", 0.1, False, "Error")

        # Reset
        self.metrics.reset_metrics()

        # Verify reset
        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics['total_requests'], 0)
        self.assertEqual(metrics['successful_requests'], 0)
        self.assertEqual(metrics['failed_requests'], 0)

        history = self.metrics.get_request_history()
        self.assertEqual(len(history), 0)

        errors = self.metrics.get_error_log()
        self.assertEqual(len(errors), 0)

    def test_concurrent_access(self):
        """Test thread-safe concurrent access to metrics."""
        import threading

        def record_requests():
            for i in range(100):
                self.metrics.record_request(f"endpoint_{i}", 0.01, True)

        # Create multiple threads
        threads = [threading.Thread(target=record_requests) for _ in range(5)]

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify total requests
        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics['total_requests'], 500)


class TestAPIFunctions(unittest.TestCase):
    """Test cases for the API functions."""

    def setUp(self):
        """Reset global metrics before each test."""
        performance_tracker.reset_metrics()

    def test_get_performance_metrics(self):
        """Test getting performance metrics."""
        result = get_performance_metrics()

        self.assertEqual(result['status'], 'success')
        self.assertIn('data', result)
        self.assertIn('total_requests', result['data'])

    def test_get_request_history_default_limit(self):
        """Test getting request history with default limit."""
        # Simulate some requests
        for i in range(30):
            simulate_agent_task(f"task_{i}", 0.01, False)

        result = get_request_history()

        self.assertEqual(result['status'], 'success')
        self.assertIn('data', result)
        self.assertLessEqual(len(result['data']), 20)  # Default limit

    def test_get_request_history_custom_limit(self):
        """Test getting request history with custom limit."""
        # Simulate some requests
        for i in range(15):
            simulate_agent_task(f"task_{i}", 0.01, False)

        result = get_request_history(10)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['data']), 10)

    def test_get_request_history_invalid_limit(self):
        """Test getting request history with invalid limit."""
        result = get_request_history(-5)

        self.assertEqual(result['status'], 'error')
        self.assertIn('Limit must be a positive integer', result['message'])

    def test_get_request_history_limit_cap(self):
        """Test that request history limit is capped at 100."""
        result = get_request_history(500)

        self.assertEqual(result['status'], 'success')
        # Even if we request 500, it should be capped at 100

    def test_get_error_log(self):
        """Test getting error log."""
        # Simulate some failures
        for i in range(5):
            simulate_agent_task(f"fail_task_{i}", 0.01, True)

        result = get_error_log()

        self.assertEqual(result['status'], 'success')
        self.assertIn('data', result)
        self.assertEqual(len(result['data']), 5)

    def test_get_error_log_invalid_limit(self):
        """Test getting error log with invalid limit."""
        result = get_error_log(0)

        self.assertEqual(result['status'], 'error')

    def test_simulate_agent_task_success(self):
        """Test simulating a successful agent task."""
        result = simulate_agent_task("test_task", 0.1, False)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['task_name'], 'test_task')
        self.assertIn('duration', result)

        # Verify metrics were updated
        metrics_result = get_performance_metrics()
        self.assertEqual(metrics_result['data']['total_requests'], 1)
        self.assertEqual(metrics_result['data']['successful_requests'], 1)

    def test_simulate_agent_task_failure(self):
        """Test simulating a failed agent task."""
        result = simulate_agent_task("fail_task", 0.1, True)

        self.assertEqual(result['status'], 'error')
        self.assertIn('Simulated failure', result['message'])

        # Verify metrics were updated
        metrics_result = get_performance_metrics()
        self.assertEqual(metrics_result['data']['total_requests'], 1)
        self.assertEqual(metrics_result['data']['failed_requests'], 1)

    def test_simulate_agent_task_invalid_name(self):
        """Test simulating a task with invalid name."""
        result = simulate_agent_task("", 0.1, False)

        self.assertEqual(result['status'], 'error')
        self.assertIn('non-empty string', result['message'])

    def test_simulate_agent_task_invalid_duration(self):
        """Test simulating a task with invalid duration."""
        result = simulate_agent_task("test", -1, False)

        self.assertEqual(result['status'], 'error')
        self.assertIn('non-negative', result['message'])

    def test_simulate_agent_task_zero_duration(self):
        """Test simulating a task with zero duration."""
        result = simulate_agent_task("instant_task", 0, False)

        self.assertEqual(result['status'], 'success')

    def test_reset_performance_metrics(self):
        """Test resetting performance metrics."""
        # Simulate some activity
        simulate_agent_task("task1", 0.1, False)
        simulate_agent_task("task2", 0.1, True)

        # Reset
        result = reset_performance_metrics()

        self.assertEqual(result['status'], 'success')
        self.assertIn('reset', result['message'].lower())

        # Verify metrics are reset
        metrics_result = get_performance_metrics()
        self.assertEqual(metrics_result['data']['total_requests'], 0)

    def test_get_dashboard_data(self):
        """Test getting comprehensive dashboard data."""
        # Simulate some activity
        simulate_agent_task("task1", 0.1, False)
        simulate_agent_task("task2", 0.1, True)

        result = get_dashboard_data()

        self.assertEqual(result['status'], 'success')
        self.assertIn('data', result)
        self.assertIn('metrics', result['data'])
        self.assertIn('recent_requests', result['data'])
        self.assertIn('recent_errors', result['data'])

    def test_performance_under_load(self):
        """Test performance metrics under high load."""
        start_time = time.time()

        # Simulate 100 requests
        for i in range(100):
            should_fail = i % 10 == 0  # 10% failure rate
            simulate_agent_task(f"load_test_{i}", 0.01, should_fail)

        elapsed = time.time() - start_time

        # Verify metrics
        metrics_result = get_performance_metrics()
        data = metrics_result['data']

        self.assertEqual(data['total_requests'], 100)
        self.assertEqual(data['successful_requests'], 90)
        self.assertEqual(data['failed_requests'], 10)
        self.assertAlmostEqual(data['success_rate'], 90.0, places=1)
        self.assertAlmostEqual(data['error_rate'], 10.0, places=1)

        # Performance should be reasonable
        self.assertLess(elapsed, 5.0, "Test should complete in under 5 seconds")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Reset global metrics before each test."""
        performance_tracker.reset_metrics()

    def test_empty_metrics(self):
        """Test retrieving metrics when no requests have been made."""
        result = get_performance_metrics()

        self.assertEqual(result['status'], 'success')
        data = result['data']
        self.assertEqual(data['total_requests'], 0)
        self.assertEqual(data['min_response_time'], 0.0)
        self.assertEqual(data['max_response_time'], 0.0)

    def test_single_request(self):
        """Test metrics with a single request."""
        simulate_agent_task("single", 0.123, False)

        result = get_performance_metrics()
        data = result['data']

        self.assertEqual(data['total_requests'], 1)
        self.assertEqual(data['average_response_time'], data['min_response_time'])
        self.assertEqual(data['average_response_time'], data['max_response_time'])

    def test_very_long_task_name(self):
        """Test handling very long task names."""
        long_name = "a" * 1000
        result = simulate_agent_task(long_name, 0.01, False)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['task_name'], long_name)

    def test_special_characters_in_task_name(self):
        """Test handling special characters in task names."""
        special_name = "task-with.special_chars!@#$%"
        result = simulate_agent_task(special_name, 0.01, False)

        self.assertEqual(result['status'], 'success')

    def test_maximum_duration(self):
        """Test that duration is capped at 5 seconds."""
        start = time.time()
        result = simulate_agent_task("long_task", 10.0, False)
        elapsed = time.time() - start

        self.assertEqual(result['status'], 'success')
        self.assertLess(elapsed, 6.0, "Duration should be capped at 5 seconds")

    def test_whitespace_task_name(self):
        """Test task name with only whitespace."""
        result = simulate_agent_task("   ", 0.01, False)

        self.assertEqual(result['status'], 'error')


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
