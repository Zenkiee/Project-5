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
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(grades, bins=20, color="steelblue", edgecolor="white")
axes[0].axvline(np.mean(grades), color="red", linestyle="--",
label=f"Mean={np.mean(grades):.1f}")
axes[0].axvline(np.median(grades), color="green", linestyle="--",
label=f"Median={np.median(grades):.1f}")
axes[0].legend(); axes[0].set_title("Grade Distribution")
axes[1].boxplot(grades, vert=True, patch_artist=True,
boxprops=dict(facecolor="steelblue", alpha=0.5))
axes[1].set_title("Box Plot of Grades")
plt.tight_layout(); plt.show()