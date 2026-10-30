import os
import json
import requests
from dotenv import load_dotenv

# 1. Load .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Bonus Challenge: Safe get function with 3 retries on timeout
def safe_get(url, timeout=5, retries=3):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            return response
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt} timed out.")
            if attempt == retries:
                print("All retries exhausted.")
                return None
        except requests.exceptions.ConnectionError:
            print("Connection error occurred.")
            return None

# 2. Call httpbin.org/headers with X-API-Key
try:
    headers = {"X-API-Key": api_key}
    res_headers = requests.get("https://httpbin.org/headers", headers=headers, timeout=5)
    data = res_headers.json()
    received_key = data.get("headers", {}).get("X-Api-Key")
    print(f"Server received key: {received_key}")
except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
    print("Network error on headers call:", e)

# 3. Call delay/10 with a 3-second timeout
try:
    requests.get("https://httpbin.org/delay/10", timeout=3)
except requests.exceptions.Timeout:
    print("Timeout after 3 seconds: please try again")
except requests.exceptions.ConnectionError:
    print("Connection error occurred")

# 4. Handle 500 error using raise_for_status()
try:
    res_500 = requests.get("https://httpbin.org/status/500", timeout=5)
    res_500.raise_for_status()
except requests.exceptions.HTTPError:
    print("Server error 500 handled")
except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
    print("Network error")

# 5. Parse nested JSON and save to result.json
try:
    res_json = requests.get("https://httpbin.org/json", timeout=5)
    if res_json.status_code == 200:
        json_data = res_json.json()
        parsed_result = {
            "title": json_data.get("slideshow", {}).get("title"),
            "author": json_data.get("slideshow", {}).get("author")
        }
        with open("result.json", "w") as f:
            json.dump(parsed_result, f, indent=4)
except Exception as e:
    print("Error handling json:", e)