import requests
import re
import sys

BASE_URL = 'https://ekaaprasetya24.pythonanywhere.com'
SESSION = requests.Session()
# Set a user-agent to mimic browser
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'})

def get_csrf_token(html):
    match = re.search(r'<input[^>]*name=\"csrf_token\"[^>]*value=\"([^\"]*)\"', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def login():
    login_url = f'{BASE_URL}/dashboard/login'
    # Get login page
    r = SESSION.get(login_url)
    if r.status_code != 200:
        print(f'Failed to get login page: {r.status_code}')
        return False
    token = get_csrf_token(r.text)
    if not token:
        print('Could not find CSRF token in login page')
        return False
    # Prepare payload with referer header
    headers = {'Referer': login_url}
    payload = {
        'username': 'admin',
        'password': 'admin',
        'csrf_token': token
    }
    r = SESSION.post(login_url, data=payload, headers=headers)
    # After login, we may be redirected to dashboard
    if r.status_code == 200 and 'Dashboard' in r.text:
        print('Login succeeded')
        return True
    if r.status_code in (302, 303):
        loc = r.headers.get('Location', '')
        if '/dashboard' in loc:
            print('Login succeeded (redirect)')
            return True
    print(f'Login failed: {r.status_code}')
    print(r.text[:500])
    return False

def get_csrf_from_page(url):
    r = SESSION.get(url)
    if r.status_code != 200:
        return None
    return get_csrf_token(r.text)

def delete_project(pid):
    # Get CSRF token from projects page
    token = get_csrf_from_page(f'{BASE_URL}/dashboard/projects')
    if not token:
        print('Could not get CSRF token from projects page')
        return False
    delete_url = f'{BASE_URL}/dashboard/project/delete/{pid}'
    headers = {'Referer': f'{BASE_URL}/dashboard/projects'}
    payload = {'csrf_token': token}
    r = SESSION.post(delete_url, data=payload, headers=headers)
    if r.status_code in (200, 302):
        print(f'Delete request sent, status: {r.status_code}')
        # Optionally check response for success message
        return True
    else:
        print(f'Delete failed: {r.status_code}')
        print(r.text[:500])
        return False

def main():
    if not login():
        sys.exit(1)
    if delete_project(3):
        print('Deletion request succeeded')
    else:
        print('Deletion request failed')
        sys.exit(1)

if __name__ == '__main__':
    main()
