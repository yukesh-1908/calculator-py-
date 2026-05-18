import re
import tkinter as tk
from calc import calculator

class CalculatorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("360x520")
        self.window.resizable(False, False)
        self.window.configure(bg="#222831")

        self.expression = tk.StringVar()
        self.result = tk.StringVar(value="0")

        title = tk.Label(
            self.window,
            text="Calculator",
            fg="#eeeeee",
            bg="#222831",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=(16, 4))

        self.display = tk.Entry(
            self.window,
            textvariable=self.expression,
            font=("Segoe UI", 26),
            bd=0,
            bg="#393e46",
            fg="#eeeeee",
            justify="right",
            insertbackground="#eeeeee",
        )
        self.display.pack(fill="x", padx=12, pady=(0, 6), ipady=14)
        self.display.bind("<Return>", lambda event: self.evaluate())

        self.result_label = tk.Label(
            self.window,
            textvariable=self.result,
            fg="#00adb5",
            bg="#222831",
            font=("Segoe UI", 16),
        )
        self.result_label.pack(anchor="e", padx=18)

        self.history = []
        self.history_window = None
        self.load_history()

        control_frame = tk.Frame(self.window, bg="#222831")
        control_frame.pack(fill="x", padx=12, pady=(10, 0))

        controls = [("C", self.clear), ("DEL", self.delete_last), ("HISTORY", self.show_history)]
        for label, action in controls:
            btn = tk.Button(
                control_frame,
                text=label,
                command=action,
                fg="#eeeeee",
                bg="#393e46",
                activebackground="#00adb5",
                activeforeground="#222831",
                font=("Segoe UI", 14, "bold"),
                bd=0,
                relief="ridge",
            )
            btn.pack(side="left", expand=True, fill="x", padx=4, pady=4, ipadx=4, ipady=10)
            self.create_hover_effect(btn)

        button_frame = tk.Frame(self.window, bg="#222831")
        button_frame.pack(padx=12, pady=12, fill="both", expand=True)

        self.window.bind("<Key>", self.on_keypress)

        buttons = [
            ("C", "DEL", "/", "*"),
            ("7", "8", "9", "-"),
            ("4", "5", "6", "+"),
            ("1", "2", "3", "="),
            ("0", ".", "", ""),
        ]

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                if not label:
                    continue
                action = self.create_action(label)
                btn = tk.Button(
                    button_frame,
                    text=label,
                    command=action,
                    fg="#eeeeee",
                    bg="#393e46",
                    activebackground="#00adb5",
                    activeforeground="#222831",
                    font=("Segoe UI", 18),
                    bd=0,
                    relief="ridge",
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6, ipadx=10, ipady=10)
                self.create_hover_effect(btn)

        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        for i in range(len(buttons)):
            button_frame.rowconfigure(i, weight=1)

    def create_action(self, label):
        if label == "C":
            return self.clear
        if label == "DEL":
            return self.delete_last
        if label == "=":
            return self.evaluate
        return lambda l=label: self.append_text(l)

    def append_text(self, text):
        current = self.expression.get()
        if current == "0":
            current = ""
        self.expression.set(current + text)

    def clear(self):
        self.expression.set("")
        self.result.set("0")

    def delete_last(self):
        self.expression.set(self.expression.get()[:-1])

    def evaluate(self):
        expr = self.expression.get().strip()
        if not expr:
            return
        try:
            value = self.safe_evaluate(expr)
            display_value = self.format_value(value)
            self.result.set(display_value)
            self.expression.set(display_value)
            self.save_history(expr, display_value)
        except ZeroDivisionError:
            self.result.set("Cannot divide by zero")
        except ValueError:
            self.result.set("Invalid expression")
        except Exception:
            self.result.set("Error")

    def safe_evaluate(self, expression):
        if not re.fullmatch(r"[0-9.+\-*/ ]+", expression):
            raise ValueError("Unsupported characters")

        tokens = re.findall(r"\d+\.\d+|\d+|[+\-*/]", expression)
        if not tokens:
            raise ValueError("Empty expression")

        tokens = self.normalize_negatives(tokens)
        tokens = self.compute_mul_div(tokens)
        return self.compute_add_sub(tokens)

    def normalize_negatives(self, tokens):
        normalized = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "-" and (i == 0 or tokens[i - 1] in "+-*/"):
                if i + 1 >= len(tokens):
                    raise ValueError("Invalid unary minus")
                normalized.append(str(-float(tokens[i + 1])))
                i += 2
            else:
                normalized.append(tokens[i])
                i += 1
        return normalized

    def compute_mul_div(self, tokens):
        output = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in "*/":
                if not output:
                    raise ValueError("Operator position error")
                left = float(output.pop())
                right = float(tokens[i + 1])
                result = calculator.mul(left, right) if token == "*" else calculator.div(left, right)
                output.append(str(result))
                i += 2
            else:
                output.append(token)
                i += 1
        return output

    def compute_add_sub(self, tokens):
        result = float(tokens[0])
        i = 1
        while i < len(tokens):
            op = tokens[i]
            right = float(tokens[i + 1])
            if op == "+":
                result = calculator.add(result, right)
            elif op == "-":
                result = calculator.sub(result, right)
            i += 2
        return result

    def format_value(self, value):
        if value == int(value):
            return str(int(value))
        return str(round(value, 10)).rstrip("0").rstrip(".")

    def save_history(self, expression, result):
        line = f"{expression} = {result}"
        self.history.append(line)
        try:
            with open("history.txt", "a", encoding="utf-8") as history:
                history.write(line + "\n")
        except OSError:
            pass

    def load_history(self):
        try:
            with open("history.txt", "r", encoding="utf-8") as history:
                self.history = [line.strip() for line in history if line.strip()]
        except FileNotFoundError:
            self.history = []

    def show_history(self):
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        self.history_window = tk.Toplevel(self.window)
        self.history_window.title("History")
        self.history_window.geometry("360x420")
        self.history_window.configure(bg="#222831")
        self.history_window.resizable(False, False)

        title = tk.Label(
            self.history_window,
            text="Calculation History",
            fg="#eeeeee",
            bg="#222831",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(pady=(14, 8))

        history_frame = tk.Frame(self.history_window, bg="#222831")
        history_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        history_text = tk.Text(
            history_frame,
            bg="#393e46",
            fg="#eeeeee",
            bd=0,
            font=("Segoe UI", 14),
            padx=10,
            pady=10,
            wrap="word",
        )
        history_text.pack(fill="both", expand=True, side="left")
        history_text.insert("1.0", "\n".join(self.history) or "No history yet.")
        history_text.configure(state="disabled")

        scrollbar = tk.Scrollbar(history_frame, command=history_text.yview)
        scrollbar.pack(side="right", fill="y")
        history_text.configure(yscrollcommand=scrollbar.set)

        close_btn = tk.Button(
            self.history_window,
            text="Close",
            command=self.history_window.destroy,
            fg="#eeeeee",
            bg="#00adb5",
            activebackground="#00c5dd",
            activeforeground="#222831",
            font=("Segoe UI", 14, "bold"),
            bd=0,
            relief="ridge",
        )
        close_btn.pack(pady=(0, 12), ipadx=10, ipady=6)

    def create_hover_effect(self, button):
        normal_bg = button["bg"]
        hover_bg = "#00adb5"

        def enter(event):
            button.configure(bg=hover_bg)

        def leave(event):
            button.configure(bg=normal_bg)

        button.bind("<Enter>", enter)
        button.bind("<Leave>", leave)

    def on_keypress(self, event):
        key = event.keysym
        char = event.char

        if key in ("Return", "KP_Enter"):
            self.evaluate()
            return
        if key == "BackSpace":
            self.delete_last()
            return
        if key == "Escape":
            self.clear()
            return
        if key.lower() == "h":
            self.show_history()
            return
        if char in "0123456789.+-*/":
            self.append_text(char)
            return

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    CalculatorApp().run()