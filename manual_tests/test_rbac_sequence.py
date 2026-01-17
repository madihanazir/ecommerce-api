# test_rbac_sequence.py
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

class RBACTester:
    def __init__(self):
        self.admin_token = None
        self.customer_token = None
        self.category_id = None
        self.product_id = None
    
    def print_step(self, num, title):
        print(f"\n{'='*60}")
        print(f"STEP {num}: {title}")
        print(f"{'='*60}")
    
    def test_admin_login(self):
        self.print_step(1, "ADMIN LOGIN")
        response = requests.post(f"{BASE_URL}/auth/login/", json={
            "email": "testadmin@example.com",
            "password": "testadmin"  # Change if different
        })
        
        if response.status_code != 200:
            print(f"❌ Admin login failed: {response.status_code}")
            print(response.json())
            return False
        
        self.admin_token = response.json()["data"]["access"]
        print(f"✅ Admin token: {self.admin_token[:30]}...")
        return True
    
    def test_customer_register_and_login(self):
        self.print_step(2, "CUSTOMER REGISTRATION & LOGIN")
        
        # Register customer
        register_resp = requests.post(f"{BASE_URL}/auth/register/", json={
            "username": "testcustomer",
            "email": "testcustomer@example.com",
            "password": "customer123",
            "phone": "1234567890"
        })
        
        if register_resp.status_code not in [201, 400]:  # 400 if already exists
            print(f"❌ Customer registration: {register_resp.status_code}")
        
        # Login as customer
        login_resp = requests.post(f"{BASE_URL}/auth/login/", json={
            "email": "testcustomer@example.com",
            "password": "customer123"
        })
        
        if login_resp.status_code != 200:
            print(f"❌ Customer login: {login_resp.status_code}")
            return False
        
        self.customer_token = login_resp.json()["data"]["access"]
        print(f"✅ Customer token: {self.customer_token[:30]}...")
        return True
    
    def test_user_endpoints(self):
        self.print_step(3, "USER ENDPOINTS")
        
        headers_admin = {"Authorization": f"Bearer {self.admin_token}"}
        headers_customer = {"Authorization": f"Bearer {self.customer_token}"}
        
        # Test /users/me
        me_admin = requests.get(f"{BASE_URL}/users/me/", headers=headers_admin)
        me_customer = requests.get(f"{BASE_URL}/users/me/", headers=headers_customer)
        
        print(f"Admin /me/: {me_admin.status_code}")
        if me_admin.status_code == 200:
            print(f"  Role: {me_admin.json().get('data', {}).get('role')}")
        
        print(f"Customer /me/: {me_customer.status_code}")
        if me_customer.status_code == 200:
            print(f"  Role: {me_customer.json().get('data', {}).get('role')}")
        
        # Test admin-only endpoint
        admin_test = requests.get(f"{BASE_URL}/admin-test/", headers=headers_admin)
        customer_test = requests.get(f"{BASE_URL}/admin-test/", headers=headers_customer)
        
        print(f"\nAdmin /admin-test/: {admin_test.status_code}")
        print(f"Customer /admin-test/: {customer_test.status_code}")
        
        return (me_admin.status_code == 200 and 
                me_customer.status_code == 200 and
                admin_test.status_code == 200 and
                customer_test.status_code == 403)
    
    def test_categories_rbac(self):
        self.print_step(4, "CATEGORIES RBAC")
        
        headers_admin = {"Authorization": f"Bearer {self.admin_token}"}
        headers_customer = {"Authorization": f"Bearer {self.customer_token}"}
        
        # Admin creates category
        cat_data = {"name": "Test Category RBAC"}
        create_admin = requests.post(
            f"{BASE_URL}/categories/",
            json=cat_data,
            headers=headers_admin
        )
        
        print(f"Admin POST /categories/: {create_admin.status_code}")
        if create_admin.status_code == 201:
            self.category_id = create_admin.json()["data"]["id"]
            print(f"  Category ID: {self.category_id}")
        
        # Customer tries to create category (should fail)
        create_customer = requests.post(
            f"{BASE_URL}/categories/",
            json=cat_data,
            headers=headers_customer
        )
        
        print(f"Customer POST /categories/: {create_customer.status_code}")
        
        # Both should be able to GET
        get_admin = requests.get(f"{BASE_URL}/categories/", headers=headers_admin)
        get_customer = requests.get(f"{BASE_URL}/categories/", headers=headers_customer)
        
        print(f"Admin GET /categories/: {get_admin.status_code}")
        print(f"Customer GET /categories/: {get_customer.status_code}")
        
        return (create_admin.status_code == 201 and
                create_customer.status_code == 403 and
                get_admin.status_code == 200 and
                get_customer.status_code == 200)
    
    def test_products_rbac(self):
        self.print_step(5, "PRODUCTS RBAC")
        
        if not self.category_id:
            print("⚠️ No category ID, using ID 1")
            self.category_id = 1
        
        headers_admin = {"Authorization": f"Bearer {self.admin_token}"}
        headers_customer = {"Authorization": f"Bearer {self.customer_token}"}
        
        # Admin creates product
        product_data = {
            "name": "RBAC Test Product",
            "price": 99.99,
            "category": self.category_id,
            "description": "Test product for RBAC"
        }
        
        create_admin = requests.post(
            f"{BASE_URL}/products/",
            json=product_data,
            headers=headers_admin
        )
        
        print(f"Admin POST /products/: {create_admin.status_code}")
        if create_admin.status_code == 201:
            self.product_id = create_admin.json()["data"]["id"]
        
        # Customer tries to create product (should fail)
        create_customer = requests.post(
            f"{BASE_URL}/products/",
            json=product_data,
            headers=headers_customer
        )
        
        print(f"Customer POST /products/: {create_customer.status_code}")
        
        # Both should be able to GET
        get_admin = requests.get(f"{BASE_URL}/products/", headers=headers_admin)
        get_customer = requests.get(f"{BASE_URL}/products/", headers=headers_customer)
        
        print(f"Admin GET /products/: {get_admin.status_code}")
        print(f"Customer GET /products/: {get_customer.status_code}")
        
        return (create_admin.status_code == 201 and
                create_customer.status_code == 403 and
                get_admin.status_code == 200 and
                get_customer.status_code == 200)
    
    def run_all_tests(self):
        print("🚀 STARTING COMPLETE RBAC TEST SEQUENCE")
        
        tests = [
            ("Admin Login", self.test_admin_login()),
            ("Customer Registration & Login", self.test_customer_register_and_login()),
            ("User Endpoints", self.test_user_endpoints()),
            ("Categories RBAC", self.test_categories_rbac()),
            ("Products RBAC", self.test_products_rbac()),
        ]
        
        self.print_step(6, "TEST SUMMARY")
        
        passed = 0
        total = len(tests)
        
        for name, result in tests:
            status = "✅" if result else "❌"
            print(f"{status} {name}")
            if result:
                passed += 1
        
        print(f"\n📊 Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL RBAC TESTS PASSED!")
        else:
            print("⚠️ Some tests failed. Check above for details.")
        
        return passed == total

if __name__ == "__main__":
    tester = RBACTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)