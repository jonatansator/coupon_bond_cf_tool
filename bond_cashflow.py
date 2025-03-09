import numpy as np
import numpy_financial as npf  # Added for YTM calculation
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Step 1: Define bond payment calculation
def compute_payments(principal, rate, term, freq, price=None):
    periods = int(term * freq)
    coupon = principal * (rate / freq)
    t = np.linspace(0, term, periods + 1)[1:]
    flows = [coupon] * periods
    flows[-1] += principal
    
    # Calculate YTM if price is provided, otherwise assume par (YTM = coupon rate)
    if price is None:
        ytm = rate
    else:
        cash_flows = np.array(flows)
        ytm = npf.irr([-price] + cash_flows) * freq  # Annualized YTM
    
    # Calculate Macaulay duration
    pv_cash_flows = [(cf / (1 + ytm / freq) ** (i + 1)) for i, cf in enumerate(flows)]
    time_weighted = [(i + 1) / freq * pv for i, pv in enumerate(pv_cash_flows)]
    duration = sum(time_weighted) / sum(pv_cash_flows)
    
    return t, flows, ytm, duration

# Step 2: Define result update function
def refresh_output():
    try:
        P = float(en1.get())
        R = float(en2.get()) / 100
        T = float(en3.get())
        F = float(en4.get())
        price_input = en5.get()
        price = float(price_input) if price_input else P  # Default to par if empty

        if P <= 0 or R < 0 or T <= 0 or F <= 0 or price <= 0:
            raise ValueError("Inputs must be positive")
        if F not in [1, 2, 4]:
            raise ValueError("Frequency must be 1, 2, or 4")

        X, Y, ytm, duration = compute_payments(P, R, T, F, price)

        total = sum(Y)
        lbl_sum.config(text=f"Total Cash Flow: ${total:,.2f}")
        lbl_count.config(text=f"Payment Periods: {len(X)}")
        lbl_ytm.config(text=f"YTM: {ytm * 100:.2f}%")
        lbl_dur.config(text=f"Macaulay Duration: {duration:.2f} years")

        ax.cla()
        bar_width = max(0.1, 0.8 / (len(X) + 1)) 
        colors = ['#4ECDC4'] * len(X)
        colors[-1] = '#FF6B6B'  # Final payment in red
        bars = ax.bar(X, Y, width=bar_width, color=colors, edgecolor='#2B2B2B')
        
        ax.set_xlabel('Time (Years)', fontsize=12, color='white')
        ax.set_ylabel('Cash Flow ($)', fontsize=12, color='white')
        ax.set_title(f'Bond Cash Flow Schedule\nPrincipal=${P:,.0f}, Rate={R*100:.1f}%, Term={T}y, Freq={int(F)}/yr', 
                     fontsize=12, color='white', pad=10)
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.3)
        ax.tick_params(colors='white', labelsize=8)

     
        if len(X) > 10:
            ax.set_xticks(X[::int(len(X)/5)])  # Show ~5 ticks

        # Label first and last bar
        ax.text(X[0], Y[0] + P * 0.02, f'${Y[0]:,.0f}', ha='center', va='bottom', color='white', fontsize=8)
        ax.text(X[-1], Y[-1] + P * 0.02, f'${Y[-1]:,.0f}', ha='center', va='bottom', color='white', fontsize=8)

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
fig, ax = plt.subplots(figsize=(8, 5))  
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
ttk.Label(panel, text="Coupon Rate (%):", style='Dark.TLabel').pack(pady=3)
en2 = ttk.Entry(panel); en2.pack(pady=3); en2.insert(0, "5")
ttk.Label(panel, text="Term (Years):", style='Dark.TLabel').pack(pady=3)
en3 = ttk.Entry(panel); en3.pack(pady=3); en3.insert(0, "10")
ttk.Label(panel, text="Frequency (1, 2, 4):", style='Dark.TLabel').pack(pady=3)
en4 = ttk.Entry(panel); en4.pack(pady=3); en4.insert(0, "2")
ttk.Label(panel, text="Price ($, optional):", style='Dark.TLabel').pack(pady=3)
en5 = ttk.Entry(panel); en5.pack(pady=3); en5.insert(0, "")  # Optional price

ttk.Button(panel, text="Update", command=refresh_output).pack(pady=10)

lbl_sum = ttk.Label(panel, text="Total Cash Flow: ", style='Dark.TLabel'); lbl_sum.pack(pady=2)
lbl_count = ttk.Label(panel, text="Payment Periods: ", style='Dark.TLabel'); lbl_count.pack(pady=2)
lbl_ytm = ttk.Label(panel, text="YTM: ", style='Dark.TLabel'); lbl_ytm.pack(pady=2)
lbl_dur = ttk.Label(panel, text="Macaulay Duration: ", style='Dark.TLabel'); lbl_dur.pack(pady=2)

# Step 6: Run initial calculation and start GUI
refresh_output()
win.mainloop()
