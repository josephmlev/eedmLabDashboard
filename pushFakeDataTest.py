import requests
import json
import base64
from datetime import datetime
import random
import time
import os

GITHUB_TOKEN = "token here!!!"

REPO = 'josephmlev/eedmLabDashboard'
FILE_PATH = 'data.json'

def get_file():
    url = f'https://api.github.com/repos/{REPO}/contents/{FILE_PATH}'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = base64.b64decode(r.json()['content']).decode()
        return json.loads(content), r.json()['sha']
    return [], None

def push_data(data, sha):
    url = f'https://api.github.com/repos/{REPO}/contents/{FILE_PATH}'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    payload = {
        'message': 'sensor update',
        'content': base64.b64encode(json.dumps(data, indent=2).encode()).decode(),
    }
    if sha:
        payload['sha'] = sha
    r = requests.put(url, json=payload, headers=headers)
    return r.status_code

# Test with fake readings
if __name__ == '__main__':
    data, sha = get_file()
    
    # Simulate a new reading
    data.append({
        'time': datetime.now().isoformat(),
        'temp': 22 + random.random(),
        'pressure': 1010 + random.random() * 5,
        'v0': 3.3 + random.random() * 0.1,
        'v1': 2.0 + random.random() * 0.1
    })
    
    data = data[-2000:]  # keep last 2000 points
    
    status = push_data(data, sha)
    print(f'Push status: {status}')