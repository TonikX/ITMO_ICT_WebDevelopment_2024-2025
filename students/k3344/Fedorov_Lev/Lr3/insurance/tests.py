import requests
from getpass import getpass

BASE_URL = 'http://127.0.0.1:8000'
LOGIN_URL = f'{BASE_URL}/auth/token/'
HEADERS = {}


def get_admin_token():
    username =  'admin'
    password =  'admin'

    response = requests.post(LOGIN_URL, data={
        'username': username,
        'password': password
    })

    if response.status_code == 200:
        token = response.json().get('access')
        print("Token received successfully.")
        HEADERS['Authorization'] = f'Bearer {token}'
    else:
        print("Failed to retrieve token. Check credentials.")
        exit()


def test_get_endpoints():
    endpoints = [
        '/organizations/',
        '/positions/',
        '/agents/',
        '/employees/',
        '/contracts/',
        '/insurance_cases/',
        '/user_profiles/'
    ]

    for endpoint in endpoints:
        response = requests.get(f'{BASE_URL}{endpoint}', headers=HEADERS)
        if response.status_code == 200:
            print(f"GET {endpoint} - SUCCESS ({len(response.json())} items)")
        else:
            print(f"GET {endpoint} - FAILED: {response.status_code}")


def test_post_endpoints():
    # Пример создания новой организации
    data = {
        "code": "ORG100",
        "full_name": "Test Insurance Co.",
        "short_name": "TestIns",
        "address": "100 Test St.",
        "bank_details": "IBAN100",
        "specialization": "Life Insurance"
    }
    response = requests.post(f'{BASE_URL}/organizations/', json=data, headers=HEADERS)
    if response.status_code == 201:
        print("POST /organizations/ - SUCCESS")
    else:
        print(f"POST /organizations/ - FAILED: {response.status_code} - {response.json()}")


def test_put_endpoints():
    # Получаем первую организацию
    response = requests.get(f'{BASE_URL}/organizations/', headers=HEADERS)
    if response.status_code == 200 and response.json():
        org_id = response.json()[0]['id']
        data = {
            "code": "ORG001-EDIT",
            "full_name": "Updated Alpha Insurance",
            "short_name": "AlphaUpdated",
            "address": "Updated Address",
            "bank_details": "IBAN-EDIT",
            "specialization": "Updated Auto Insurance"
        }
        response = requests.put(f'{BASE_URL}/organizations/{org_id}/', json=data, headers=HEADERS)
        if response.status_code == 200:
            print(f"PUT /organizations/{org_id}/ - SUCCESS")
        else:
            print(f"PUT /organizations/{org_id}/ - FAILED: {response.status_code} - {response.json()}")
    else:
        print("No organizations found for PUT test.")


def test_delete_endpoints():
    response = requests.get(f'{BASE_URL}/organizations/', headers=HEADERS)
    if response.status_code == 200 and response.json():
        org_id = response.json()[-1]['id']
        response = requests.delete(f'{BASE_URL}/organizations/{org_id}/', headers=HEADERS)
        if response.status_code == 204:
            print(f"DELETE /organizations/{org_id}/ - SUCCESS")
        else:
            print(f"DELETE /organizations/{org_id}/ - FAILED: {response.status_code}")
    else:
        print("No organizations found for DELETE test.")


if __name__ == '__main__':
    get_admin_token()
    test_get_endpoints()
    test_post_endpoints()
    test_put_endpoints()
    test_delete_endpoints()
