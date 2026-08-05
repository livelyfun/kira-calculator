from calculator.parser import prepare_expression


def evaluate_expression(expression: str) -> str:
    """
    Evaluate a prepared expression.
    """

    try:
        result = eval(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)

    except Exception:  # noqa: BLE001
        return "Error"


def calculate(expression: str) -> str:
    """
    Main entry point for calculator logic.
    """

    prepared = prepare_expression(expression)

    return evaluate_expression(prepared)