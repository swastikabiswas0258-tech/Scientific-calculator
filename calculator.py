"""
Professional Scientific Calculator (Light Blue Theme) with Replay Button
--------------------------------------------------------------------------
Features:
- Clean, modern light-blue color scheme
- Standard + scientific functions (sin, cos, tan, log, ln, sqrt, x^2, x^y, 1/x, pi, e)
- History panel showing past calculations
- "Replay" button that re-executes the last successful calculation

Run with: python scientific_calculator_pro.py
"""

import tkinter as tk
from tkinter import messagebox
import math


# ---------------------- COLOR PALETTE ----------------------
BG_MAIN      = "#eaf4fb"   # very light blue background
BG_DISPLAY   = "#ffffff"   # white display
BG_HISTORY   = "#f4fafd"   # near-white light blue for history box
COLOR_NUM    = "#ffffff"   # number buttons - white
COLOR_NUM_FG = "#1b3a4b"   # dark blue-gray text
COLOR_OP     = "#bfe3f7"   # operator buttons - light blue
COLOR_OP_FG  = "#0b3d5c"   # darker blue text
COLOR_SCI    = "#d8ecf9"   # scientific function buttons - lighter blue
COLOR_SCI_FG = "#0b3d5c"
COLOR_EQUAL  = "#2f9bd6"   # equals button - vivid blue
COLOR_EQUAL_FG = "#ffffff"
COLOR_CLEAR  = "#7fb8dd"   # clear button
COLOR_CLEAR_FG = "#ffffff"
COLOR_REPLAY = "#1c7ed6"   # replay button - strong blue
COLOR_REPLAY_FG = "#ffffff"
COLOR_REPLAY_HOVER = "#1565c0"
BORDER_COLOR = "#a9d2ec"


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.expression = ""
        self.last_expression = ""
        self.last_result = ""

        self._build_display()
        self._build_history()
        self._build_buttons()
        self._build_replay_button()

    # ---------------------------------------------------------
    def _build_display(self):
        frame = tk.Frame(self.root, bg=BG_MAIN)
        frame.grid(row=0, column=0, columnspan=5, padx=12, pady=(12, 6), sticky="nsew")

        self.display_var = tk.StringVar()
        display = tk.Entry(
            frame, textvariable=self.display_var, font=("Segoe UI", 24),
            bd=0, justify="right", state="readonly",
            readonlybackground=BG_DISPLAY, fg="#0b2f45",
            highlightthickness=2, highlightbackground=BORDER_COLOR,
            highlightcolor=COLOR_EQUAL
        )
        display.pack(fill="both", ipady=14)

    # ---------------------------------------------------------
    def _build_history(self):
        frame = tk.Frame(self.root, bg=BG_MAIN)
        frame.grid(row=1, column=0, columnspan=5, padx=12, pady=(0, 8), sticky="nsew")

        tk.Label(
            frame, text="History", font=("Segoe UI", 9, "bold"),
            bg=BG_MAIN, fg="#3a6b8a"
        ).pack(anchor="w")

        self.history_box = tk.Listbox(
            frame, height=5, font=("Consolas", 10),
            bg=BG_HISTORY, fg="#264a5e", bd=0,
            highlightthickness=1, highlightbackground=BORDER_COLOR,
            selectbackground=COLOR_OP
        )
        self.history_box.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    def _make_button(self, parent, text, bg, fg, command, font_size=13):
        btn = tk.Button(
            parent, text=text, font=("Segoe UI", font_size, "bold"),
            bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
            bd=0, relief="flat", width=6, height=2, cursor="hand2",
            command=command
        )
        return btn

    def _build_buttons(self):
        grid_frame = tk.Frame(self.root, bg=BG_MAIN)
        grid_frame.grid(row=2, column=0, columnspan=5, padx=12, pady=4, sticky="nsew")

        buttons = [
            ("sin", 0, 0, COLOR_SCI, COLOR_SCI_FG), ("cos", 0, 1, COLOR_SCI, COLOR_SCI_FG),
            ("tan", 0, 2, COLOR_SCI, COLOR_SCI_FG), ("log", 0, 3, COLOR_SCI, COLOR_SCI_FG),
            ("ln", 0, 4, COLOR_SCI, COLOR_SCI_FG),

            ("(", 1, 0, COLOR_SCI, COLOR_SCI_FG), (")", 1, 1, COLOR_SCI, COLOR_SCI_FG),
            ("√", 1, 2, COLOR_SCI, COLOR_SCI_FG), ("x²", 1, 3, COLOR_SCI, COLOR_SCI_FG),
            ("xʸ", 1, 4, COLOR_SCI, COLOR_SCI_FG),

            ("7", 2, 0, COLOR_NUM, COLOR_NUM_FG), ("8", 2, 1, COLOR_NUM, COLOR_NUM_FG),
            ("9", 2, 2, COLOR_NUM, COLOR_NUM_FG), ("/", 2, 3, COLOR_OP, COLOR_OP_FG),
            ("1/x", 2, 4, COLOR_SCI, COLOR_SCI_FG),

            ("4", 3, 0, COLOR_NUM, COLOR_NUM_FG), ("5", 3, 1, COLOR_NUM, COLOR_NUM_FG),
            ("6", 3, 2, COLOR_NUM, COLOR_NUM_FG), ("*", 3, 3, COLOR_OP, COLOR_OP_FG),
            ("π", 3, 4, COLOR_SCI, COLOR_SCI_FG),

            ("1", 4, 0, COLOR_NUM, COLOR_NUM_FG), ("2", 4, 1, COLOR_NUM, COLOR_NUM_FG),
            ("3", 4, 2, COLOR_NUM, COLOR_NUM_FG), ("-", 4, 3, COLOR_OP, COLOR_OP_FG),
            ("e", 4, 4, COLOR_SCI, COLOR_SCI_FG),

            ("0", 5, 0, COLOR_NUM, COLOR_NUM_FG), (".", 5, 1, COLOR_NUM, COLOR_NUM_FG),
            ("C", 5, 2, COLOR_CLEAR, COLOR_CLEAR_FG), ("+", 5, 3, COLOR_OP, COLOR_OP_FG),
            ("=", 5, 4, COLOR_EQUAL, COLOR_EQUAL_FG),
        ]

        for (text, r, c, bg, fg) in buttons:
            btn = self._make_button(grid_frame, text, bg, fg, lambda t=text: self.on_button_click(t))
            btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        for i in range(5):
            grid_frame.grid_columnconfigure(i, weight=1)

    # ---------------------------------------------------------
    def _build_replay_button(self):
        self.replay_btn = tk.Button(
            self.root, text="⟳  Replay Last Calculation",
            font=("Segoe UI", 13, "bold"),
            bg=COLOR_REPLAY, fg=COLOR_REPLAY_FG,
            activebackground=COLOR_REPLAY_HOVER, activeforeground="#ffffff",
            bd=0, relief="flat", height=2, cursor="hand2",
            command=self.replay_last_calculation
        )
        self.replay_btn.grid(row=6, column=0, columnspan=5, padx=12, pady=(6, 12), sticky="nsew")

        # subtle hover effect
        self.replay_btn.bind("<Enter>", lambda e: self.replay_btn.config(bg=COLOR_REPLAY_HOVER))
        self.replay_btn.bind("<Leave>", lambda e: self.replay_btn.config(bg=COLOR_REPLAY))

    # ---------------------------------------------------------
    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.update_display("")
            return

        if char == "=":
            self.evaluate_expression()
            return

        mapping = {
            "sin": "math.sin(", "cos": "math.cos(", "tan": "math.tan(",
            "log": "math.log10(", "ln": "math.log(",
            "√": "math.sqrt(", "x²": "**2", "xʸ": "**",
            "1/x": "1/", "π": "math.pi", "e": "math.e",
        }

        self.expression += mapping.get(char, char)
        self.update_display(self.expression)

    # ---------------------------------------------------------
    def evaluate_expression(self, expr=None):
        expr_to_eval = expr if expr is not None else self.expression
        if not expr_to_eval:
            return

        try:
            result = eval(expr_to_eval, {"__builtins__": {}}, {"math": math})
            self.update_display(str(result))

            if expr is None:
                self.last_expression = expr_to_eval
                self.last_result = result
                self.expression = str(result)

            self.history_box.insert(tk.END, f"{expr_to_eval} = {result}")
            self.history_box.see(tk.END)

        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.expression = ""
            self.update_display("")

    # ---------------------------------------------------------
    def replay_last_calculation(self):
        if not self.last_expression:
            messagebox.showinfo("Replay", "No previous calculation to replay yet.")
            return

        self.evaluate_expression(expr=self.last_expression)
        self.history_box.insert(tk.END, f"↺ Replayed: {self.last_expression} = {self.last_result}")
        self.history_box.see(tk.END)

    # ---------------------------------------------------------
    def update_display(self, value):
        self.display_var.set(value)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()