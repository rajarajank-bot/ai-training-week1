# Task 1: Python Core, OOP and Errors

# 1. Custom Exception
class InvalidSalaryError(Exception):
    pass

# 2. Base Class - Employee
class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"

# Derived Class - Manager (Inheritance & super())
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return f"Manager: {self.name}, Salary: {self.salary}, Team Size: {self.team_size}"

# 3. Bonus Function
def bonus(salary, rate=0.1, *extras, **options):
    total_bonus = (salary * rate) + sum(extras)
    if 'cap' in options:
        total_bonus = min(total_bonus, options['cap'])
    return total_bonus

# 4. Employees Data
employees_data = [
    {"id": 1, "name": "Arun", "department": "Sales", "salary": 30000, "city": "Chennai"},
    {"id": 2, "name": "Priya", "department": "HR", "salary": 45000, "city": "Chennai"},
    {"id": 3, "name": "Rahul", "department": "IT", "salary": 60000, "city": "Bangalore"},
    {"id": 4, "name": "Divya", "department": "IT", "salary": 75000, "city": "Chennai"},
    {"id": 5, "name": "Karthik", "department": "Finance", "salary": 90000, "city": "Mumbai"},
    {"id": 6, "name": "Meena", "department": "Sales", "salary": 52000, "city": "Bangalore"},
    {"id": 7, "name": "Suresh", "department": "IT", "salary": 68000, "city": "Chennai"},
    {"id": 8, "name": "Anitha", "department": "HR", "salary": 48000, "city": "Mumbai"}
]

# List Comprehension (> 50000)
above_50k = [emp['name'] for emp in employees_data if emp['salary'] > 50000]
print(f"Above 50000: {above_50k}")

# Filter (Chennai employees)
chennai_emps = list(filter(lambda emp: emp['city'] == 'Chennai', employees_data))
chennai_names = [emp['name'] for emp in chennai_emps]
print(f"Chennai: {chennai_names}")

# Map & Lambda (10% raise)
raised_salaries = list(map(lambda emp: {**emp, 'salary': emp['salary'] * 1.10}, employees_data))

# 5. For Loop (continue & break)
for emp in employees_data:
    if emp['salary'] <= 0:
        continue
    if emp['salary'] > 85000:
        break

# 6. Exception Handling (try, except, finally)
try:
    emp_error_test = Employee("TestUser", -500)
except InvalidSalaryError as err:
    print(f"Error: {err}")
finally:
    print("Transaction finished")