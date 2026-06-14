import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# =====================================================
# Group 05 - Basic Descriptive Statistics Dashboard
# Topic: Statistics
# Dataset: Synthetic Student Grades
# =====================================================


# -----------------------------
# 1. Data Generation / Loading
# -----------------------------
np.random.seed(42)

grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)

df = pd.DataFrame({
    "Grade": grades
})


# -----------------------------
# 2. Descriptive Statistics
# -----------------------------
rounded_grades = np.round(grades)

minimum = np.min(grades)
maximum = np.max(grades)
mean = np.mean(grades)
median = np.median(grades)
mode = stats.mode(rounded_grades, keepdims=True).mode[0]
variance = np.var(grades)
standard_deviation = np.std(grades)
data_range = maximum - minimum
skewness = stats.skew(grades)
kurtosis = stats.kurtosis(grades)

q1 = np.percentile(grades, 25)
q2 = np.percentile(grades, 50)
q3 = np.percentile(grades, 75)
iqr = q3 - q1


# -----------------------------
# 3. Print Results Clearly
# -----------------------------
print("\nGROUP 05 BASIC DESCRIPTIVE STATISTICS DASHBOARD")
print("=" * 55)
print("\nDataset Preview:")
print(df.head())

print("\nDescriptive Statistics:")
print(df.describe().round(2))

print("\nAdditional Statistics:")
print(f"Mode                : {mode:.0f}")
print(f"Variance            : {variance:.2f}")
print(f"Standard Deviation  : {standard_deviation:.2f}")
print(f"Range               : {data_range:.2f}")
print(f"Skewness            : {skewness:.4f}")
print(f"Kurtosis            : {kurtosis:.4f}")
print(f"Q1                  : {q1:.2f}")
print(f"Median / Q2         : {q2:.2f}")
print(f"Q3                  : {q3:.2f}")
print(f"IQR                 : {iqr:.2f}")


# -----------------------------
# 4. Summary Statistics Table
# -----------------------------
summary = pd.DataFrame({
    "Statistic": [
        "Minimum",
        "Maximum",
        "Mean",
        "Median",
        "Mode",
        "Variance",
        "Standard Deviation",
        "Range",
        "Skewness",
        "Kurtosis",
        "Q1",
        "Q3",
        "IQR"
    ],
    "Value": [
        minimum,
        maximum,
        mean,
        median,
        mode,
        variance,
        standard_deviation,
        data_range,
        skewness,
        kurtosis,
        q1,
        q3,
        iqr
    ]
})

summary["Value"] = summary["Value"].round(2)


# -----------------------------
# 5. Dashboard Layout
# -----------------------------
fig, axes = plt.subplots(2, 2, figsize=(15, 9))

fig.suptitle(
    "Group 05 Basic Descriptive Statistics Dashboard",
    fontsize=18,
    fontweight="bold"
)


# -----------------------------
# Histogram with Mean and Median Overlays
# -----------------------------
axes[0, 0].hist(
    grades,
    bins=20,
    color="steelblue",
    edgecolor="white"
)

axes[0, 0].axvline(
    mean,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean = {mean:.2f}"
)

axes[0, 0].axvline(
    median,
    color="green",
    linestyle="--",
    linewidth=2,
    label=f"Median = {median:.2f}"
)

axes[0, 0].set_title("Grade Distribution")
axes[0, 0].set_xlabel("Grade")
axes[0, 0].set_ylabel("Frequency")
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)


# -----------------------------
# Box Plot
# -----------------------------
axes[0, 1].boxplot(
    grades,
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.6),
    medianprops=dict(color="red", linewidth=2),
    whiskerprops=dict(linewidth=1.5),
    capprops=dict(linewidth=1.5),
    flierprops=dict(marker="o", markerfacecolor="orange", markersize=6)
)

axes[0, 1].set_title("Box Plot of Grades")
axes[0, 1].set_ylabel("Grade")
axes[0, 1].grid(alpha=0.3)

box_text = f"""
Q1 = {q1:.2f}
Median = {median:.2f}
Q3 = {q3:.2f}
IQR = {iqr:.2f}
"""

axes[0, 1].text(
    1.15,
    median,
    box_text,
    fontsize=10,
    verticalalignment="center"
)


# -----------------------------
# Summary Statistics Table
# -----------------------------
axes[1, 0].axis("off")
axes[1, 0].set_title("Summary Statistics Table")

table = axes[1, 0].table(
    cellText=summary.values,
    colLabels=summary.columns,
    cellLoc="center",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.35)


# -----------------------------
# Interpretation
# -----------------------------
axes[1, 1].axis("off")
axes[1, 1].set_title("Interpretation of Results")

if skewness < 0:
    skew_text = "The data is slightly left-skewed."
elif skewness > 0:
    skew_text = "The data is slightly right-skewed."
else:
    skew_text = "The data is approximately symmetrical."

interpretation = f"""
The dataset contains 100 synthetic student grades.

The mean grade is {mean:.2f}, while the median is {median:.2f}.
This means that most student grades are centered around the mid-70s.

The minimum grade is {minimum:.2f}, and the maximum grade is {maximum:.2f}.
The range is {data_range:.2f}, which shows the difference between
the highest and lowest grades.

The standard deviation is {standard_deviation:.2f}.
This means the grades have a moderate spread around the average.

The skewness is {skewness:.2f}.
{skew_text}

The box plot shows the quartiles, median, whiskers, and possible outliers.
Overall, the student grades are mostly clustered near the average.
"""

axes[1, 1].text(
    0.05,
    0.5,
    interpretation,
    fontsize=11,
    verticalalignment="center"
)


# -----------------------------
# Show Dashboard
# -----------------------------
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()