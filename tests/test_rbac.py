# test_rbac.py
import requests
import json
import sys
import os

# Add project to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_step(step_num, message):
    print(f"\n{'='*50}")
    print(f"STEP {step_num}: {message}")
    print(f"{'='*50}")

def test_rbac():
    print("🚀 STARTING RBAC SANITY TESTS")
    
    # Use hardcoded tokens or get them fresh
    ADMIN_EMAIL = "admin@test.com"
    CUSTOMER_EMAIL = "customer@test.com"
    PASSWORD = "test123"
    
    # Step 1: Register test users
    print_step(1, "REGISTERING TEST USERS")
    try:
        # Admin
        admin_reg = requests.post(f"{BASE_URL}/auth/register/", json={
            "username": "admin_user",
            "email": ADMIN_EMAIL,
            "password": PASSWORD
        })
        print(f"Admin register: {admin_reg.status_code}")
        
        # Customer
        customer_reg = requests.post(f"{BASE_URL}/auth/register/", json={
            "username": "customer_user",
            "email": CUSTOMER_EMAIL,
            "password": PASSWORD
        })
        print(f"Customer register: {customer_reg.status_code}")
    except Exception as e:
        print(f"Register error (users may exist): {e}")
    
    # Step 2: Get tokens
    print_step(2, "GETTING JWT TOKENS")
    
    # Admin login
    admin_login = requests.post(f"{BASE_URL}/auth/login/", json={
        "email": ADMIN_EMAIL,
        "password": PASSWORD
    })
    
    if admin_login.status_code != 200:
        print(f"❌ Admin login failed: {admin_login.status_code}")
        print(f"Response: {admin_login.text}")
        return
    
    admin_data = admin_login.json()
    admin_token = admin_data.get("data", {}).get("access")
    if admin_token:
        print(f"✅ Admin token: {admin_token[:30]}...")
        print(f"Admin full response: {json.dumps(admin_data, indent=2)}")
    else:
        print("❌ No admin token in response")
    
    # Customer login
    customer_login = requests.post(f"{BASE_URL}/auth/login/", json={
        "email": CUSTOMER_EMAIL,
        "password": PASSWORD
    })
    
    if customer_login.status_code != 200:
        print(f"❌ Customer login failed: {customer_login.status_code}")
        return
    
    customer_data = customer_login.json()
    customer_token = customer_data.get("data", {}).get("access")
    if customer_token:
        print(f"✅ Customer token: {customer_token[:30]}...")
    else:
        print("❌ No customer token")
    
    # Step 3: Test user endpoints
    print_step(3, "TESTING USER ENDPOINTS")
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    customer_headers = {"Authorization": f"Bearer {customer_token}"}
    
    # Test /users/me
    me_admin = requests.get(f"{BASE_URL}/users/me/", headers=admin_headers)
    print(f"Admin /users/me/: {me_admin.status_code}")
    if me_admin.status_code == 200:
        me_data = me_admin.json()
        print(f"   Role: {me_data.get('data', {}).get('role', 'N/A')}")
        print(f"   Email: {me_data.get('data', {}).get('email', 'N/A')}")
    
    me_customer = requests.get(f"{BASE_URL}/users/me/", headers=customer_headers)
    print(f"Customer /users/me/: {me_customer.status_code}")
    
    # Test /profile
    profile_admin = requests.get(f"{BASE_URL}/profile/", headers=admin_headers)
    print(f"Admin /profile/: {profile_admin.status_code}")
    
    # Test admin-test endpoint
    admin_test = requests.get(f"{BASE_URL}/admin-test/", headers=admin_headers)
    print(f"Admin /admin-test/: {admin_test.status_code}")
    if admin_test.status_code == 200:
        print(f"   Response: {admin_test.json()}")
    
    # Step 4: Test products RBAC
    print_step(4, "TESTING PRODUCTS RBAC")
    
    # First, create a category as admin
    print("Creating category as admin...")
    category_data = {"name": "Test Category RBAC"}
    create_category = requests.post(
        f"{BASE_URL}/categories/",
        json=category_data,
        headers=admin_headers
    )
    print(f"Admin POST /categories/: {create_category.status_code}")
    
    # Get category ID
    category_id = 1  # Default or extract from response
    
    # Test product GET (both should work)
    get_products_admin = requests.get(f"{BASE_URL}/products/", headers=admin_headers)
    print(f"Admin GET /products/: {get_products_admin.status_code}")
    
    get_products_customer = requests.get(f"{BASE_URL}/products/", headers=customer_headers)
    print(f"Customer GET /products/: {get_products_customer.status_code}")
    
    # Test product POST (admin only)
    product_data = {
        "name": "RBAC Test Product",
        "price": 99.99,
        "category": category_id
    }
    
    # Admin create
    create_product_admin = requests.post(
        f"{BASE_URL}/products/",
        json=product_data,
        headers=admin_headers
    )
    print(f"Admin POST /products/: {create_product_admin.status_code}")
    if create_product_admin.status_code != 201:
        print(f"   Error: {create_product_admin.text}")
    
    # Customer create (should fail)
    create_product_customer = requests.post(
        f"{BASE_URL}/products/",
        json=product_data,
        headers=customer_headers
    )
    print(f"Customer POST /products/: {create_product_customer.status_code}")
    if create_product_customer.status_code == 403:
        print("   ✅ CORRECT: Customer blocked from creating product")
    elif create_product_customer.status_code == 201:
        print("   ⚠️ WARNING: Customer can create product - RBAC broken!")
    else:
        print(f"   Unexpected: {create_product_customer.text}")
    
    # Step 5: Summary
    print_step(5, "TEST SUMMARY")
    
    success_conditions = [
        me_admin.status_code == 200,
        me_customer.status_code == 200,
        admin_test.status_code == 200,
        get_products_admin.status_code == 200,
        get_products_customer.status_code == 200,
        create_product_customer.status_code in [403, 401]  # Blocked or unauthorized
    ]
    
    passed = sum(success_conditions)
    total = len(success_conditions)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL RBAC TESTS PASSED!")
    else:
        print("⚠️ Some tests failed. Check above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = test_rbac()
    sys.exit(0 if success else 1)