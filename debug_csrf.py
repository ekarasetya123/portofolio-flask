import requests
import re

BASE_URL = 'https://ekaaprasetya24.pythonanywhere.com'
s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0'})
login_url = f'{BASE_URL}/dashboard/login'
r = s.get(login_url)
print('Login page status:', r.status_code)
token = re.search(r'<input[^>]*name=\"csrf_token\"[^>]*value=\"([^\"]*)\"', r.text, re.IGNORECASE)
if token:
    print('Login page token:', token.group(1))
else:
    print('No token in login page')
    # maybe token is in meta?
# login
payload = {'username':'admin','password':'admin','csrf_token':token.group(1) if token else ''}
r = s.post(login_url, data=payload, headers={'Referer':login_url})
print('Login post status:', r.status_code)
print('Login post URL:', r.url)
# get projects page
proj = s.get(f'{BASE_URL}/dashboard/projects')
print('Projects page status:', proj.status_code)
# find input
matches = re.findall(r'<input[^>]*name=\"csrf_token\"[^>]*value=\"([^\"]*)\"', proj.text, re.IGNORECASE)
print('Found token inputs:', len(matches))
if matches:
    print('First token:', matches[0])
# also show snippet
snippet = proj.text[proj.text.lower().find('csrf_token'):][:500]
print('Snippet around csrf:')
print(snippet)
