import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_auth():
    print("=== RBAC SANITY TEST ===")
    
    # 1. Login as admin
    admin_resp = requests.post(f"{BASE_URL}/auth/login/", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    admin_token = admin_resp.json()["data"]["access"]
    print(f"Admin Token: {admin_token[:50]}...")
    
    # 2. Login as customer
    customer_resp = requests.post(f"{BASE_URL}/auth/login/", json={
        "email": "customer@test.com",
        "password": "customer123"
    })
    customer_token = customer_resp.json()["data"]["access"]
    print(f"Customer Token: {customer_token[:50]}...")
    
    # 3. Test /users/me
    headers = {"Authorization": f"Bearer {admin_token}"}
    me_resp = requests.get(f"{BASE_URL}/users/me/", headers=headers)
    print(f"Admin /me/: {me_resp.status_code}")
    print(f"Admin Role: {me_resp.json()}")
    
    # 4. Test products read (both should work)
    print("\n=== Testing Product Read ===")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    customer_headers = {"Authorization": f"Bearer {customer_token}"}
    
    prod_resp_admin = requests.get(f"{BASE_URL}/products/", headers=admin_headers)
    prod_resp_customer = requests.get(f"{BASE_URL}/products/", headers=customer_headers)
    
    print(f"Admin GET /products/: {prod_resp_admin.status_code}")
    print(f"Customer GET /products/: {prod_resp_customer.status_code}")
    
    # 5. Test product create (only admin)
    print("\n=== Testing Product Create ===")
    product_data = {"name": "RBAC Test Product", "price": 99.99}
    
    create_admin = requests.post(
        f"{BASE_URL}/products/", 
        json=product_data, 
        headers=admin_headers
    )
    create_customer = requests.post(
        f"{BASE_URL}/products/", 
        json=product_data, 
        headers=customer_headers
    )
    
    print(f"Admin POST /products/: {create_admin.status_code}")
    print(f"Customer POST /products/: {create_customer.status_code}")
    
    print("\n=== TEST SUMMARY ===")
    if (prod_resp_admin.status_code == 200 and 
        prod_resp_customer.status_code == 200 and
        create_admin.status_code == 201 and
        create_customer.status_code == 403):
        print("RBAC WORKING CORRECTLY!")
    else:
        print("RBAC ISSUES DETECTED")

if __name__ == "__main__":
    test_auth()