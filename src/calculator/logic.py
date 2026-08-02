def calculate(expression):
    """
    Evaluate a calculator expression.
    """

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    try:
        return str(eval(expression))

    except Exception:
        return "Error"