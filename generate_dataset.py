import pandas as pd
import numpy as np

# Reproducible results
np.random.seed(42)

# Number of orders
n = 10000

print("Dataset generation started...")
print(f"Number of orders: {n}")

# Products
products = [
    "Laptop",
    "Smartphone",
    "Tablet",
    "Headphones",
    "Smartwatch",
    "Monitor",
    "Keyboard",
    "Mouse",
    "T-Shirt",
    "Jeans",
    "Shoes",
    "Jacket",
    "Coffee Maker",
    "Blender",
    "Backpack"
]

# Business regions
regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

# Payment methods
payment_methods = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Cash on Delivery",
    "Net Banking"
]

# Customer types
customer_types = [
    "New",
    "Returning",
    "VIP"
]

print("Products, regions and customer types defined.")

# Product categories
categories = {
    "Laptop": "Electronics",
    "Smartphone": "Electronics",
    "Tablet": "Electronics",
    "Headphones": "Electronics",
    "Smartwatch": "Electronics",
    "Monitor": "Electronics",
    "Keyboard": "Electronics",
    "Mouse": "Electronics",

    "T-Shirt": "Fashion",
    "Jeans": "Fashion",
    "Shoes": "Fashion",
    "Jacket": "Fashion",

    "Coffee Maker": "Home & Kitchen",
    "Blender": "Home & Kitchen",

    "Backpack": "Accessories"
}

print("Product categories mapped.")

# Generate Order IDs
order_ids = [
    f"ORD-{100000 + i}"
    for i in range(n)
]

# Generate Customer IDs
customer_ids = [
    f"CUST-{np.random.randint(1000, 5000)}"
    for _ in range(n)
]

# Generate order dates
order_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2024-01-01", "2025-12-31"),
        size=n
    )
)

print("Order IDs, customer IDs and dates generated.")

# Create the main dataset
df = pd.DataFrame({
    "Order_ID": order_ids,
    "Order_Date": order_dates,
    "Customer_ID": customer_ids,
    "Product": np.random.choice(products, n),
    "Region": np.random.choice(regions, n),
    "Payment_Method": np.random.choice(payment_methods, n),
    "Customer_Type": np.random.choice(
        customer_types,
        n,
        p=[0.55, 0.35, 0.10]
    ),
    "Quantity": np.random.randint(1, 6, n)
})

# Add product category
df["Category"] = df["Product"].map(categories)

print("Main order DataFrame created.")
print(df.head())
# Product price ranges
price_ranges = {
    "Laptop": (45000, 100000),
    "Smartphone": (15000, 80000),
    "Tablet": (12000, 50000),
    "Headphones": (1000, 15000),
    "Smartwatch": (2000, 30000),
    "Monitor": (8000, 40000),
    "Keyboard": (800, 6000),
    "Mouse": (400, 3000),
    "T-Shirt": (500, 2500),
    "Jeans": (1000, 4000),
    "Shoes": (1500, 8000),
    "Jacket": (2000, 10000),
    "Coffee Maker": (2500, 15000),
    "Blender": (1500, 8000),
    "Backpack": (800, 5000)
}

# Generate unit price based on product
df["Unit_Price"] = df["Product"].apply(
    lambda product: np.random.randint(
        price_ranges[product][0],
        price_ranges[product][1] + 1
    )
)

# Generate discount percentages
df["Discount"] = np.random.choice(
    [0, 5, 10, 15, 20, 25],
    size=n,
    p=[0.15, 0.20, 0.25, 0.20, 0.15, 0.05]
)

print("Prices and discounts generated.")

# Calculate sales before discount
df["Gross_Sales"] = (
    df["Quantity"] * df["Unit_Price"]
).round(2)

# Calculate discount amount
df["Discount_Amount"] = (
    df["Gross_Sales"] * df["Discount"] / 100
).round(2)

# Calculate final sales/revenue
df["Sales"] = (
    df["Gross_Sales"] - df["Discount_Amount"]
).round(2)

# Generate product cost
cost_percentage = np.random.uniform(0.55, 0.85, n)

df["Cost"] = (
    df["Sales"] * cost_percentage
).round(2)

# Calculate profit
df["Profit"] = (
    df["Sales"] - df["Cost"]
).round(2)

# Calculate profit margin
df["Profit_Margin"] = (
    (df["Profit"] / df["Sales"]) * 100
).round(2)

print("Sales, cost, profit and profit margin calculated.")

# -----------------------------
# Add realistic data-quality issues
# -----------------------------

# 1. Missing discount values
missing_discount_indices = np.random.choice(
    df.index,
    size=100,
    replace=False
)

df.loc[missing_discount_indices, "Discount"] = np.nan


# 2. Missing customer types
missing_customer_indices = np.random.choice(
    df.index,
    size=50,
    replace=False
)

df.loc[missing_customer_indices, "Customer_Type"] = np.nan


# 3. Duplicate orders
duplicates = df.sample(
    n=50,
    random_state=42
)

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)

print("Data-quality issues added.")
print(f"Current records: {len(df)}")
# -----------------------------
# Add sales anomalies
# -----------------------------

# Select 20 random orders
anomaly_indices = np.random.choice(
    df.index,
    size=20,
    replace=False
)

# Make their sales unusually high
df.loc[anomaly_indices, "Sales"] *= 5

# Make their profit unusually high
df.loc[anomaly_indices, "Profit"] *= 5

# Recalculate profit margin
df.loc[anomaly_indices, "Profit_Margin"] = (
    df.loc[anomaly_indices, "Profit"]
    / df.loc[anomaly_indices, "Sales"]
    * 100
).round(2)

print("Sales anomalies added.")
# -----------------------------
# Finalize and save dataset
# -----------------------------

# Sort data by order date
df = df.sort_values("Order_Date").reset_index(drop=True)

# Save as CSV
df.to_csv(
    "data/sales_data.csv",
    index=False
)

# Final validation
print("\n" + "=" * 50)
print("DATASET GENERATED SUCCESSFULLY!")
print("=" * 50)

print(f"Total records : {len(df)}")
print(f"Total columns : {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDataset saved to:")
print("data/sales_data.csv")