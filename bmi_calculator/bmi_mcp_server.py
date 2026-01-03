from fastmcp import FastMCP

# Define our BMI calculation functions
def calculate_bmi(height, weight):
    """Calculate BMI using formula: weight (kg) / (height (m) * height (m))"""
    if height <= 0 or weight <= 0:
        return {"error": "Height and weight must be positive values"}
    
    bmi = weight / (height * height)
    return {"bmi": round(bmi, 2)}

def get_bmi_category(bmi):
    """Determine BMI category based on the BMI value"""
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity"
        
    return {"category": category}

def bmi_assessment(height, weight):
    """Calculate BMI and provide category assessment"""
    bmi_result = calculate_bmi(height, weight)

    if "error" in bmi_result:
        return bmi_result

    bmi = bmi_result["bmi"]
    category_result = get_bmi_category(bmi)

    return {
        "bmi": bmi,
        "category": category_result["category"],
        "message": f"Your BMI is {bmi}, which is classified as '{category_result['category']}'"
    }

def greet(name="World"):
    """Return a JSON greeting message with a customizable name parameter"""
    if not name or not isinstance(name, str):
        return {"error": "Name must be a non-empty string"}

    # Sanitize name to prevent injection issues
    sanitized_name = name.strip()
    if not sanitized_name:
        return {"error": "Name must be a non-empty string"}

    return {
        "message": f"Hello, {sanitized_name}!",
        "name": sanitized_name
    }

if __name__ == "__main__":
    # Create the MCP server
    server_name = "BMI Calculator MCP Server"
    print(f"Starting {server_name}...")
    server = FastMCP(server_name)
    
    # Register our standalone functions
    server.add_tool("calculate_bmi", calculate_bmi)
    server.add_tool("get_bmi_category", get_bmi_category)
    server.add_tool("bmi_assessment", bmi_assessment)
    server.add_tool("greet", greet)

    # Run the server
    server.run()