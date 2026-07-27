import tkinter as tk
from tkinter import messagebox

class InvalidDomainError(Exception):
    """Raised when input parameters violate the domain constraints of the Beta Function."""
    pass

class BetaCalculatorEngine:
    """Core mathematical engine implemented entirely from scratch."""
    PI = 3.141592653589793
    E  = 2.718281828459045

    @staticmethod
    def power(base, exponent):
        if base <= 0:
            if base == 0 and exponent > 0:
                return 0.0
            raise InvalidDomainError("Power base must be positive.")
        return BetaCalculatorEngine.exp(exponent * BetaCalculatorEngine.ln(base))

    @staticmethod
    def sqrt(x):
        if x < 0:
            raise InvalidDomainError("Cannot compute square root of a negative number.")
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
            raise InvalidDomainError("Logarithm undefined for non-positive numbers.")
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

    @classmethod
    def lanczos_gamma(cls, z):
        if z <= 0:
            raise InvalidDomainError("Gamma function requires z > 0.")
        if z < 0.5:
            return cls.PI / (cls.sin(cls.PI * z) * cls.lanczos_gamma(1.0 - z))

        z -= 1.0
        x = 0.99999999999980993
        p = [
            676.5203681218851, -1259.1392167224028, 771.32342877765313,
            -176.61502916214059, 12.507343278686905, -0.13857109526572012,
            9.9843695780195716e-6, 1.5056327351493116e-7
        ]
        for i, val in enumerate(p):
            x += val / (z + i + 1.0)

        t = z + 7.0 + 0.5
        return cls.sqrt(2.0 * cls.PI) * cls.power(t, (z + 0.5)) * cls.exp(-t) * x

    @classmethod
    def calculate_beta(cls, x, y):
        if x <= 0 or y <= 0:
            raise InvalidDomainError("Parameters x and y must both be strictly greater than 0.")
        return (cls.lanczos_gamma(x) * cls.lanczos_gamma(y)) / cls.lanczos_gamma(x + y)


class BetaCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator - Beta Function B(x,y)")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        tk.Label(root, text="Beta Function B(x,y) Calculator", font=("Helvetica", 14, "bold")).pack(pady=15)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Value x (x > 0):", font=("Helvetica", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_x = tk.Entry(input_frame, font=("Helvetica", 11), width=15)
        self.entry_x.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Value y (y > 0):", font=("Helvetica", 11)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_y = tk.Entry(input_frame, font=("Helvetica", 11), width=15)
        self.entry_y.grid(row=1, column=1, padx=5, pady=5)

        self.calc_button = tk.Button(root, text="Calculate B(x,y)", command=self.on_calculate, font=("Helvetica", 11, "bold"), fg="black", padx=10, pady=5)
        self.calc_button.pack(pady=15)

        self.result_label = tk.Label(root, text="Result: --", font=("Helvetica", 12, "bold"), fg="#333333")
        self.result_label.pack(pady=10)

    def on_calculate(self):
        """Handles GUI events and catches exceptions cleanly via popups."""
        x_str = self.entry_x.get().strip()
        y_str = self.entry_y.get().strip()

        try:
            x = float(x_str)
            y = float(y_str)

            res = BetaCalculatorEngine.calculate_beta(x, y)
            self.result_label.config(text=f"Result B({x}, {y}) = {res:.6e}", fg="green")

        except ValueError:
            messagebox.showerror("Input Error", "Invalid input format. Please enter valid real numbers.")
            self.result_label.config(text="Result: Error", fg="red")
        except InvalidDomainError as ide:
            messagebox.showwarning("Domain Error", str(ide))
            self.result_label.config(text="Result: Domain Error", fg="red")
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred: {e}")
            self.result_label.config(text="Result: System Error", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = BetaCalculatorGUI(root)
    root.mainloop()