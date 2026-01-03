"""
Greeting API Demo

This script demonstrates how to use the greeting API endpoint
of the MCP Server by making function calls with different name parameters.
"""

import json


def call_mcp_function(function_name, params):
    """
    This function simulates calling an MCP function directly.
    In a real application, this would be handled by the MCP client/framework.
    """
    print(f"\n----- Calling {function_name} -----")
    print(f"Parameters: {json.dumps(params, indent=2)}")


def demonstrate_greeting_api():
    """Demonstrate the greeting API with various examples"""

    # Example 1: Default greeting (no name parameter)
    print("\n=== Example 1: Default Greeting ===")
    call_mcp_function("greet", {})
    # Expected output: {"message": "Hello, World!", "name": "World"}

    # Example 2: Custom name
    print("\n=== Example 2: Custom Name ===")
    call_mcp_function("greet", {
        "name": "Alice"
    })
    # Expected output: {"message": "Hello, Alice!", "name": "Alice"}

    # Example 3: Name with multiple words
    print("\n=== Example 3: Multiple Words ===")
    call_mcp_function("greet", {
        "name": "John Doe"
    })
    # Expected output: {"message": "Hello, John Doe!", "name": "John Doe"}

    # Example 4: Name with special characters
    print("\n=== Example 4: Special Characters ===")
    call_mcp_function("greet", {
        "name": "José García"
    })
    # Expected output: {"message": "Hello, José García!", "name": "José García"}

    # Example 5: Whitespace handling
    print("\n=== Example 5: Whitespace Handling ===")
    call_mcp_function("greet", {
        "name": "  Bob  "
    })
    # Expected output: {"message": "Hello, Bob!", "name": "Bob"}


if __name__ == "__main__":
    print("Greeting API Demo")
    print("=================")

    demonstrate_greeting_api()

    print("\n\nDemo completed. In a real application, you would use the MCP framework to make these calls to the server.")
    print("\nTo test the actual API, run the server with:")
    print("  python bmi_mcp_server.py")
    print("\nThen interact with it through an MCP-compatible client.")
