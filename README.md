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

#### Files:

- `bmi_calculator/bmi_mcp_server.py` - The MCP server implementation
- `bmi_calculator/bmi_mcp_client.py` - A demo client showing how to use the server
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

3. In a separate terminal, run the client demo:
   ```
   python bmi_calculator/bmi_mcp_client.py
   ```

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