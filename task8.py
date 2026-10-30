import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def explain_status(code):
    status_messages = {
        200: "200 OK - Request succeeded",
        201: "201 Created - Resource created successfully",
        400: "400 Bad Request - Invalid request",
        401: "401 Unauthorized - Authentication required",
        404: "404 Not Found - Resource not found",
        500: "500 Internal Server Error - Server encountered an error"
    }
    return status_messages.get(code, f"Status code: {code}")

res_users = requests.get(f"{BASE_URL}/users")
if res_users.status_code == 200:
    users = res_users.json()
    for user in users[:5]:
        print(f"{user['id']} - {user['name']} - {user['email']}")

new_post = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}
res_post = requests.post(f"{BASE_URL}/posts", json=new_post)
post_data = res_post.json()
print(f"POST: {res_post.status_code}, id: {post_data.get('id')}")

res_put = requests.put(f"{BASE_URL}/posts/1", json={"id": 1, "title": "updated title", "body": "updated body", "userId": 1})
res_patch = requests.patch(f"{BASE_URL}/posts/1", json={"title": "patched title"})
res_delete = requests.delete(f"{BASE_URL}/posts/1")

print(f"PUT: {res_put.status_code} | PATCH: {res_patch.status_code} | DELETE: {res_delete.status_code}")

res_404 = requests.get(f"{BASE_URL}/posts/9999")
if res_404.status_code == 404:
    print("GET /posts/9999 -> 404 Not found")
else:
    print(f"Status: {res_404.status_code}")