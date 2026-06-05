from collections.abc import Callable


class Calculator:
    def __init__(self) -> None:
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> float | None:
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression: str) -> list[str]:
        # Improved tokenization to handle multi-digit numbers and decimals
        import re
        # This regex matches numbers (integers or floats), operators, and parentheses
        tokens = re.findall(r'\d+\.?\d*|[+\-*/()]', expression)
        return tokens

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        values.append(self.operators[operator](left, right))

    def _evaluate_infix(self, tokens: list[str]) -> float:
        values: list[float] = []
        operators: list[str] = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == " ":
                i += 1
                continue
            if token.isdigit() or (token[0] == '-' and len(token) > 1 and token[1:].isdigit()):
                # Handle negative numbers
                if token.startswith('-') and (i == 0 or tokens[i-1] in self.operators or tokens[i-1] == '('):
                    values.append(float(token))
                else:
                    values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                operators.pop() # Pop '('
            elif token in self.operators:
                while (
                    operators
                    and operators[-1] != '('
                    and self.precedence.get(operators[-1], 0) >= self.precedence.get(token, 0)
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            i += 1
        
        while operators:
            self._apply_operator(operators, values)

        return values[0]
