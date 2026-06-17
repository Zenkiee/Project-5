import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats


# ── helpers ──────────────────────────────────────────────────────────────────

def generate_sample_data():
    """Return synthetic student grades (100 values, clipped 0–100)."""
    np.random.seed(42)
    return np.random.normal(loc=75, scale=12, size=100).clip(0, 100)


def calculate_mode(data):
    values, counts = np.unique(data, return_counts=True)
    highest_frequency = counts.max()
    if highest_frequency == 1:
        return "No mode"
    modes = values[counts == highest_frequency]
    def format_mode_value(value):
        if np.isclose(value, round(value)):
            return str(int(round(value)))
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return ", ".join(format_mode_value(value) for value in modes)


def compute_stats(data):
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


def justify_text(text, width=95):
    lines = textwrap.wrap(text, width=width)
    justified_lines = []
    for i, line in enumerate(lines):
        words = line.split()
        if i == len(lines) - 1 or len(words) == 1:
            justified_lines.append(line)
            continue
        total_padding = width - sum(len(w) for w in words)
        gap_count = len(words) - 1
        base_spaces, extra_spaces = divmod(total_padding, gap_count)
        justified_line = ""
        for j, word in enumerate(words[:-1]):
            spaces = base_spaces + (1 if j < extra_spaces else 0)
            justified_line += word + " " * spaces
        justified_line += words[-1]
        justified_lines.append(justified_line)
    return "\n".join(justified_lines)


# ── main app ─────────────────────────────────────────────────────────────────

class StatsDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basic Descriptive Statistics Dashboard")
        self.geometry("1100x720")
        self.resizable(False, False)
        self.configure(bg="#f0f4f8")

        self.data = generate_sample_data()
        self._showing_data = False

        self._build_ui()
        self._refresh()

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
        tk.Button(toolbar, text="📄  Export PDF",
                  command=self._export_report, **btn_style).pack(side="right", padx=6)
        tk.Button(toolbar, text="🗃️  View Data",
                  command=self._toggle_view, **btn_style).pack(side="right", padx=6)

        # ── main content area (swappable frames) ─────────────────────────────
        self.content = tk.Frame(self, bg="#f0f4f8")
        self.content.pack(fill="both", expand=True, padx=12, pady=10)

        self.frame_dashboard = tk.Frame(self.content, bg="#f0f4f8")
        self.frame_dashboard.place(relwidth=1, relheight=1)

        self.frame_data = tk.Frame(self.content, bg="#f0f4f8")
        self.frame_data.place(relwidth=1, relheight=1)

        self._build_dashboard(self.frame_dashboard)
        self._build_data_viewer(self.frame_data)

        self.frame_dashboard.lift()

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

    # ── Dashboard tab ─────────────────────────────────────────────────────────

    def _build_dashboard(self, parent):
        body = tk.Frame(parent, bg="#f0f4f8")
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="#f0f4f8")
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="Summary Statistics",
                 font=("Helvetica", 12, "bold"),
                 bg="#f0f4f8", fg="#1e3a5f").pack(anchor="w", pady=(0, 6))
        self._build_stats_table(left)

        right = tk.Frame(body, bg="#f0f4f8")
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Visualizations",
                 font=("Helvetica", 12, "bold"),
                 bg="#f0f4f8", fg="#1e3a5f").pack(anchor="w", pady=(0, 6))
        self._build_charts(right)

    def _build_stats_table(self, parent):
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
        self.fig, (self.ax_hist, self.ax_box) = plt.subplots(
            1, 2, figsize=(8, 4.2), facecolor="#f0f4f8"
        )
        self.fig.subplots_adjust(wspace=0.35)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ── Data Viewer tab ───────────────────────────────────────────────────────

    def _build_data_viewer(self, parent):
        header = tk.Frame(parent, bg="#f0f4f8")
        header.pack(fill="x", pady=(0, 6))

        tk.Label(header, text="Raw Data Values",
                 font=("Helvetica", 12, "bold"),
                 bg="#f0f4f8", fg="#1e3a5f").pack(side="left")

        self.data_count_var = tk.StringVar()
        tk.Label(header, textvariable=self.data_count_var,
                 font=("Helvetica", 10), bg="#f0f4f8", fg="#555").pack(side="left", padx=12)

        tk.Label(header, text="🔍 Search:",
                 font=("Helvetica", 10), bg="#f0f4f8").pack(side="left", padx=(20, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_data_table)
        tk.Entry(header, textvariable=self.search_var,
                 font=("Helvetica", 10), width=14,
                 bd=1, relief="solid").pack(side="left")

        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True)

        cols = ("#", "Value")
        self.data_tree = ttk.Treeview(frame, columns=cols, show="headings",
                                      selectmode="browse")

        style = ttk.Style()
        style.configure("DataView.Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("DataView.Treeview", font=("Helvetica", 10), rowheight=24)
        self.data_tree.configure(style="DataView.Treeview")

        for col, width, anchor in [("#", 60, "center"), ("Value", 110, "e")]:
            self.data_tree.heading(col, text=col,
                                   command=lambda c=col: self._sort_data_col(c))
            self.data_tree.column(col, width=width, anchor=anchor, stretch=False)

        self.data_tree.tag_configure("odd",  background="#f7f9fc")
        self.data_tree.tag_configure("even", background="#ffffff")

        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.data_tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.data_tree.xview)
        self.data_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.data_tree.pack(fill="both", expand=True)

        legend = tk.Frame(parent, bg="#f0f4f8")
        legend.pack(fill="x", pady=(4, 0))
        tk.Label(legend, text="Click column headers to sort",
                 font=("Helvetica", 8), bg="#f0f4f8", fg="#666").pack(side="left")

        self._sort_col = "#"
        self._sort_asc = True
        self._all_rows = []

    # ── refresh logic ─────────────────────────────────────────────────────────

    def _refresh(self):
        s = compute_stats(self.data)
        self._update_table(s)
        self._update_interpretation(s)
        self._update_charts(s)
        self._populate_data_viewer()

    def _update_table(self, s):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, (name, val) in enumerate(s.items()):
            tag = "odd" if i % 2 else "even"
            display_value = val if isinstance(val, str) else f"{val:.4f}"
            self.tree.insert("", "end", values=(name, display_value), tags=(tag,))

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
        self.ax_hist.clear()
        self.ax_box.clear()
        grades = self.data

        self.ax_hist.hist(grades, bins=20, color="#4a90d9", edgecolor="white", alpha=0.85)
        self.ax_hist.axvline(s["Mean"],   color="#e74c3c", linestyle="--", linewidth=1.8,
                             label=f"Mean = {s['Mean']:.1f}")
        self.ax_hist.axvline(s["Median"], color="#2ecc71", linestyle="--", linewidth=1.8,
                             label=f"Median = {s['Median']:.1f}")
        self.ax_hist.set_title("Grade Distribution", fontsize=11, fontweight="bold")
        self.ax_hist.set_xlabel("Grade")
        self.ax_hist.set_ylabel("Frequency")
        self.ax_hist.legend(fontsize=9)
        self.ax_hist.set_facecolor("#fafcff")

        self.ax_box.boxplot(grades, orientation="vertical", patch_artist=True,
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

        for label, val, side in [("Q1", s["Q1"], -0.35),
                                   ("Med", s["Median"], -0.35),
                                   ("Q3", s["Q3"], -0.35)]:
            self.ax_box.text(1 + side, val, f"{label}={val:.1f}",
                             fontsize=7.5, va="center", color="#333")

        self.fig.tight_layout()
        self.canvas.draw()

    # ── data viewer logic ─────────────────────────────────────────────────────

    def _populate_data_viewer(self):
        self._all_rows = [(i, v) for i, v in enumerate(self.data, start=1)]
        self.data_count_var.set(f"({len(self.data)} values)")
        self._render_data_table(self._all_rows)

    def _render_data_table(self, rows):
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        for stripe, (idx, val) in enumerate(rows):
            tag = "odd" if stripe % 2 else "even"
            self.data_tree.insert("", "end", values=(idx, f"{val:.4f}"), tags=(tag,))

    def _filter_data_table(self, *_):
        query = self.search_var.get().strip().lower()
        if not query:
            self._render_data_table(self._all_rows)
            return
        filtered = [r for r in self._all_rows
                    if query in str(r[0]) or query in f"{r[1]:.4f}"]
        self._render_data_table(filtered)

    def _sort_data_col(self, col):
        col_map = {"#": 0, "Value": 1}
        key_idx = col_map[col]
        if self._sort_col == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_col = col
            self._sort_asc = True

        sorted_rows = sorted(self._all_rows, key=lambda r: r[key_idx],
                             reverse=not self._sort_asc)
        query = self.search_var.get().strip().lower()
        if query:
            sorted_rows = [r for r in sorted_rows
                           if query in str(r[0]) or query in f"{r[1]:.4f}"]
        self._render_data_table(sorted_rows)

        for c in ["#", "Value"]:
            arrow = (" ▲" if self._sort_asc else " ▼") if c == col else ""
            self.data_tree.heading(c, text=c + arrow,
                                   command=lambda c=c: self._sort_data_col(c))

    # ── toggle view ───────────────────────────────────────────────────────────

    def _toggle_view(self):
        self._showing_data = not self._showing_data
        if self._showing_data:
            self.frame_data.lift()
        else:
            self.frame_dashboard.lift()

    # ── button callbacks ─────────────────────────────────────────────────────

    def _new_sample(self):
        np.random.seed(None)
        self.data = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)
        self.status_var.set("Using newly generated sample data (n=100)")
        self._refresh()

    def _load_csv(self):
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
                messagebox.showerror("No numeric data", "The CSV has no numeric columns.")
                return
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
        win = tk.Toplevel(self)
        win.title("Choose column")
        win.geometry("260x200")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="Select a numeric column:",
                 font=("Helvetica", 10)).pack(pady=10)

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

    def _export_report(self):
        path = filedialog.asksaveasfilename(
            title="Save PDF Report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            self._generate_pdf_report(path)
            messagebox.showinfo("Export Successful", f"Report saved to:\n{path}")
        except Exception as exc:
            messagebox.showerror("Error exporting report", str(exc))

    def _generate_pdf_report(self, path):
        s = compute_stats(self.data)

        fig = plt.figure(figsize=(8.5, 11), facecolor="white")
        gs = fig.add_gridspec(4, 2, height_ratios=[0.5, 3.3, 2.7, 1.5],
                              hspace=0.65, wspace=0.3)

        ax_title = fig.add_subplot(gs[0, :])
        ax_title.axis("off")
        ax_title.text(0.5, 0.7, "Descriptive Statistics Report",
                      ha="center", va="center", fontsize=18, fontweight="bold",
                      color="#1e3a5f")
        ax_title.text(0.5, 0.15, self.status_var.get(),
                      ha="center", va="center", fontsize=9, color="#555")

        ax_table = fig.add_subplot(gs[1, :])
        ax_table.axis("off")
        rows = [[name, val if isinstance(val, str) else f"{val:.4f}"]
                for name, val in s.items()]
        table = ax_table.table(cellText=rows, colLabels=["Statistic", "Value"],
                               cellLoc="center", loc="center", bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        for (row, _col), cell in table.get_celld().items():
            cell.PAD = 0.12
            if row == 0:
                cell.set_facecolor("#1e3a5f")
                cell.set_text_props(color="white", fontweight="bold")
            else:
                cell.set_facecolor("#f7f9fc" if row % 2 == 0 else "#ffffff")

        ax_hist = fig.add_subplot(gs[2, 0])
        ax_hist.hist(self.data, bins=20, color="#4a90d9", edgecolor="white", alpha=0.85)
        ax_hist.axvline(s["Mean"], color="#e74c3c", linestyle="--", linewidth=1.5,
                        label=f"Mean = {s['Mean']:.1f}")
        ax_hist.axvline(s["Median"], color="#2ecc71", linestyle="--", linewidth=1.5,
                        label=f"Median = {s['Median']:.1f}")
        ax_hist.set_title("Grade Distribution", fontsize=10, fontweight="bold")
        ax_hist.set_xlabel("Grade")
        ax_hist.set_ylabel("Frequency")
        ax_hist.legend(fontsize=7)

        ax_box = fig.add_subplot(gs[2, 1])
        ax_box.boxplot(self.data, orientation="vertical", patch_artist=True,
                       boxprops=dict(facecolor="#4a90d9", alpha=0.6),
                       medianprops=dict(color="#e74c3c", linewidth=2),
                       flierprops=dict(marker="o", markerfacecolor="#e74c3c",
                                       markersize=5, alpha=0.6))
        ax_box.set_title("Box Plot", fontsize=10, fontweight="bold")
        ax_box.set_ylabel("Grade")
        ax_box.set_xticks([])

        ax_interp = fig.add_subplot(gs[3, :])
        ax_interp.axis("off")
        ax_interp.text(0, 1.0, "Interpretation", fontsize=11, fontweight="bold",
                       color="#1e3a5f", va="top")
        justified_text = justify_text(self.interp_var.get(), width=95)
        ax_interp.text(0, 0.8, justified_text, fontsize=8.5, va="top",
                       ha="left", fontfamily="monospace", linespacing=1.6)

        with PdfPages(path) as pdf:
            pdf.savefig(fig)
        plt.close(fig)


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = StatsDashboard()
    app.mainloop()
