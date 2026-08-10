from pulp import *
import pandas as pd
import matplotlib.pyplot as plt
import sys

data = pd.read_csv("production_data.csv")

paint_capacity = float(sys.argv[1])
body_capacity = float(sys.argv[2])
assembly_capacity = float(sys.argv[3])

# Read data from CSV

profit = dict(zip(data["Vehicle"], data["Profit"]))
paint = dict(zip(data["Vehicle"], data["Paint"]))
body = dict(zip(data["Vehicle"], data["Body"]))
assembly = dict(zip(data["Vehicle"], data["Assembly"]))
demand = dict(zip(data["Vehicle"], data["Demand"]))


print(data)

# ==========================
# Create Optimization Model
# ==========================

model = LpProblem("Toyota_Production_Planning", LpMaximize)

# ==========================
# Decision Variables
# ==========================

corolla = LpVariable("Corolla", lowBound=0, cat="Integer")
camry = LpVariable("Camry", lowBound=0, cat="Integer")
rav4 = LpVariable("RAV4", lowBound=0, cat="Integer")
highlander = LpVariable("Highlander", lowBound=0, cat="Integer")
prius = LpVariable("Prius", lowBound=0, cat="Integer")

# ==========================
# Objective Function
# ==========================

model += (
    profit["Corolla"] * corolla +
    profit["Camry"] * camry +
    profit["RAV4"] * rav4 +
    profit["Highlander"] * highlander +
    profit["Prius"] * prius
)

# ==========================
# Constraints
# ==========================

# Engine Capacity
model += (
    corolla + camry + rav4 + highlander + prius <= 600,
    "Engine_Capacity"
)

# Transmission Capacity
model += corolla + camry + rav4 + highlander + prius <= 600

# Paint Shop Capacity
model += (
    2.1 * corolla +
    2.5 * camry +
    3.0 * rav4 +
    3.5 * highlander +
    2.4 * prius
    <= paint_capacity,
    "Paint_Capacity"
)

# Body Shop Capacity
model += (
    2.5 * corolla +
    3.0 * camry +
    3.5 * rav4 +
    4.0 * highlander +
    2.8 * prius
    <= body_capacity,
    "Body_Capacity"
)

# Assembly Capacity
model += (
    5 * corolla +
    6 * camry +
    7.5 * rav4 +
    9 * highlander +
    5.5 * prius
    <= assembly_capacity,
    "Assembly_Capacity"
)

# Market Demand
model += (
    corolla <= demand["Corolla"],
    "Corolla_Demand"
)

model += (
    camry <= demand["Camry"],
    "Camry_Demand"
)

model += (
    rav4 <= demand["RAV4"],
    "RAV4_Demand"
)

model += (
    highlander <= demand["Highlander"],
    "Highlander_Demand"
)

model += (
    prius <= demand["Prius"],
    "Prius_Demand"
)

# ==========================
# Solve Model
# ==========================

model.solve()
print("\n========== SHADOW PRICES ==========\n")

for name, constraint in model.constraints.items():
    print(
        f"{name}: Shadow Price = {constraint.pi}, Slack = {constraint.slack}"
    )

shadow_data = []

for name, constraint in model.constraints.items():

    shadow_data.append({
        "Constraint": name,
        "Shadow Price": constraint.pi,
        "Slack": constraint.slack
    })

shadow_df = pd.DataFrame(shadow_data)

shadow_df.to_excel(
    "outputs/shadow_prices.xlsx",
    index=False
)

# ==========================
# Results
# ==========================

print("\n========== TOYOTA PRODUCTION PLAN ==========\n")

print("Status:", LpStatus[model.status])

print("\nOptimal Production:\n")

print("Corolla     :", int(value(corolla)))
print("Camry       :", int(value(camry)))
print("RAV4        :", int(value(rav4)))
print("Highlander  :", int(value(highlander)))
print("Prius       :", int(value(prius)))

print("\nMaximum Profit = ${:,.0f}".format(value(model.objective)))

# ==========================
# Save Results to Excel
# ==========================

results = pd.DataFrame({

    "Vehicle":[
        "Corolla",
        "Camry",
        "RAV4",
        "Highlander",
        "Prius"
    ],

    "Production":[
        value(corolla),
        value(camry),
        value(rav4),
        value(highlander),
        value(prius)
    ]

})

results.to_excel("outputs/production_plan.xlsx", index=False)

print("\nResults saved to outputs/production_plan.xlsx")

# ==========================
# Production Chart
# ==========================

vehicles = ["Corolla", "Camry", "RAV4", "Highlander", "Prius"]

production = [
    value(corolla),
    value(camry),
    value(rav4),
    value(highlander),
    value(prius)
]

plt.figure(figsize=(8,5))
plt.bar(vehicles, production)

plt.title("Toyota Production Plan")
plt.xlabel("Vehicle")
plt.ylabel("Units Produced")

plt.savefig("outputs/production_chart.png")
plt.show()

print("Chart saved to outputs/production_chart.png")