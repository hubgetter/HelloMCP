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

## Contributing

Feel free to contribute your own MCP examples or improvements to existing ones!

## License

MIT License