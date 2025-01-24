# Software Carbon Intensity (SCI) Calculation Tool

Welcome to the **Software Carbon Intensity (SCI) Calculation Tool**! This simple command-line program estimates the carbon footprint of your software by calculating its **SCI score**, a metric reflecting the greenhouse gas emissions (in grams of CO₂) per functional unit of your software’s output.

## Table of Contents

1.  [What is SCI?](#what-is-sci)
2.  [Overview of Our Approach](#overview-of-our-approach)
3.  [How It Works](#how-it-works)
4.  [Requirements](#requirements)
5.  [How to Use](#how-to-use)
6.  [Detailed Steps](#detailed-steps)
    -   [1) CPU Energy (E)](#1-cpu-energy-e)
    -   [2) Carbon Intensity (I)](#2-carbon-intensity-i)
    -   [3) Hardware Carbon (M)](#3-hardware-carbon-m)
    -   [4) Result Metric (R)](#4-result-metric-r)
    -   [5) SCI Formula](#5-sci-formula)
7.  [Interpreting the Log File](#interpreting-the-log-file)
8.  [Limitations & Disclaimer](#limitations--disclaimer)
9.  [Further Improvements](#further-improvements)

----------

## What is SCI?

**Software Carbon Intensity (SCI)** is a methodology proposed by the Green Software Foundation. The goal is to quantify how much greenhouse gas emissions your software generates **per unit of work** it performs. By having a numeric indicator, you can track, compare, and optimize the carbon footprint of your software over time.

The general formula is:

SCI=(E×I)+MR\text{SCI} = \frac{(E \times I) + M}{R}SCI=R(E×I)+M​

where:

-   E = Energy consumed (kWh)
-   I= Carbon intensity of the energy (gCO₂/kWh)
-   M = Hardware (embodied) carbon emissions (gCO₂)
-   R = Result metric (e.g., number of requests, number of tasks, etc.)

----------

## Overview of Our Approach

We use a **simplified method** to calculate the SCI in this tool:

1.  **Estimate CPU Energy Usage (E)** by monitoring CPU utilization and multiplying by a “nominal power” (TPW/RPW/TDP) over a chosen duration.
2.  **Determine Carbon Intensity (I)** by either asking for the user’s country and using an approximate value, or defaulting to a generic average.
3.  **Compute Hardware Carbon (M)** by simply doing M=E×IM = E \times IM=E×I. This follows a suggestion that hardware footprint can be represented by the same “energy multiplied by intensity” approach. (In reality, embodied carbon is more complex, but we keep it simple here.)
4.  **Ask for a Result Metric (R)** such as the number of transactions or requests handled.
5.  **Calculate the SCI** as (E×I)+MR\frac{(E \times I) + M}{R}R(E×I)+M​.

Finally, we **log** these details (time of measurement, inputs, and final SCI) to a `.log` file.

----------

## How It Works

1.  The script **prompts** for input:
    
    -   CPU nominal power (e.g., TDP in Watts)
    -   Duration of the software run (in seconds)
    -   Location (country code) to pick an approximate grid carbon intensity (gCO₂/kWh)
    -   How many requests or results were handled (the denominator RRR)
2.  The script **measures** CPU usage in real time (using the [psutil](https://pypi.org/project/psutil/) Python library) and calculates the estimated CPU energy consumption in kWh.
    
3.  The script **calculates**:
    
    -   **I**: carbon intensity for the region.
    -   **M**: hardware carbon, estimated as E×IE \times IE×I.
4.  It then **computes** the SCI = (E×I)+MR\frac{(E \times I) + M}{R}R(E×I)+M​.
    
5.  It **writes** these results (including the SCI score) to `sci_score.log`.
    

----------

## Requirements

-   **Python 3.x**
-   **psutil** library installed.
    -   Installation:
        
        bash
        
        Copier
        
        `pip install psutil` 
        
-   A terminal or command prompt to run the script.

----------

## How to Use

1.  **Clone or download** this repository (or just save the `main.py` file  in the folder sci ).
    
2.  **Install psutil** if not already installed.
    
3.  **Run the script** from your terminal:
    
    bash
    
    Copier
    
    `python main.py` 
    
4.  **Answer the prompts**:
    
    -   CPU nominal power (Watts), e.g. `65`
    -   Duration (in seconds), e.g. `10`
    -   Country code, e.g. `DE` for Germany
    -   Number of results (e.g., `1000` requests)
5.  **Check the output** displayed in the terminal. The SCI score will be printed at the end.
    
6.  **Open** the `sci_score.log` file (created or appended each time you run the script) to see a detailed record of inputs and the final SCI score.
    

----------

## Detailed Steps

### 1) CPU Energy (E)

We do not have direct access to hardware counters like Intel RAPL in this script, so we **estimate** the CPU energy usage by:

1.  Monitoring CPU usage (in %) each second over a given duration.
2.  Assuming the CPU consumes power proportional to its nominal power rating (TPW/RPW/TDP) times the observed usage fraction.
3.  Multiplying by the measurement time (in hours) gives total Wh, then converting to kWh.

For example, if your CPU is nominally **65 W**, and it’s used at **50%** for **10 seconds**:

-   Approx. power = 65 W ×\times× 0.5 = **32.5 W**
-   Time = 10 seconds = 10/3600 hours = 0.00278 h
-   Energy = 32.5 W ×\times× 0.00278 h ≈0.0904Wh\approx 0.0904 Wh≈0.0904Wh = 0.0000904 kWh

### 2) Carbon Intensity (I)

We choose a **carbon intensity** in **gCO₂/kWh** by:

-   Asking the user for the country code.
-   Looking up a predefined average (e.g., 300 for Germany, 60 for France, etc.).
-   If no match, we use a default of 300 gCO₂/kWh.

You could improve accuracy by calling an external API like [Electricity Maps](https://www.electricitymaps.com/), which provides near-real-time grid intensities.

### 3) Hardware Carbon (M)

In reality, **embodied carbon** or **hardware carbon** is a complex topic. It often involves dividing the total carbon footprint of the machine’s manufacturing over its usable lifetime. Here, however, we **simplify** and define MMM as:

M=E×I M = E \times IM=E×I

meaning we assume the hardware’s share of carbon is essentially the same as the operational energy usage. This is a **placeholder** approach.

### 4) Result Metric (R)

Finally, we ask the user for **RRR**, a count of the “units of service” the software provided (e.g., how many requests, tasks, or transactions happened during the measured period). This helps us express emissions **per unit** of software outcome.

### 5) SCI Formula

Putting it all together:

SCI=(E×I)+MR \text{SCI} = \frac{(E \times I) + M}{R} SCI=R(E×I)+M​

Given our simplifications:

-   E in kWh
-   I in gCO₂/kWh
-   M in gCO₂
-   R is an integer count

The result is **SCI** in gCO₂ per result unit.

----------

## Interpreting the Log File

Each time you run the script, it appends to `sci_score.log`:

-   **Timestamp**
-   **CPU Nominal Power**
-   **Measurement Duration**
-   **Country Code** and **Grid Intensity**
-   **Estimated CPU Energy** (kWh)
-   **Hardware Carbon** (gCO₂)
-   **Result Metric** (R)
-   **SCI Score** (gCO₂/unit)

You’ll see multiple runs stacked one after another. This helps keep track of your measurements over time.

----------

## Limitations & Disclaimer

-   This tool provides **approximations**. Real hardware power usage can vary beyond the nominal TDP/TPW. CPU turbo modes, thermal conditions, and other components (RAM, GPU, etc.) can affect actual consumption.
-   The hardware carbon is simplified as E×IE \times IE×I, whereas real embodied carbon should be considered over the product’s entire lifecycle.
-   The carbon intensities provided are just **typical averages** and can be much higher or lower depending on the time of day, region, and energy mix.
-   This method is still useful to get a **rough sense** of your software’s carbon footprint and track improvements over time.

----------

## Further Improvements

1.  **Use Real-time Carbon Data**
    
    -   Integrate an API call to [Electricity Maps](https://www.electricitymaps.com/) to get the actual gCO₂/kWh for the user’s location.
2.  **Include More Hardware**
    
    -   Estimate or measure GPU, RAM, or network energy consumption if relevant.
3.  **Refine M**
    
    -   Calculate actual **embodied carbon**: gather info about the hardware’s lifecycle emissions (LCA) and distribute it over the total hours or usage.
4.  **Automate Data Collection**
    
    -   You could run the script regularly (e.g., via cron) and track changes in a database or dashboard.
5.  **Integration**
    
    -   Integrate with CI/CD pipelines to evaluate software carbon intensity upon each build or deployment.