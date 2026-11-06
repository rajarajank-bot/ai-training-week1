
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. NumPy Operation
marks = np.array([
    [75, 80, 85],
    [60, 65, 70],
    [88, 92, 79],
    [90, 85, 95]
])

print(f"Array Shape: {marks.shape}")
print(f"Student averages (axis=1): {marks.mean(axis=1)}")
print(f"Subject averages (axis=0): {marks.mean(axis=0)}")

# Broadcasting: 5 grace marks 
marks_with_grace = marks + 5

# Weighted scores 
weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(marks_with_grace, weights)
print(f"Weighted Scores: {weighted_scores}")

# ==========================================
# 2. Pandas Operations & Data Cleaning
# ==========================================
dirty_data = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 8],
    "name": ["Arun", "Priya", "Rahul", "Divya", "Karthik", "Meena", "Suresh", "Anitha", "Anitha"],
    "department": ["Sales", "HR", "IT", "IT", "Finance", "Sales", "IT", "HR", "HR"],
    "salary": [30000, np.nan, 60000, 75000, 90000, np.nan, 68000, 48000, 48000],
    "city": ["Chennai", "Chennai", "Bangalore", "Chennai", "Mumbai", "Bangalore", "Chennai", "Mumbai", "Mumbai"]
}
df_emp = pd.DataFrame(dirty_data)

# Data Cleaning: Duplicates 
df_emp = df_emp.drop_duplicates()
median_sal = df_emp["salary"].median()
df_emp["salary"] = df_emp["salary"].fillna(median_sal).astype(int)

# Groupby Aggregation: Headcount, Average, Max Salary
summary = df_emp.groupby("department")["salary"].agg(
    headcount="count",
    average_salary="mean",
    max_salary="max"
).reset_index()

print("\nDepartment Summary:")
print(summary)

# Merge with departments.csv (Outer join)
df_dept = pd.read_csv("departments.csv")
merged_outer = pd.merge(df_emp, df_dept, on="department", how="outer")

empty_dept = merged_outer[merged_outer["id"].isna()]["department"].tolist()
print(f"\nOuter join department with no employees: {empty_dept}")

# ==========================================
# 3. Matplotlib Visualizations (4 Charts)
# ==========================================

# Chart 1: Bar Chart (Headcount per Department)
plt.figure(figsize=(6, 4))
plt.bar(summary["department"], summary["headcount"], color='skyblue', label='Headcount')
plt.title("Employee Headcount by Department")
plt.xlabel("Department")
plt.ylabel("Headcount")
plt.legend()
plt.tight_layout()
plt.savefig("1_avg_salary_per_department.png")
plt.close()
# Insight: IT department has the highest employee headcount.

# Chart 2: Histogram (Salary Distribution)
plt.figure(figsize=(6, 4))
plt.hist(df_emp["salary"], bins=5, color='salmon', edgecolor='black', label='Salaries')
plt.title("Salary Distribution")
plt.xlabel("Salary (INR)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("2_salary_histogram.png")
plt.close()
# Insight: Most employee salaries fall in the 60,000 to 75,000 range.

# Chart 3: Scatter Plot (ID vs Salary)
plt.figure(figsize=(6, 4))
plt.scatter(df_emp["id"], df_emp["salary"], color='purple', label='Employee Salary')
plt.title("Employee ID vs Salary")
plt.xlabel("Employee ID")
plt.ylabel("Salary (INR)")
plt.legend()
plt.tight_layout()
plt.savefig("3_id_vs_salary_scatter.png")
plt.close()
# Insight: There is no strict linear correlation between ID and salary.

# Chart 4: Line Chart (Average Salary Trend)
plt.figure(figsize=(6, 4))
plt.plot(summary["department"], summary["average_salary"], marker='o', color='green', label='Avg Salary')
plt.title("Average Salary per Department")
plt.xlabel("Department")
plt.ylabel("Average Salary (INR)")
plt.legend()
plt.tight_layout()
plt.savefig("4_salary_trend_line.png")
plt.close()
# Insight: Finance holds the highest average salary across all departments.