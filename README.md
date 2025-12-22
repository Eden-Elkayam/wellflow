# wellflow

A Python package for processing plate reader growth data and estimating microbial growth rates.

`wellflow` provides a reproducible pipeline for:
- converting plate reader exports into tidy data
- blank correction and smoothing
- growth rate estimation via rolling log-linear regression
- extracting maximum growth rates per well or experimental condition

The package is designed for day-to-day experimental analysis in microbiology labs and prioritizes clarity, transparency, and reproducibility.

---

## Installation

### From GitHub (recommended)

```bash
pip install git+https://github.com/flamholz-lab/wellflow.git
```

### Editable install (for development)

```bash
git clone https://github.com/<Flamholz-Lab>/wellflow.git
cd wellflow
pip install -e .
```

---

## Requirements

* Python ≥ 3.10
* pandas
* numpy
* openpyxl

## Basic usage

### 1. Load plate reader measurements

```python
from wellflow import read_plate_measurements

df = read_plate_measurements(
    path="plate_reader_output.xlsx",
    header_row=2,
    last_row=150,
    start_col="C"
)

```
This returns a tidy dataframe with one row per (time, well) and a time_hours column.

### 2. Add experimental design metadata

```python
from wellflow import parse_plate_design, merge_measurements_and_conditions

design = parse_plate_design("plate_design.xlsx")
df = merge_measurements_and_conditions(df, design)
```

### 3. Blank correction and smoothing

```python
from wellflow import add_blank_value, add_smoothed_od

df = add_blank_value(df, window=4)
df = add_smoothed_od(df, window=5)
```

### 4. Growth rate estimation

```python
from wellflow import add_growth_rate, add_max_growth_rate

df = add_growth_rate(df, window=5)
df = add_max_growth_rate(df)
```

This adds:
* mu: instantaneous growth rate estimated from log-linear regression
* mu_max: maximum growth rate per well or condition
* t_at_mu_max: time at which maximum growth rate occurs










