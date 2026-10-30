import pandas as pd

# 1. Cleaned orders data
orders_data = """order_id,customer_id,amount
1,101,500.0
2,102,600.0
3,101,700.0
4,103,300.0
5,104,900.0"""

with open("orders_cleaned.csv", "w") as f:
    f.write(orders_data)

orders_df = pd.read_csv("orders_cleaned.csv")

# Create customers.csv
customers_data = """customer_id,name,city
101,Arun,Chennai
102,Priya,Mumbai
103,Rahul,Chennai
105,Divya,Bangalore"""

with open("customers.csv", "w") as f:
    f.write(customers_data)

customers_df = pd.read_csv("customers.csv")

# 2. Inner join
inner_join_df = pd.merge(orders_df, customers_df, on='customer_id', how='inner')

# 3. Left join to find customers with no orders
left_join_df = pd.merge(customers_df, orders_df, on='customer_id', how='left')
no_orders = left_join_df[left_join_df['order_id'].isna()]['name'].tolist()

# 4. Outer join to find orders with no customer record
outer_join_df = pd.merge(orders_df, customers_df, on='customer_id', how='outer')
order_without_customer = outer_join_df[outer_join_df['name'].isna()]['customer_id'].tolist()

# Expected output
print(f"Inner join rows: {len(inner_join_df)} (customer 104 dropped)")
print(f"No orders: {', '.join(no_orders)}")
print(f"Order without customer: customer_id {int(order_without_customer[0])}")

# 3-line explanation for joins
print("\nJoin Explanations:")
print("1. Inner Join: Returns only the rows where the join key matches in both DataFrames.")
print("2. Left Join: Keeps all records from the left DataFrame and fills unmatched columns from the right with NaN.")
print("3. Outer Join: Retains all records from both DataFrames, populating NaN wherever matching keys are missing.")

# Bonus Challenge: Concat two files and repeat groupby
orders_month2_data = """order_id,customer_id,amount
6,101,400.0
7,105,800.0"""

with open("orders_month2.csv", "w") as f:
    f.write(orders_month2_data)

orders_month2_df = pd.read_csv("orders_month2.csv")

# Combine datasets
combined_orders = pd.concat([orders_df, orders_month2_df], ignore_index=True)

# Groupby on combined data
bonus_result = combined_orders.groupby('customer_id').agg(
    total=('amount', 'sum'),
    orders=('order_id', 'count')
)

print("\n--- Bonus Challenge: Combined GroupBy Output ---")
print(bonus_result)