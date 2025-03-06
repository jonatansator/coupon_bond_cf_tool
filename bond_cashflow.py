import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Step 1: Define bond payment calculation
def compute_payments(principal, rate, term, freq):
    periods = int(term * freq)
    payment = principal * (rate / freq)
    t = np.linspace(0, term, periods + 1)[1:]
    flows = [payment] * periods
    flows[-1] += principal
    return t, flows

# Step 2: Define result update function
def refresh_output():
    try:
        P = float(en1.get())
        R = float(en2.get()) / 100
        T = float(en3.get())
        F = float(en4.get())

        if P <= 0 or R < 0 or T <= 0 or F <= 0:
            raise ValueError("Inputs must be positive")
        if F not in [1, 2, 4]:
            raise ValueError("Frequency must be 1, 2, or 4")

        X, Y = compute_payments(P, R, T, F)

        total = sum(Y)
        lbl_sum.config(text=f"Total Cash Flow: ${total:,.2f}")
        lbl_count.config(text=f"Number of Periods: {len(X)}")

        ax.cla()
        ax.bar(X, Y, width=0.1, color='#4ECDC4', label='Payments')
        ax.set_xlabel('Time (Years)', color='white')
        ax.set_ylabel('Cash Flow ($)', color='white')
        ax.set_title('Bond Payment Schedule', color='white')
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.5)
        ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
        ax.tick_params(colors='white')
        canvas.draw()

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Step 3: Initialize GUI
win = tk.Tk()
win.title("Bond Payment Visualizer")
win.configure(bg='#1E1E1E')

frm = ttk.Frame(win, padding=10)
frm.pack()
frm.configure(style='Dark.TFrame')

# Step 4: Set up plotting area
fig, ax = plt.subplots(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig, master=frm)
canvas.get_tk_widget().pack(side=tk.LEFT)

# Step 5: Build input section
panel = ttk.Frame(frm)
panel.pack(side=tk.RIGHT, padx=10)
panel.configure(style='Dark.TFrame')

style = ttk.Style()
style.theme_use('default')
style.configure('Dark.TFrame', background='#1E1E1E')
style.configure('Dark.TLabel', background='#1E1E1E', foreground='white')
style.configure('TButton', background='#333333', foreground='white')
style.configure('TEntry', fieldbackground='#333333', foreground='white')

ttk.Label(panel, text="Principal ($):", style='Dark.TLabel').pack(pady=3)
en1 = ttk.Entry(panel); en1.pack(pady=3); en1.insert(0, "1000")
ttk.Label(panel, text="Rate (%):", style='Dark.TLabel').pack(pady=3)
en2 = ttk.Entry(panel); en2.pack(pady=3); en2.insert(0, "5")
ttk.Label(panel, text="Term (Years):", style='Dark.TLabel').pack(pady=3)
en3 = ttk.Entry(panel); en3.pack(pady=3); en3.insert(0, "10")
ttk.Label(panel, text="Payment Frequency:", style='Dark.TLabel').pack(pady=3)
en4 = ttk.Entry(panel); en4.pack(pady=3); en4.insert(0, "2")

ttk.Button(panel, text="Update", command=refresh_output).pack(pady=10)

lbl_sum = ttk.Label(panel, text="Total Cash Flow: ", style='Dark.TLabel'); lbl_sum.pack(pady=2)
lbl_count = ttk.Label(panel, text="Number of Periods: ", style='Dark.TLabel'); lbl_count.pack(pady=2)

# Step 6: Run initial calculation and start GUI
refresh_output()
win.mainloop()