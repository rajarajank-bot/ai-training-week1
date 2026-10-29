import numpy as np
import pandas as pd

csv_content = """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai"""

with open("employees.csv", "w") as f:
    f.write(csv_content)

df = pd.read_csv("employees.csv")

print("--- df.head() ---")
print(df.head())

print("\n--- df.info() ---")
df.info()

print("\n--- df.describe() ---")
print(df.describe())

name_col = df['name']
name_salary_col = df[['name', 'salary']]


chennai_names = df.loc[df['city'] == 'Chennai', 'name'].tolist()


sliced_df = df.iloc[0:3, 1:3]
print("\n--- df.iloc[0:3, 1:3] ---")
print(sliced_df)


salary_above_50000_count = len(df[df['salary'] > 50000])
it_dept_names = df[df['department'] == 'IT']['name'].tolist()


print("\n--- Expected Output ---")
print("Chennai:", ", ".join(chennai_names))
print(f"Salary above 50000: {salary_above_50000_count} employees")
print("IT department:", ", ".join(it_dept_names))

arr_24 = np.arange(24).reshape(2, 3, 4)
print("\n--- Bonus Challenge ---")
for i, slice_arr in enumerate(arr_24):
    print(f"Slice {i} shape along axis 0: {slice_arr.shape}")