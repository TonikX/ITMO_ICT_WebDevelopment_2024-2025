import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = "http://127.0.0.1:8000/auth/token/"

USERNAME = "admin"
PASSWORD = "admin"

def get_token():
    response = requests.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})
    print("Response Status Code:", response.status_code)
    print("Response Content:", json.dumps(response.json(), indent=4))
    return response.json().get("access")

def pretty_print_response(response):
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print("Failed to retrieve data:", response.status_code, response.content)

def test_get_organizations(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/organizations/", headers=headers)
    pretty_print_response(response)

def test_get_employees(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/employees/", headers=headers)
    pretty_print_response(response)

def test_get_contracts(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/contracts/", headers=headers)
    pretty_print_response(response)

def test_get_insurance_cases(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/insurance_cases/", headers=headers)
    pretty_print_response(response)

def test_get_employee_contracts(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/employee_contracts/1/", headers=headers)
    pretty_print_response(response)

if __name__ == "__main__":
    token = get_token()
    if token:
        test_get_organizations(token)
        test_get_employees(token)
        test_get_contracts(token)
        test_get_insurance_cases(token)
        test_get_employee_contracts(token)
    else:
        print("Failed to obtain token")