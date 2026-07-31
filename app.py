import streamlit as st
import pandas as pd
import pulp

# Page Configuration
st.set_page_config(
    page_title="ACCA SBL Transportation Optimizer",
    page_icon="🚚",
    layout="wide"
)

# Top Bar Header with Portfolio & CV Link
st.title("🚚 Prescriptive Supply Chain Transportation Optimizer")
st.markdown("""
**ACCA Technical Framework Alignment (PM / APM / SBL)**  
*This app updates the traditional spreadsheet solution (Excel Solver) to Python.*  
Developed by **Alastair McBride** | [View Project Repository & CV on GitHub](https://github.com/amcbhome/ACCA-SBL-Transportation)
""")

st.divider()

# --- SIDEBAR: INPUT CONTROL PANEL ---
st.sidebar.header("⚙️ Network Parameters")

# Default Nodes
warehouses = ["Warehouse A", "Warehouse B", "Warehouse C"]
hubs = ["Hub North", "Hub Central", "Hub South", "Hub East"]

# Capacity Inputs
st.sidebar.subheader("1. Warehouse Capacities")
supply = {}
for w in warehouses:
    default_val = 500 if w == "Warehouse A" else (700 if w == "Warehouse B" else 400)
    supply[w] = st.sidebar.number_input(f"{w} Supply", min_value=0, value=default_val, step=50)

# Demand Inputs
st.sidebar.subheader("2. Hub Demand")
demand = {}
default_demands = [300, 450, 500, 350]
for idx, h in enumerate(hubs):
    demand[h] = st.sidebar.number_input(f"{h} Demand", min_value=0, value=default_demands[idx], step=50)

# Total Network Sanity Check
total_supply = sum(supply.values())
total_demand = sum(demand.values())

# --- MAIN CONTENT: COST MATRIX CONFIGURATION ---
st.subheader("📊 Unit Shipping Cost Matrix (£ per unit)")

# Setup DataFrame with Warehouse as a explicit data column to prevent Python 3.14 Index TypeErrors
cost_data = [
    {"Warehouse": "Warehouse A", "Hub North": 4.5, "Hub Central": 6.0, "Hub South": 8.0, "Hub East": 5.0},
    {"Warehouse": "Warehouse B", "Hub North": 7.0, "Hub Central": 4.0, "Hub South": 5.5, "Hub East": 6.5},
    {"Warehouse": "Warehouse C", "Hub North": 8.0, "Hub Central": 5.0, "Hub South": 3.5, "Hub East": 4.0},
]
cost_df = pd.DataFrame(cost_data)

edited_cost_df = st.data_editor(
    cost_df,
    use_container_width=True,
    num_rows="fixed",
    disabled=["Warehouse"],
    help="Edit unit freight costs directly in the grid."
)

# Convert edited DataFrame back to operational dictionary format
costs = {}
for _, row in edited_cost_df.iterrows():
    w_name = row["Warehouse"]
    costs[w_name] = {h: float(row[h]) for h in hubs}

# --- PULP OPTIMIZATION ENGINE ---
model = pulp.LpProblem("Supply_Chain_Freight_Minimization", pulp.LpMinimize)

# Decision Variables
routes = [(i, j) for i in warehouses for j in hubs]
x = pulp.LpVariable.dicts("Ship_Units", (warehouses, hubs), lowBound=0, cat="Continuous")

# Objective Function
model += pulp.lpSum([x[i][j] * costs[i][j] for (i, j) in routes]), "Total_Freight_Cost"

# Constraints
for i in warehouses:
    model += (pulp.lpSum([x[i][j] for j in hubs]) <= supply[i], f"Supply_{i}")

for j in hubs:
    model += (pulp.lpSum([x[i][j] for i in warehouses]) >= demand[j], f"Demand_{j}")

# Solve
model.solve(pulp.PULP_CBC_CMD(msg=False))
status = pulp.LpStatus[model.status]

# --- RESULTS DASHBOARD ---
st.divider()

if status != "Optimal" or total_supply < total_demand:
    st.error(f"⚠️ **Infeasible Optimization State**: Total Supply ({total_supply:,} units) is less than Total Demand ({total_demand:,} units), or dynamic constraints cannot be satisfied.")
else:
    total_cost = pulp.value(model.objective)

    # Key Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Optimization Status", status)
    col2.metric("Minimized Cost", f"£{total_cost:,.2f}")
    col3.metric("Total Supply Capacity", f"{total_supply:,} units")
    col4.metric("Total Regional Demand", f"{total_demand:,} units")

    # Extract Results into Matrix
    results_data = []
    for i in warehouses:
        row = {}
        for j in hubs:
            val = x[i][j].varValue
            row[j] = val if val > 0 else 0
        results_data.append(row)

    results_df = pd.DataFrame(results_data, index=warehouses)

    # Output Visualizations & Tables
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("📋 Optimal Dispatch Schedule (Units)")
        st.dataframe(results_df.style.highlight_between(left=1, color="#d1e7dd"), use_container_width=True)

    with right_col:
        st.subheader("📈 Route Volume Allocation")
        chart_df = results_df.reset_index().melt(id_vars="index", var_name="Destination Hub", value_name="Units Shipped")
        chart_df.rename(columns={"index": "Origin Warehouse"}, inplace=True)
        
        st.bar_chart(
            chart_df,
            x="Destination Hub",
            y="Units Shipped",
            color="Origin Warehouse",
            stack=False
        )

# --- BENEFITS OF UPDATING FROM SPREADSHEET TO PYTHON ---
st.divider()
st.subheader("💡 Strategic Benefits: Transitioning from Excel Solver to Python (`PuLP`)")

st.markdown("""
While classic accounting curricula (ACCA PM/APM) teach linear programming using manual matrix steps or Excel's Solver plugin, migrating these models to Python provides distinct commercial advantages:

1. **Overcoming Constraint & Cell Limits:** Standard Excel Solver restricts models to 200 decision variables without expensive third-party add-ins. Python's `PuLP` interface handles thousands of supply nodes, routes, and SKU constraints seamlessly.
2. **Automated Pipeline Integration:** Instead of manual spreadsheet copy-pasting, Python scripts pull live stock levels and demand forecasts straight from SQL databases or ERP systems, solve the model, and write optimal routes back to operational databases.
3. **Auditability & Reduced Cell Error:** Formula errors in hidden spreadsheet cells can obscure misallocations. Python code isolates logic, parameters, and constraints into clear, version-controlled scripts (Git/GitHub) that are easy to test and verify.
4. **Interactive Executive Dashboards:** Deploying with frameworks like Streamlit transforms static financial calculations into dynamic web apps that commercial management can test in real time.
""")
