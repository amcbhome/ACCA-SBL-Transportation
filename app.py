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

# Mileage Freight Rate Configuration
st.sidebar.subheader("1. Freight Rate Parameter")
rate_per_mile = st.sidebar.number_input(
    "Freight Rate (£ / TV / Mile)",
    min_value=0.0,
    value=5.00,
    step=0.50,
    help="Rate per unit per mile shipped"
)

# Capacity Inputs (Units)
st.sidebar.subheader("2. Warehouse Capacities (Units)")
supply = {
    "Warehouse A": st.sidebar.number_input("Warehouse A Supply", min_value=0, value=500, step=50),
    "Warehouse B": st.sidebar.number_input("Warehouse B Supply", min_value=0, value=700, step=50),
    "Warehouse C": st.sidebar.number_input("Warehouse C Supply", min_value=0, value=400, step=50)
}

# Demand Inputs (Units)
st.sidebar.subheader("3. Hub Demand (Units)")
demand = {
    "Hub North": st.sidebar.number_input("Hub North Demand", min_value=0, value=300, step=50),
    "Hub Central": st.sidebar.number_input("Hub Central Demand", min_value=0, value=450, step=50),
    "Hub South": st.sidebar.number_input("Hub South Demand", min_value=0, value=500, step=50),
    "Hub East": st.sidebar.number_input("Hub East Demand", min_value=0, value=350, step=50)
}

# Total Network Sanity Check
total_supply = sum(supply.values())
total_demand = sum(demand.values())

# --- MAIN CONTENT: ROUTE DISTANCE MATRIX CONFIGURATION ---
st.subheader("📏 Route Distance Matrix (Miles)")
st.caption(f"Freight cost per route is dynamically calculated as: **Distance (Miles) × £{rate_per_mile:.2f}/TV/Mile**")

# Default Distance Matrix (Miles) tailored to £812,500 target baseline solution
default_distances = {
    "Warehouse A": {"Hub North": 100.0, "Hub Central": 150.0, "Hub South": 300.0, "Hub East": 120.0},
    "Warehouse B": {"Hub North": 220.0, "Hub Central": 110.0, "Hub South": 180.0, "Hub East": 200.0},
    "Warehouse C": {"Hub North": 280.0, "Hub Central": 160.0, "Hub South": 90.0,  "Hub East": 130.0},
}

# Render Interactive Distance Input Grid in Columns
distances = {w: {} for w in warehouses}

for w in warehouses:
    st.markdown(f"**{w}**")
    cols = st.columns(len(hubs))
    for idx, h in enumerate(hubs):
        with cols[idx]:
            distances[w][h] = st.number_input(
                label=f"➔ {h} (Miles)",
                min_value=0.0,
                value=float(default_distances[w][h]),
                step=10.0,
                key=f"dist_{w}_{h}"
            )

# Compute Unit Costs: Cost (£/unit) = Distance (Miles) * Rate (£/unit/mile)
costs = {
    w: {h: distances[w][h] * rate_per_mile for h in hubs}
    for w in warehouses
}

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

# Solve Model
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
        st.subheader("📋 Optimal Dispatch Schedule (TV Units)")
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
2. **Dynamic Mileage Parameterization:** Decoupling route mileage from variable transport rates (£5/TV/mile) allows finance teams to run sensitivity analyses on fuel inflation and carrier negotiations in real time.
3. **Automated Pipeline Integration:** Instead of manual spreadsheet copy-pasting, Python scripts pull live stock levels and demand forecasts straight from SQL databases or ERP systems, solve the model, and write optimal routes back to operational databases.
4. **Interactive Executive Dashboards:** Deploying with frameworks like Streamlit transforms static financial calculations into dynamic web apps that commercial management can test in real time.
""")
