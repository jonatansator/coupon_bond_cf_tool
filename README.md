# coupon_bond_cf_tool

- This project calculates and visualizes the cash flow schedule of a coupon bond based on user-defined inputs.
- It uses a Tkinter GUI for input and Matplotlib for plotting the payment schedule.

---

## Files
- `bond_cashflow.py`: Main script for computing bond payments and displaying the GUI with visualization.
- `output.png`: Plot.

---

## Libraries Used
- `numpy`
- `matplotlib`
- `tkinter`

---

## Features
- **Inputs**: 
  - Principal amount (in dollars)
  - Annual coupon rate (in percentage)
  - Term (in years)
  - Payment frequency (1, 2, or 4 times per year)
- **Outputs**: 
  - Bar chart of cash flows over time (including coupon payments and final principal repayment)
  - Total cash flow sum
  - Number of payment periods
