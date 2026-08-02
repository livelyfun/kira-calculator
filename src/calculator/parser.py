def prepare_expression(expression: str) -> str:
    """
    Convert calculator symbols into Python operators.
    """

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    return expression