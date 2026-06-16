import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats


# ── helpers ──────────────────────────────────────────────────────────────────

def generate_sample_data():
    """Return synthetic student grades (100 values, clipped 0–100)."""
    np.random.seed(42)
    return np.random.normal(loc=75, scale=12, size=100).clip(0, 100)


def calculate_mode(data):
    """Return the true mode value(s), or a message when no mode exists."""
    values, counts = np.unique(data, return_counts=True)
    highest_frequency = counts.max()

    # A dataset has no mode when every value occurs only once.
    if highest_frequency == 1:
        return "No mode"

    # Include every value tied for the highest frequency.
    modes = values[counts == highest_frequency]

    def format_mode_value(value):
        """Display whole numbers cleanly and preserve decimal values."""
        if np.isclose(value, round(value)):
            return str(int(round(value)))
        return f"{value:.4f}".rstrip("0").rstrip(".")

    return ", ".join(format_mode_value(value) for value in modes)


def compute_stats(data):
    """Return a dict of descriptive statistics for *data*."""
    mode_value = calculate_mode(data)

    return {
        "Count":    len(data),
        "Min":      np.min(data),
        "Max":      np.max(data),
        "Range":    np.max(data) - np.min(data),
        "Mean":     np.mean(data),
        "Median":   np.median(data),
        "Mode":     mode_value,
        "Std Dev":  np.std(data, ddof=1),
        "Variance": np.var(data, ddof=1),
        "Skewness": stats.skew(data),
        "Kurtosis": stats.kurtosis(data),
        "Q1":       np.percentile(data, 25),
        "Q3":       np.percentile(data, 75),
        "IQR":      np.percentile(data, 75) - np.percentile(data, 25),
    }


# ── main app ─────────────────────────────────────────────────────────────────

class StatsDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basic Descriptive Statistics Dashboard")
        self.geometry("1100x720")
        self.resizable(True, True)
        self.configure(bg="#f0f4f8")

        self.data = generate_sample_data()   # active dataset

        self._build_ui()
        self._refresh()                       # draw everything on start

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        # ── top toolbar ──────────────────────────────────────────────────────
        toolbar = tk.Frame(self, bg="#1e3a5f", pady=8)
        toolbar.pack(fill="x")

        tk.Label(
            toolbar, text="📊  Descriptive Statistics Dashboard",
            font=("Helvetica", 15, "bold"),
            bg="#1e3a5f", fg="white"
        ).pack(side="left", padx=15)

        btn_style = {"bg": "#4a90d9", "fg": "white", "relief": "flat",
                     "font": ("Helvetica", 10, "bold"), "padx": 10, "pady": 4,
                     "cursor": "hand2"}

        tk.Button(toolbar, text="🔄  New Sample",
                  command=self._new_sample, **btn_style).pack(side="right", padx=6)
        tk.Button(toolbar, text="📂  Load CSV",
                  command=self._load_csv, **btn_style).pack(side="right", padx=6)

        # ── main body: left = stats table, right = charts ────────────────────
        body = tk.Frame(self, bg="#f0f4f8")
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # left panel – stats table
        left = tk.Frame(body, bg="#f0f4f8")
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="Summary Statistics",
                 font=("Helvetica", 12, "bold"),
                 bg="#f0f4f8", fg="#1e3a5f").pack(anchor="w", pady=(0, 6))

        self._build_stats_table(left)

        # right panel – charts
        right = tk.Frame(body, bg="#f0f4f8")
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Visualizations",
                 font=("Helvetica", 12, "bold"),
                 bg="#f0f4f8", fg="#1e3a5f").pack(anchor="w", pady=(0, 6))

        self._build_charts(right)
        # ── interpretation panel ─────────────────────────────────────────────
        interp_frame = tk.Frame(self, bg="#e8f0fe", bd=1, relief="solid")
        interp_frame.pack(fill="x", padx=12, pady=(0, 6))

        tk.Label(interp_frame, text="📝  Interpretation",
                 font=("Helvetica", 10, "bold"),
                 bg="#e8f0fe", fg="#1e3a5f").pack(anchor="w", padx=10, pady=(6, 2))

        self.interp_var = tk.StringVar()
        tk.Label(interp_frame, textvariable=self.interp_var,
                 font=("Helvetica", 9), bg="#e8f0fe", fg="#333",
                 anchor="w", justify="left", wraplength=1060,
                 padx=10).pack(anchor="w", pady=(0, 6))
        # ── status bar ───────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Using generated sample data (n=100)")
        tk.Label(self, textvariable=self.status_var,
                 font=("Helvetica", 9), bg="#d0dce8", fg="#333",
                 anchor="w", padx=10).pack(fill="x", side="bottom")

    def _build_stats_table(self, parent):
        """Create the Treeview that shows stat name / value."""
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="y", expand=True)

        cols = ("Statistic", "Value")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings",
                                 height=14, selectmode="none")

        style = ttk.Style()
        style.configure("Treeview.Heading",
                         font=("Helvetica", 10, "bold"), background="#1e3a5f",
                         foreground="black")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=26)
        style.map("Treeview", background=[("selected", "#d0e8ff")])

        self.tree.heading("Statistic", text="Statistic")
        self.tree.heading("Value",     text="Value")
        self.tree.column("Statistic",  width=120, anchor="w")
        self.tree.column("Value",      width=100, anchor="e")

        self.tree.tag_configure("odd",  background="#f7f9fc")
        self.tree.tag_configure("even", background="#ffffff")

        self.tree.pack(fill="both", expand=True)

    def _build_charts(self, parent):
        """Embed a matplotlib Figure with histogram + box-plot."""
        self.fig, (self.ax_hist, self.ax_box) = plt.subplots(
            1, 2, figsize=(8, 4.2), facecolor="#f0f4f8"
        )
        self.fig.subplots_adjust(wspace=0.35)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ── data / refresh logic ─────────────────────────────────────────────────

    def _refresh(self):
        """Re-compute stats and redraw charts from self.data."""
        s = compute_stats(self.data)
        self._update_table(s)
        self._update_interpretation(s)
        self._update_charts(s)

    def _update_table(self, s):
        """Clear and repopulate the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, (name, val) in enumerate(s.items()):
            tag = "odd" if i % 2 else "even"
            display_value = val if isinstance(val, str) else f"{val:.4f}"
            self.tree.insert(
                "",
                "end",
                values=(name, display_value),
                tags=(tag,)
            )

    def _update_interpretation(self, s):
        skew_desc = (
            "approximately symmetric" if abs(s["Skewness"]) < 0.5
            else ("positively skewed (tail to the right)" if s["Skewness"] > 0
                  else "negatively skewed (tail to the left)")
        )
        kurt_desc = (
            "normal-tailed (mesokurtic)" if abs(s["Kurtosis"]) < 0.5
            else ("heavy-tailed (leptokurtic)" if s["Kurtosis"] > 0
                  else "light-tailed (platykurtic)")
        )
        text = (
            f"The dataset has {int(s['Count'])} values ranging from {s['Min']:.1f} to {s['Max']:.1f} "
            f"(Range = {s['Range']:.1f}).  "
            f"The center is around a mean of {s['Mean']:.1f} and median of {s['Median']:.1f}.  "
            f"The spread is {s['Std Dev']:.1f} (std dev) with an IQR of {s['IQR']:.1f}, "
            f"indicating {'moderate' if s['IQR'] < 20 else 'wide'} variability.  "
            f"The distribution is {skew_desc} (skewness = {s['Skewness']:.2f}) "
            f"and {kurt_desc} (kurtosis = {s['Kurtosis']:.2f})."
        )
        self.interp_var.set(text)

    def _update_charts(self, s):
        """Redraw histogram and box-plot."""
        self.ax_hist.clear()
        self.ax_box.clear()

        grades = self.data

        # ── histogram ────────────────────────────────────────────────────────
        self.ax_hist.hist(grades, bins=20, color="#4a90d9",
                          edgecolor="white", alpha=0.85)
        self.ax_hist.axvline(s["Mean"],   color="#e74c3c",
                             linestyle="--", linewidth=1.8,
                             label=f"Mean = {s['Mean']:.1f}")
        self.ax_hist.axvline(s["Median"], color="#2ecc71",
                             linestyle="--", linewidth=1.8,
                             label=f"Median = {s['Median']:.1f}")
        self.ax_hist.set_title("Grade Distribution", fontsize=11, fontweight="bold")
        self.ax_hist.set_xlabel("Grade")
        self.ax_hist.set_ylabel("Frequency")
        self.ax_hist.legend(fontsize=9)
        self.ax_hist.set_facecolor("#fafcff")

        # ── box-plot ─────────────────────────────────────────────────────────
        bp = self.ax_box.boxplot(grades, vert=True, patch_artist=True,
                                 boxprops=dict(facecolor="#4a90d9", alpha=0.6),
                                 medianprops=dict(color="#e74c3c", linewidth=2),
                                 whiskerprops=dict(linewidth=1.5),
                                 capprops=dict(linewidth=1.5),
                                 flierprops=dict(marker="o", markerfacecolor="#e74c3c",
                                                 markersize=5, alpha=0.6))
        self.ax_box.set_title("Box Plot of Grades", fontsize=11, fontweight="bold")
        self.ax_box.set_ylabel("Grade")
        self.ax_box.set_xticks([])
        self.ax_box.set_facecolor("#fafcff")

        # annotate quartiles
        for label, val, side in [("Q1", s["Q1"], -0.35),
                                   ("Med", s["Median"], -0.35),
                                   ("Q3", s["Q3"], -0.35)]:
            self.ax_box.text(1 + side, val, f"{label}={val:.1f}",
                             fontsize=7.5, va="center", color="#333")

        self.fig.tight_layout()
        self.canvas.draw()

    # ── button callbacks ─────────────────────────────────────────────────────

    def _new_sample(self):
        """Generate a fresh random dataset."""
        np.random.seed(None)   # different seed each time
        self.data = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)
        self.status_var.set("Using newly generated sample data (n=100)")
        self._refresh()

    def _load_csv(self):
        """Let the user pick a CSV; use its first numeric column."""
        path = filedialog.askopenfilename(
            title="Open CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            df = pd.read_csv(path)
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if not numeric_cols:
                messagebox.showerror("No numeric data",
                                     "The CSV has no numeric columns.")
                return

            # if multiple numeric columns, let user pick one
            if len(numeric_cols) == 1:
                col = numeric_cols[0]
            else:
                col = self._pick_column(numeric_cols)
                if col is None:
                    return

            self.data = df[col].dropna().to_numpy()
            self.status_var.set(
                f"Loaded '{col}' from {path.split('/')[-1]}  (n={len(self.data)})"
            )
            self._refresh()
        except Exception as exc:
            messagebox.showerror("Error loading CSV", str(exc))

    def _pick_column(self, columns):
        """Simple popup to choose one column from a list."""
        win = tk.Toplevel(self)
        win.title("Choose column")
        win.geometry("260x200")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="Select a numeric column:",
                 font=("Helvetica", 10)).pack(pady=10)

        chosen = tk.StringVar(value=columns[0])
        lb = tk.Listbox(win, listvariable=tk.StringVar(value=columns),
                        selectmode="single", height=6)
        lb.pack(fill="x", padx=20)
        lb.select_set(0)

        result = [None]

        def ok():
            sel = lb.curselection()
            result[0] = columns[sel[0]] if sel else columns[0]
            win.destroy()

        tk.Button(win, text="OK", command=ok,
                  bg="#4a90d9", fg="white", padx=12).pack(pady=10)
        self.wait_window(win)
        return result[0]


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = StatsDashboard()
    app.mainloop()
