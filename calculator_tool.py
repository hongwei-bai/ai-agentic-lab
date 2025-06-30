def calculator_tool(query: str) -> str:
    try:
        return str(eval(query))
    except Exception as e:
        return f"Error: {str(e)}"
