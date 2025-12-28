# test_admin.py
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# 1. Login with testadmin
print("1. Logging in...")
login_resp = requests.post(f"{BASE_URL}/auth/login/", json={
    "email": "testadmin@example.com",
    "password": "testadmin"  # Use the password you registered with
})

if login_resp.status_code != 200:
    print(f"Login failed: {login_resp.status_code}")
    print(login_resp.json())
    exit()

token = login_resp.json()["data"]["access"]
print(f"Token: {token[:50]}...")

# 2. Check user info
print("\n2. Checking user role...")
headers = {"Authorization": f"Bearer {token}"}
me_resp = requests.get(f"{BASE_URL}/users/me/", headers=headers)
me_data = me_resp.json()
print(f"Status: {me_resp.status_code}")
print(f"Role: {me_data.get('data', {}).get('role', 'NO ROLE!')}")

# 3. Try to create category
print("\n3. Testing category creation...")
cat_resp = requests.post(
    f"{BASE_URL}/categories/",
    headers=headers,
    json={"name": "Test Category"}
)
print(f"Status: {cat_resp.status_code}")
print(f"Response: {cat_resp.text}")