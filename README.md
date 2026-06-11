# Project 05: Basic Descriptive Statistics Dashboard

## Topic

Statistics

## Level

Beginner

## Libraries Used

* NumPy
* Pandas
* Matplotlib

## Project Description

This project computes and visualizes core descriptive statistics for a dataset, such as student grades. It includes measures of central tendency, measures of spread, and visual charts to help understand the distribution of the data.

The program can either load a CSV dataset or generate synthetic student grade data. It then calculates key statistics and displays them in a simple dashboard.

## Core Concept

Descriptive statistics summarize and describe the main features of a dataset.

Measures of central tendency tell us about the center of the data:

* Mean
* Median
* Mode

Measures of spread tell us about the variability of the data:

* Variance
* Standard deviation
* Range

Skewness shows whether the data is symmetrical or leaning more to the left or right.

## Learning Objective

The objective of this project is to load a CSV dataset or generate synthetic data, compute key descriptive statistics, and present the results using a dashboard.

The dashboard includes:

* Histogram
* Box plot
* Summary statistics table

## Expected Outputs

The program should produce the following outputs:

1. **Histogram with Mean and Median Lines**

   * Shows the grade distribution
   * Includes mean and median overlays

2. **Box Plot**

   * Shows quartiles
   * Shows outliers
   * Shows the spread of the data

3. **Summary Statistics Table**

   * Minimum
   * Maximum
   * Mean
   * Median
   * Standard deviation
   * Skewness

## How to Run the Program

### 1. Install the Required Libraries

Run this command in the terminal:

```bash
pip install numpy pandas matplotlib scipy
```

### 2. Run the Python File

Run this command:

```bash
python main.py
```

or:

```bash
py main.py
```

## Files

* `main.py` - Main Python program for generating the dashboard
* `README.md` - Project description and instructions

## Sample Dataset

This project uses synthetic student grades generated with NumPy. A random seed is used so the results can be reproduced every time the program runs.

## Dashboard Features

* Generates student grade data
* Computes descriptive statistics
* Displays a histogram with mean and median lines
* Displays a box plot for quartiles, outliers, and spread
* Displays a summary statistics table
* Provides a simple interpretation of the results
  ::: 
