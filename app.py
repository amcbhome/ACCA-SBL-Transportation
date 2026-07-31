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

# Depots & Stores matching spreadsheet
depots = ["D1", "D2", "D3"]
stores = ["Store 1", "Store 2", "Store 3"]

# Freight Rate Parameter (£5 / TV / mile)
st.sidebar.subheader("1. Freight Rate Parameter")
rate_per_mile = st.sidebar.number_input(
    "Cost per TV per mile (£)",
    min_value=0.0,
    value=5.00,
    step=0.50,
    help="Delivery cost per TV per mile shipped"
)

# Depot Supply / Availability Inputs (Depot Capacities: D1=2500, D2=3100, D3=1250)
st.sidebar.subheader("2. Depot Supply (TVs Available)")
supply = {
    "D1": st.sidebar.number_input("D1 Supply", min_value=0, value=2500, step=100),
    "D2": st.sidebar.number_input("D2 Supply", min_value=0, value=3100, step=100),
    "D3": st.sidebar.number_input("D3 Supply", min_value=0, value=1250, step=100)
}

# Store Target Demand Inputs (Store 1=2000, Store 2=2850, Store 3=2000)
st.sidebar.subheader("3. Store Demand Target")
demand = {
    "Store 1": st.sidebar.number_input("Store 1 Demand", min_value=0, value=2000, step=100),
    "Store 2": st.sidebar.number_input("Store 2 Demand", min_value=0, value=2850, step=100),
    "Store 3": st.sidebar.number_input("Store 3 Demand", min_value=0, value=2000, step=100)
}

# Total Network Sanity Check
total_supply = sum(supply.values())
total_demand = sum(demand.values())

# --- MAIN CONTENT: ROUTE DISTANCE MATRIX ---
st.subheader("📏 Distances between Depots and Stores (Miles)")
st.caption(f"Freight cost per route is calculated as: **Distance (Miles) × £{rate_per_mile:.2f}/TV/Mile**")

# Exact Distance Matrix from Excel (C8:E10)
default_distances = {
    "D1": {"Store 1": 22.0, "Store 2": 33.0, "Store 3": 40.0},
    "D2": {"Store 1": 27.0, "Store 2": 30.0, "Store 3": 22.0},
    "D3": {"Store 1": 36.0, "Store 2": 20.0, "Store 3": 25.0},
}

# Interactive Distance Input Grid in Columns
distances = {d: {} for d in depots}

for d in depots:
    st.markdown(f"**{d}**")
    cols = st.columns(len(stores))
    for idx, s in enumerate(stores):
        with cols[idx]:
            distances[d][s] = st.number_input(
                label=f"➔ {s} (Miles)",
                min_value=0.0,
                value=float(default_distances[d][s]),
                step=1.0,
                key=f"dist_{d}_{s}"
            )

# Calculate Unit Cost (£/TV) = Distance * Rate
costs = {
    d: {s: distances[d][s] * rate_per_mile for s in stores}
    for d in depots
}

# --- PULP OPTIMIZATION ENGINE ---
model = pulp.LpProblem("TV_Transportation_Minimization", pulp.LpMinimize)

# Decision Variables: TVs Shipped from Depots to Stores
routes = [(i, j) for i in depots for j in stores]
x = pulp.LpVariable.dicts("Ship_TVs", (depots, stores), lowBound=0, cat="Continuous")

# Objective Function: Minimize total delivery cost (£)
model += pulp.lpSum([x[i][j] * costs[i][j] for (i, j) in routes]), "Total_Delivery_Cost"

# Supply Constraints: TVs transported <= TVs available at depot
supply_constraints = {}
for i in depots:
    c = (pulp.lpSum([x[i][j] for j in stores]) <= supply[i])
    model += c, f"Depot_Supply_{i}"
    supply_constraints[i] = c

# Store Demand Constraints: TVs received EQUALS required store demand
demand_constraints = {}
for j in stores:
    c = (pulp.lpSum([x[i][j] for i in depots]) == demand[j])
    model += c, f"Store_Demand_{j}"
    demand_constraints[j] = c

