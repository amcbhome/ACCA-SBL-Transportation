# ACCA SBL Transportation Optimizer (PuLP & Streamlit)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://github.com/amcbhome/ACCA-SBL-Transportation)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository demonstrates how to modernize traditional accounting and operational research models by transitioning **spreadsheet-based linear programming (Excel Solver)** into a dynamic, production-ready **Python (`PuLP`) optimization engine**.

Modeled around classic **ACCA Management Accounting (PM/APM)** and **Strategic Business Leader (SBL)** big data directives, this interactive Streamlit application solves multi-depot transportation matrices to minimize global freight expenditure while satisfying warehouse supply capacities and regional distribution hub demands.

---

## Strategic Value: Why Transition from Spreadsheets to Python?

While corporate finance and operational teams traditionally rely on Excel Solver for linear programming, scaling these models in modern FMCG and logistics environments presents clear limitations:

| Capability | Traditional Spreadsheet (Excel Solver) | Python Optimization (`PuLP` & Streamlit) |
| :--- | :--- | :--- |
| **Model Scale** | Limited to 200 decision variables without costly add-ins | Unlimited nodes, routes, and SKU constraints |
| **Data Ingestion** | Manual copy-pasting or fragile VBA macros | Direct integration with SQL databases & ERP pipelines |
| **Audit & Governance** | High risk of hidden cell/formula errors | Version-controlled, testable code via GitHub |
| **Stakeholder UX** | Static workbook files | Interactive web app deployed for executive scenarios |

---

## Features & Implementation Details

* **Dynamic Network Setup:** Adjust warehouse supply capacities, hub demands, and unit freight costs ($c_{ij}$) in real time.
* **Mathematical Optimization Engine:** Uses standard Continuous Linear Programming via `PuLP` and the CBC solver engine to compute exact minimal cost configurations.
* **Executive Visualization:** Auto-generates optimal dispatch schedules alongside dynamic route volume allocation charts using Streamlit.
* **Feasibility Auditing:** Built-in error handling alerts users to infeasible optimization states (e.g., global demand exceeding available supply).

---

## Technical Architecture & Mathematical Formulation

### Objective Function
Minimize total freight cost $Z$:

$$Z = \sum_{i \in S} \sum_{j \in D} c_{ij} \cdot x_{ij}$$

Where:
* $S$: Set of origin warehouses / manufacturing facilities
* $D$: Set of destination hubs / retail distribution nodes
* $c_{ij}$: Unit transport cost from origin $i$ to destination $j$
* $x_{ij}$: Continuous decision variable representing shipment volume from $i$ to $j$

### Subject to Constraints:
1. **Supply Limits:** $\sum_{j \in D} x_{ij} \le S_i \quad \forall i \in S$
2. **Demand Requirements:** $\sum_{i \in S} x_{ij} \ge D_j \quad \forall j \in D$
3. **Non-negativity:** $x_{ij} \ge 0 \quad \forall i \in S, j \in D$

---

## Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed.

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/amcbhome/ACCA-SBL-Transportation.git](https://github.com/amcbhome/ACCA-SBL-Transportation.git)
   cd ACCA-SBL-Transportation
