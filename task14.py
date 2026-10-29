 
import pandas as pd
import matplotlib.pyplot as plt


if not os.path.exists("employees.csv"):
    sample_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "department": ["IT", "HR", "Sales", "IT", "HR", "Sales", "IT", "HR", "Sales", "IT"],
        "salary": [70000, 50000, 60000, 80000, 52000, 65000, 90000, 48000, 72000, 110000]
    }
    pd.DataFrame(sample_data).to_csv("employees.csv", index=False)
    print("Created a dummy 'employees.csv' for demonstration.")


df = pd.read_csv("employees.csv")

plt.figure(figsize=(6, 4))
avg_salary = df.groupby("department")["salary"].mean()
bars = plt.bar(avg_salary.index, avg_salary.values, color=['skyblue', 'salmon', 'lightgreen'])


for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1500, f"${yval:,.0f}", ha='center', va='bottom', fontsize=9)

plt.title("Average Salary per Department")
plt.xlabel("Department")
plt.ylabel("Average Salary ($)")
plt.tight_layout()
plt.savefig("1_avg_salary_per_department.png")
plt.close()


plt.figure(figsize=(6, 4))
plt.hist(df["salary"], bins=5, color="mediumpurple", edgecolor="black")
plt.title("Distribution of Salaries")
plt.xlabel("Salary ($)")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig("2_salary_histogram.png")
plt.close()



plt.figure(figsize=(6, 4))
departments = df["department"].unique()
colors = ['blue', 'orange', 'green', 'red'][:len(departments)] # Add more if needed

for dept, color in zip(departments, colors):
    dept_df = df[df["department"] == dept]
    plt.scatter(dept_df["id"], dept_df["salary"], label=dept, color=color, s=100, edgecolors='black')

plt.title("Employee ID vs Salary (by Department)")
plt.xlabel("Employee ID")
plt.ylabel("Salary ($)")
plt.legend(title="Department")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("3_id_vs_salary_scatter.png")
plt.close()



months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12, 15, 14, 18, 22, 25]

plt.figure(figsize=(6, 4))
plt.plot(months, sales, marker='o', color='crimson', linewidth=2, label="Sales Trends")

for i, txt in enumerate(sales):
    plt.annotate(txt, (months[i], sales[i]), textcoords="offset points", xytext=(0, 7), ha='center', fontweight='bold')

plt.title("Monthly Sales Trend (Jan to Jun)")
plt.xlabel("Month")
plt.ylabel("Sales (units)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("4_monthly_sales_line.png")
plt.close()



fig, axs = plt.subplots(2, 2, figsize=(14, 10))


axs[0, 0].bar(avg_salary.index, avg_salary.values, color=['skyblue', 'salmon', 'lightgreen'])
axs[0, 0].set_title("Average Salary per Department")
axs[0, 0].set_xlabel("Department")
axs[0, 0].set_ylabel("Average Salary ($)")


axs[0, 1].hist(df["salary"], bins=5, color="mediumpurple", edgecolor="black")
axs[0, 1].set_title("Distribution of Salaries")
axs[0, 1].set_xlabel("Salary ($)")
axs[0, 1].set_ylabel("Number of Employees")

for dept, color in zip(departments, colors):
    dept_df = df[df["department"] == dept]
    axs[1, 0].scatter(dept_df["id"], dept_df["salary"], label=dept, color=color, s=80, edgecolors='black')
axs[1, 0].set_title("Employee ID vs Salary (by Department)")
axs[1, 0].set_xlabel("Employee ID")
axs[1, 0].set_ylabel("Salary ($)")
axs[1, 0].legend()
axs[1, 0].grid(True, linestyle="--", alpha=0.4)


axs[1, 1].plot(months, sales, marker='o', color='crimson', linewidth=2)
for i, txt in enumerate(sales):
    axs[1, 1].annotate(txt, (months[i], sales[i]), textcoords="offset points", xytext=(0, 5), ha='center')
axs[1, 1].set_title("Monthly Sales Trend (Jan to Jun)")
axs[1, 1].set_xlabel("Month")
axs[1, 1].set_ylabel("Sales (units)")
axs[1, 1].grid(True, linestyle=":", alpha=0.4)

plt.suptitle("Task-1: Dashboard Visualizations", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("bonus_all_charts.png")
plt.show()

print("All individual charts and the combined bonus chart have been saved successfully!")