import requests
import json
import base64
from datetime import datetime
import random
import time
import os
import git_token as gt

import board
import busio
import adafruit_bme680
import adafruit_mmc56x3
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = busio.I2C(board.SCL, board.SDA)

bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)
mag = adafruit_mmc56x3.MMC5603(i2c)
ads = ADS1115(i2c)


GITHUB_TOKEN = gt.token

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





if __name__ == '__main__':
    data, sha = get_file()

    x, y, z = mag.magnetic
    chan = AnalogIn(ads, ads1x15.Pin.A0)
    igPressure = 10**((chan.voltage*4)-11)
    
    data.append({
        'time': datetime.now().isoformat(),
        'temp': bme.temperature,
        'humidity': bme.relative_humidity,
        'ambientPressure': bme.pressure,
        'gas': bme.gas,
        'magX': x,
        'magY': y,
        'magZ': z,
        'igPressure': igPressure
    })
    
    
    data = data[-20000:]  # keep last 20000 points
    
    status = push_data(data, sha)
    print(f'Push status: {status}')
