"""
BMI Calculator MCP Client

This script demonstrates how to use the BMI Calculator MCP Server
by making function calls to calculate BMI, get BMI category,
and get a comprehensive BMI assessment.
"""

# Import necessary modules 
import sys
import json

# Function to simulate an MCP function call
def call_mcp_function(function_name, params):
    """
    This function simulates calling an MCP function directly.
    In a real application, this would be handled by the MCP client/framework.
    """
    print(f"\n----- Calling {function_name} -----")
    print(f"Parameters: {json.dumps(params, indent=2)}")
    
    # In an actual MCP client implementation, this is where
    # you would make the actual call to the MCP server

# Demonstrate BMI calculation
def demonstrate_bmi_calculator():
    # Example 1: Calculate BMI for a person with height 1.75m and weight 70kg
    call_mcp_function("calculate_bmi", {
        "height": 1.75,
        "weight": 70
    })
    # Expected output: {"bmi": 22.86}
    
    # Example 2: Get BMI category for a BMI value of 22.86
    call_mcp_function("get_bmi_category", {
        "bmi": 22.86
    })
    # Expected output: {"category": "Normal weight"}
    
    # Example 3: Get comprehensive BMI assessment
    call_mcp_function("bmi_assessment", {
        "height": 1.75,
        "weight": 70
    })
    # Expected output: {"bmi": 22.86, "category": "Normal weight", "message": "Your BMI is 22.86, which is classified as 'Normal weight'"}
    
    # Example 4: Demonstrate with different BMI ranges
    print("\n----- BMI Examples Across Different Categories -----")
    
    # Underweight example
    call_mcp_function("bmi_assessment", {
        "height": 1.80,
        "weight": 55
    })
    
    # Normal weight example
    call_mcp_function("bmi_assessment", {
        "height": 1.65,
        "weight": 60
    })
    
    # Overweight example
    call_mcp_function("bmi_assessment", {
        "height": 1.70,
        "weight": 85
    })
    
    # Obesity example
    call_mcp_function("bmi_assessment", {
        "height": 1.75,
        "weight": 100
    })

if __name__ == "__main__":
    print("BMI Calculator MCP Client Demo")
    print("==============================")
    
    demonstrate_bmi_calculator()
    
    print("\nDemo completed. In a real application, you would use the MCP framework to make these calls to the server.")