import requests
import re
import sys

BASE_URL = 'https://ekaaprasetya24.pythonanywhere.com'
SESSION = requests.Session()

def get_csrf_token(html):
    # Find csrf token input
    match = re.search(r'<input[^>]*name=\"csrf_token\"[^>]*value=\"([^\"]*)\"', html, re.IGNORECASE)
    if match:
        return match.group(1)
    # fallback: maybe token is in a meta tag? not needed
    return None

def login():
    login_url = f'{BASE_URL}/dashboard/login'
    # First get login page to obtain CSRF token
    r = SESSION.get(login_url)
    if r.status_code != 200:
        print(f'Failed to get login page: {r.status_code}')
        return False
    token = get_csrf_token(r.text)
    if not token:
        print('Could not find CSRF token in login page')
        return False
    # Perform login
    payload = {
        'username': 'admin',
        'password': 'admin',
        'csrf_token': token
    }
    r = SESSION.post(login_url, data=payload)
    # After login, we may be redirected to dashboard
    if r.status_code == 200 and 'Dashboard' in r.text:
        print('Login succeeded')
        return True
    else:
        # maybe redirect
        if r.status_code in (302, 303) and '/dashboard' in r.headers.get('Location', ''):
            print('Login succeeded (redirect)')
            return True
        print(f'Login failed: {r.status_code}')
        print(r.text[:500])
        return False

def get_projects_page():
    url = f'{BASE_URL}/dashboard/projects'
    r = SESSION.get(url)
    if r.status_code != 200:
        print(f'Failed to get projects page: {r.status_code}')
        return None
    return r.text

def delete_project(pid):
    # Need to get a fresh CSRF token from a page that includes the form (projects page)
    html = get_projects_page()
    if html is None:
        return False
    token = get_csrf_token(html)
    if not token:
        print('Could not find CSRF token in projects page')
        return False
    delete_url = f'{BASE_URL}/dashboard/project/delete/{pid}'
    payload = {
        'csrf_token': token
    }
    # Note: The form may have no other fields
    r = SESSION.post(delete_url, data=payload)
    if r.status_code in (200, 302):
        print(f'Delete request sent, status: {r.status_code}')
        # Optionally follow redirect and check for success message
        return True
    else:
        print(f'Delete failed: {r.status_code}')
        print(r.text[:500])
        return False

def main():
    if not login():
        sys.exit(1)
    # Optionally list projects to confirm
    html = get_projects_page()
    if html:
        # extract project titles maybe
        # simple regex for table rows? We'll just show that we got page
        print('Fetched projects page')
    # Delete project id 3 (as per URL earlier)
    if delete_project(3):
        print('Deletion request succeeded')
    else:
        print('Deletion request failed')
        sys.exit(1)

if __name__ == '__main__':
    main()
