# frontend/api_client.py

import requests

API_BASE_URL = "http://127.0.0.1:5000/api"
TOKEN = None
USER_ROLE = None

def set_auth(token, role):
    global TOKEN, USER_ROLE
    TOKEN = token
    USER_ROLE = role

def get_headers():
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers

def login_user(email, password):
    url = f"{API_BASE_URL}/auth/login"
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            set_auth(result['token'], result['role'])
            return result
        return {"error": response.json().get('error', 'Login failed.')}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

def signup_user(name, email, password):
    url = f"{API_BASE_URL}/auth/signup"
    data = {"name": name, "email": email, "password": password}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json()
        return {"error": response.json().get('error', 'Signup failed.')}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

def get_items(status=None):
    url = f"{API_BASE_URL}/items"
    if status:
        url += f"?status={status}"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException:
        return []

def get_categories():
    # Since we didn't create a separate categories route, mock the seeded data
    return [{'category_id': 1, 'name': 'Electronics'}, {'category_id': 2, 'name': 'ID/Documents'}, {'category_id': 3, 'name': 'Apparel/Clothing'}]

def report_item_api(report_data):
    url = f"{API_BASE_URL}/items"
    try:
        response = requests.post(url, json=report_data, headers=get_headers())
        if response.status_code == 201:
            return response.json()
        return {"error": response.json().get('error', 'Report failed.')}
    except requests.exceptions.RequestException:
        return {"error": "Network error or API offline."}