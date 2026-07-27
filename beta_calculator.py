class BetaCalculatorEngine:
    """Core mathematical engine implemented entirely from scratch."""
    PI = 3.141592653589793
    E  = 2.718281828459045

    @staticmethod
    def power(base, exponent):
        if base <= 0:
            if base == 0 and exponent > 0:
                return 0.0
            raise ValueError("Power base must be positive.")
        return BetaCalculatorEngine.exp(exponent * BetaCalculatorEngine.ln(base))

    @staticmethod
    def sqrt(x):
        if x < 0:
            raise ValueError("Cannot compute square root of a negative number.")
        if x == 0:
            return 0.0
        guess = x / 2.0
        for _ in range(100):
            guess = 0.5 * (guess + x / guess)
        return guess

    @staticmethod
    def exp(x):
        sum_val = 1.0
        term = 1.0
        for i in range(1, 100):
            term *= x / i
            sum_val += term
            if abs(term) < 1e-15:
                break
        return sum_val

    @staticmethod
    def ln(x):
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers.")
        y = 0.0 
        for _ in range(100):
            ey = BetaCalculatorEngine.exp(y)
            y = y + 2 * (x - ey) / (x + ey)
        return y

    @staticmethod
    def sin(x):
        two_pi = 2 * BetaCalculatorEngine.PI
        x = x - int(x / two_pi) * two_pi
        sum_val = 0.0
        term = x
        for i in range(1, 40):
            sum_val += term
            term *= -1 * x * x / ((2 * i) * (2 * i + 1))
            if abs(term) < 1e-15:
                break
        return sum_val