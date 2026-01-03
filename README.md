# HelloMCP

A collection of Model Context Protocol (MCP) examples and demos. This repository showcases how to create and use MCP servers and clients for various use cases.

## What is MCP?

The Model Context Protocol (MCP) allows AI assistants to interact with external tools and APIs. It provides a standardized way for LLMs (Large Language Models) to access and manipulate data from various sources, making them more powerful and versatile.

## Projects

### BMI Calculator

The BMI (Body Mass Index) Calculator is a simple example of an MCP service that:

1. Calculates BMI based on height and weight
2. Categorizes BMI values into health categories
3. Provides comprehensive health assessments
4. Offers a greeting API endpoint with customizable name parameter

### Real-time Agent Performance Dashboard

A comprehensive performance monitoring system for MCP agents that provides:

1. Real-time performance metrics tracking (response times, success rates, error rates)
2. Request history management with detailed logging
3. Error tracking and logging capabilities
4. Web-based dashboard for visual monitoring
5. Task simulation for testing and demonstration
6. Thread-safe concurrent request handling

#### Files:

- `bmi_calculator/bmi_mcp_server.py` - The MCP server implementation
- `bmi_calculator/bmi_mcp_client.py` - A demo client showing how to use the server
- `bmi_calculator/greet_demo.py` - Demo client for the greeting API
- `bmi_calculator/test_greet.py` - Unit tests for the greeting API
- `bmi_calculator/requirements.txt` - Required dependencies

#### Setup and Usage:

1. Install requirements:
   ```
   pip install -r bmi_calculator/requirements.txt
   ```

2. Run the server:
   ```
   python bmi_calculator/bmi_mcp_server.py
   ```

3. In a separate terminal, run the client demos:
   ```
   python bmi_calculator/bmi_mcp_client.py
   python bmi_calculator/greet_demo.py
   ```

4. Run the unit tests:
   ```
   python bmi_calculator/test_greet.py
   ```

#### Available API Endpoints:

1. **calculate_bmi** - Calculate BMI from height and weight
2. **get_bmi_category** - Get BMI category from a BMI value
3. **bmi_assessment** - Get comprehensive BMI assessment
4. **greet** - Return a greeting message with customizable name
   - Parameters:
     - `name` (optional, default: "World"): The name to greet
   - Returns: `{"message": "Hello, {name}!", "name": "{name}"}`
   - Error handling: Returns error for empty or non-string names

#### MCP Configuration:

To use this with an MCP-compatible assistant, add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "bmi-calculator": {
      "command": "python",
      "args": [
        "path/to/bmi_mcp_server.py"
      ],
      "name": "BMI Calculator MCP Server"
    }
  }
}
```

### Performance Dashboard Files

- `bmi_calculator/performance_dashboard_server.py` - Performance monitoring MCP server
- `bmi_calculator/dashboard.html` - Web-based real-time dashboard interface
- `bmi_calculator/performance_demo.py` - Demo client showing dashboard features
- `bmi_calculator/test_performance_dashboard.py` - Comprehensive unit tests

### Performance Dashboard Setup and Usage

1. Install requirements:
   ```
   pip install -r bmi_calculator/requirements.txt
   ```

2. Run the performance dashboard server:
   ```
   python bmi_calculator/performance_dashboard_server.py
   ```

3. Open the web dashboard:
   - Open `bmi_calculator/dashboard.html` in your web browser
   - The dashboard will display real-time performance metrics

4. Run demo simulations:
   ```
   python bmi_calculator/performance_demo.py           # Basic demo
   python bmi_calculator/performance_demo.py edge      # Edge cases demo
   python bmi_calculator/performance_demo.py patterns  # Performance patterns demo
   ```

5. Run unit tests:
   ```
   python bmi_calculator/test_performance_dashboard.py
   ```

### Performance Dashboard API Endpoints

1. **get_performance_metrics** - Retrieve current performance metrics
   - Returns: Total requests, success/error rates, response times, uptime

2. **get_request_history** - Get recent request history
   - Parameters: `limit` (optional, default: 20, max: 100)
   - Returns: List of recent requests with timestamps and details

3. **get_error_log** - Get recent error log entries
   - Parameters: `limit` (optional, default: 10, max: 50)
   - Returns: List of errors with timestamps and messages

4. **simulate_agent_task** - Simulate agent tasks for testing
   - Parameters:
     - `task_name` (required): Name of the task
     - `duration` (optional, default: 0.1): Task duration in seconds
     - `should_fail` (optional, default: False): Whether task should fail
   - Returns: Task execution result and metrics

5. **reset_performance_metrics** - Reset all metrics to initial state
   - Returns: Confirmation of reset operation

6. **get_dashboard_data** - Get comprehensive dashboard data
   - Returns: All metrics, recent requests, and errors in one response

### Performance Dashboard MCP Configuration

```json
{
  "mcpServers": {
    "performance-dashboard": {
      "command": "python",
      "args": [
        "path/to/performance_dashboard_server.py"
      ],
      "name": "Agent Performance Dashboard Server"
    }
  }
}
```

### Performance Dashboard Features

- **Real-time Metrics**: Track total requests, success rates, error rates, and response times
- **Request History**: View detailed history of recent requests with timestamps
- **Error Logging**: Comprehensive error tracking with stack traces
- **Thread-Safe**: Concurrent request handling with thread locks
- **Web Interface**: Beautiful, responsive dashboard for visual monitoring
- **Auto-Refresh**: Dashboard automatically updates every 5 seconds
- **Task Simulation**: Built-in tools for testing and demonstration
- **Edge Case Handling**: Robust error handling and input validation

## Contributing

Feel free to contribute your own MCP examples or improvements to existing ones!

## License

MIT License