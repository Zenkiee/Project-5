# Project 05: Basic Descriptive Statistics Dashboard

A beginner-friendly Python desktop application that generates or loads numerical data, calculates descriptive statistics, and presents the results through an interactive dashboard.

## Project Information

- **Topic:** Statistics
- **Level:** Beginner
- **Programming Language:** Python
- **Interface:** Tkinter desktop GUI

## Project Description

The Basic Descriptive Statistics Dashboard helps users understand the main characteristics of a numerical dataset.

When the program starts, it automatically generates a sample dataset containing 100 student grades. Users can also generate a new random sample or load their own CSV file. The program then calculates descriptive statistics and displays a histogram, box plot, and summary statistics table.

## Core Concept

Descriptive statistics summarize and describe the important features of a dataset.

### Measures of Central Tendency

These values describe the center of the data:

- **Mean** – the arithmetic average
- **Median** – the middle value after sorting the data
- **Mode** – the most frequently occurring value

### Measures of Spread

These values describe how widely the data is distributed:

- **Minimum and Maximum** – the lowest and highest values
- **Range** – the difference between the maximum and minimum
- **Variance** – the average squared distance from the mean
- **Standard Deviation** – the typical distance of values from the mean
- **Interquartile Range (IQR)** – the spread of the middle 50% of the data

### Distribution Shape

- **Skewness** – indicates whether the distribution leans to the left or right
- **Kurtosis** – describes how heavy the tails of the distribution are compared with a normal distribution

## Learning Objectives

This project demonstrates how to:

- Generate synthetic numerical data using NumPy
- Load numerical data from a CSV file using Pandas
- Calculate descriptive statistics using NumPy and SciPy
- Create a graphical desktop interface using Tkinter
- Embed Matplotlib charts inside a Tkinter window
- Present statistical results in a table, histogram, and box plot
- Handle invalid CSV files and missing values

## Dashboard Features

- Automatically generates 100 sample student grades at startup
- Generates a new random sample through the **New Sample** button
- Loads a user-selected CSV file through the **Load CSV** button
- Detects numeric columns in a CSV file
- Lets the user select a column when multiple numeric columns are available
- Removes empty values before processing CSV data
- Displays a status bar showing the active data source and sample size
- Updates all statistics and charts whenever the dataset changes

## Statistics Calculated

The summary table displays:

- Count
- Minimum
- Maximum
- Mean
- Median
- Mode
- Sample standard deviation
- Sample variance
- Skewness
- Kurtosis
- First quartile (Q1)
- Third quartile (Q3)
- Interquartile range (IQR)

## Visualizations

### Histogram

The histogram shows the frequency distribution of the grades. Dashed vertical lines indicate the calculated mean and median.

### Box Plot

The box plot shows:

- First quartile (Q1)
- Median
- Third quartile (Q3)
- Interquartile range
- Whiskers
- Possible outliers

Quartile values are also displayed beside the box plot.

## Libraries Used

- **Tkinter** – creates the graphical user interface
- **NumPy** – generates sample data and performs numerical calculations
- **Pandas** – reads and processes CSV files
- **Matplotlib** – creates the histogram and box plot
- **SciPy** – calculates the mode, skewness, and kurtosis

## Project Structure

```text
Project 5/
├── main.py       # Main Python program
└── README.md     # Project documentation
```

## Installation

Make sure Python 3 is installed on your computer.

Install the required external libraries by running:

```bash
pip install numpy pandas matplotlib scipy
```

Tkinter is normally included with standard Python installations on Windows and macOS.

On some Linux distributions, it may need to be installed separately:

```bash
sudo apt install python3-tk
```

## How to Run

Open a terminal inside the project folder and run:

```bash
python main.py
```

On Windows, this command may also be used:

```bash
py main.py
```

## Using the Program

1. Run `main.py`.
2. The dashboard opens with a reproducible sample of 100 grades.
3. Click **New Sample** to create a different random dataset.
4. Click **Load CSV** to select a CSV file.
5. When the CSV contains multiple numeric columns, select the column to analyze.
6. Review the updated table, histogram, and box plot.

## CSV File Requirements

The selected CSV file must contain at least one numeric column.

Example:

```csv
Student,Grade
Student 1,85
Student 2,78
Student 3,92
Student 4,74
Student 5,88
```

The program automatically ignores empty values in the selected numeric column. An error message is displayed when the CSV file has no numeric columns or cannot be read.

## Sample Data

The starting dataset is generated from a normal distribution with:

- Mean of approximately `75`
- Standard deviation of approximately `12`
- Sample size of `100`
- Values limited to the range `0–100`
- Random seed `42` for reproducible startup results

Clicking **New Sample** removes the fixed seed and generates a different dataset.

## Expected Output

After running the program, the dashboard displays:

1. A summary table containing the calculated statistics
2. A histogram with mean and median reference lines
3. A box plot showing quartiles, spread, and possible outliers
4. A status bar describing the current dataset

## Entry Point

The application starts through the following block in `main.py`:

```python
if __name__ == "__main__":
    app = StatsDashboard()
    app.mainloop()
```
