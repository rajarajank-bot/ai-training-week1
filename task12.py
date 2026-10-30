import pandas as pd

  
csv_content = """order_id,customer_id,amount
1,101,500
2,102,
3,101,700
3,101,700
4,103,300
5,104,900"""

with open("orders.csv", "w") as f:
    f.write(csv_content)

df = pd.read_csv("orders.csv")

missing_amount = df['amount'].isna().sum()
duplicate_count = df.duplicated().sum()

print(f"Missing: amount {missing_amount} | Duplicates: {duplicate_count}")

df = df.drop_duplicates()


amount_median = df['amount'].median()
print(f"Median used: {amount_median}")
df['amount'] = df['amount'].fillna(amount_median)

df['amount'] = pd.to_numeric(df['amount'])
df['order_id'] = df['order_id'].astype(str)


result = df.groupby('customer_id').agg(
    total=('amount', 'sum'),
    orders=('order_id', 'count')
)


print(result)