# Solve Model using CBC Simplex LP engine
model.solve(pulp.PULP_CBC_CMD(msg=False))
status = pulp.LpStatus[model.status]

# --- RESULTS DASHBOARD ---
st.divider()

if status != "Optimal" or total_supply < total_demand:
    st.error("⚠️ **Infeasible Optimization State**: Total demand exceeds total depot supply, or constraints cannot be satisfied.")
else:
    total_cost = pulp.value(model.objective)

    # Calculate aggregate metrics
    total_shipped = sum(x[i][j].varValue for i in depots for j in stores)
    total_distance_tv_miles = sum(x[i][j].varValue * distances[i][j] for i in depots for j in stores)

    # Key Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Optimization Status", status)
    col2.metric("Total Cost (£)", f"£{total_cost:,.2f}")
    col3.metric("Total TV/Miles", f"{total_distance_tv_miles:,.0f}")
    col4.metric("Total TVs Shipped", f"{total_shipped:,.0f}")

    # Extract Matrix Results
    results_data = []
    for i in depots:
        row = {}
        for j in stores:
            val = x[i][j].varValue
            row[j] = val if val > 0 else 0
        results_data.append(row)

    results_df = pd.DataFrame(results_data, index=depots)

    # Output Visualizations & Tables
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("📋 Optimal Dispatch Schedule (TVs)")
        st.dataframe(results_df.style.highlight_between(left=1, color="#d1e7dd"), use_container_width=True)

    with right_col:
        st.subheader("🔍 Constraint Slack & Resource Analysis")
        st.caption("Slack measures unused capacity in non-binding constraints.")

        # Calculate Slack per Depot Constraint
        slack_data = []
        for i in depots:
            shipped = sum(x[i][j].varValue for j in stores)
            available = supply[i]
            slack_val = available - shipped
            constraint_type = "Binding" if slack_val == 0 else "Non-Binding (Slack Available)"
            
            slack_data.append({
                "Depot": i,
                "Available": available,
                "Allocated": shipped,
                "Unallocated Slack": slack_val,
                "Constraint Status": constraint_type
            })

        slack_df = pd.DataFrame(slack_data)
        st.dataframe(slack_df, use_container_width=True, hide_index=True)

        total_unallocated = slack_df["Unallocated Slack"].sum()
        if total_unallocated > 0:
            st.info(f"💡 **Unallocated Resource Note:** Network contains **{total_unallocated:,.0f} unallocated TVs** across non-binding depots. This surplus capacity can be redirected to secondary demand regions or held to minimize holding costs.")
        else:
            st.warning("⚠️ **Fully Binding System:** All available depot inventory is exhausted. No slack remains.")

# --- STRATEGIC DISCUSSION: SLACK & UNALLOCATED RESOURCES ---
st.divider()
st.subheader("💡 Strategic Benefits: Transitioning from Excel Solver to Python (`PuLP`)")

st.markdown("""
While classic accounting curricula (ACCA PM/APM/SBL) teach linear programming using manual matrix steps or Excel's Solver plugin, migrating these models to Python provides distinct commercial advantages:

1. **Analytical Slack Management:** When constraints are **non-binding**, the solver identifies positive slack values. In supply chain governance, surplus depot capacity highlights idle inventory holding costs that management can reallocate to auxiliary sales channels.
2. **Overcoming Constraint & Cell Limits:** Standard Excel Solver restricts models to 200 decision variables without expensive third-party add-ins. Python's `PuLP` interface handles thousands of supply nodes, routes, and SKU constraints seamlessly.
3. **Auditability & Reduced Cell Error:** Formula errors in hidden spreadsheet cells can obscure misallocations. Python isolates logic, parameters, and constraints into clear, version-controlled code on GitHub.
4. **Automated Pipeline Integration:** Instead of manual spreadsheet copy-pasting, Python scripts pull live inventory levels and store demand forecasts straight from SQL databases or ERP systems.
""")
