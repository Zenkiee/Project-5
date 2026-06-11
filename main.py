import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Generate synthetic student grades
np.random.seed(42)
grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)
df = pd.DataFrame({"Grade": grades})

# Descriptive stats
print(df.describe().round(2))
print(f"Skewness : {stats.skew(grades):.4f}")
print(f"Kurtosis : {stats.kurtosis(grades):.4f}")

# Summary statistics table
summary = pd.DataFrame({
    "Statistic": [
        "Minimum",
        "Maximum",
        "Mean",
        "Median",
        "Mode",
        "Variance",
        "Standard Deviation",
        "Skewness"
    ],
    "Value": [
        np.min(grades),
        np.max(grades),
        np.mean(grades),
        np.median(grades),
        stats.mode(grades, keepdims=True).mode[0],
        np.var(grades),
        np.std(grades),
        stats.skew(grades)
    ]
})

summary["Value"] = summary["Value"].round(2)

# Dashboard layout
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Histogram
axes[0].hist(grades, bins=20, color="steelblue", edgecolor="white")

axes[0].axvline(
    np.mean(grades),
    color="red",
    linestyle="--",
    label=f"Mean={np.mean(grades):.1f}"
)

axes[0].axvline(
    np.median(grades),
    color="green",
    linestyle="--",
    label=f"Median={np.median(grades):.1f}"
)

axes[0].legend()
axes[0].set_title("Grade Distribution")
axes[0].set_xlabel("Grade")
axes[0].set_ylabel("Frequency")

# Box plot
axes[1].boxplot(
    grades,
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.5)
)

axes[1].set_title("Box Plot of Grades")
axes[1].set_ylabel("Grade")

# Summary table
axes[2].axis("off")
axes[2].set_title("Summary Statistics Table")

table = axes[2].table(
    cellText=summary.values,
    colLabels=summary.columns,
    cellLoc="center",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

plt.tight_layout()
plt.show()