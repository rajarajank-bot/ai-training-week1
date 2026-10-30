import csv
import json
import os
import requests
from dotenv import load_dotenv

# 1. Load Environment Variables (.env)
load_dotenv()
api_key = os.getenv("API_KEY")

# 2. Read employees.csv with csv.DictReader
employees = []
high_earners = []

with open("employees.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        clean_row = {k.strip(): v.strip() for k, v in row.items()}
        employees.append(clean_row)
        if int(clean_row["salary"]) > 50000:
            high_earners.append(clean_row)

print(f"Rows read: {len(employees)} High earners: {len(high_earners)}")

# Write to employees.json
with open("employees.json", mode="w", encoding="utf-8") as json_file:
    json.dump(employees, json_file, indent=4)

# Write to high_earners.csv
if high_earners:
    with open("high_earners.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=high_earners[0].keys())
        writer.writeheader()
        writer.writerows(high_earners)

# 3. GET API Request with timeout=5
try:
    response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
    response.raise_for_status()
    users_data = response.json()

    for user in users_data[:3]:
        print(f"{user.get('id')}\t{user.get('name')}\t{user.get('email')}")

    parsed_users = []
    for user in users_data:
        parsed_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city")
        })

    with open("users.json", mode="w", encoding="utf-8") as u_file:
        json.dump(parsed_users, u_file, indent=4)

except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
    print(f"Network error: {err}")

# 4. Handle 404 Status Code for /users/9999
res_404 = requests.get("https://jsonplaceholder.typicode.com/users/9999", timeout=5)
if res_404.status_code == 404:
    print("/users/9999 > 404 Not found")