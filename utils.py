def run_code(code):

    try:
        exec_globals = {}

        exec(code, exec_globals)

        return "✅ Code executed successfully"

    except Exception as e:
        return f"❌ Error: {e}"
