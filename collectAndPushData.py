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
import tldevice

i2c = busio.I2C(board.SCL, board.SDA)
#i2c devices
bme = adafruit_bme680.Adafruit_BME680_I2C(i2c) #bme 1 is by the MOT stand
bme.gas_heater_enable = False
bme2 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76) #bme2 is mobile via ethernet cable
bme2.gas_heater_enable = False
#mag = adafruit_mmc56x3.MMC5603(i2c)
ads = ADS1115(i2c)

twinleafFlag = 1 # 1 means use twinleaf

#twinleaf magetometer or adafruit
try:
    tl = tldevice.Device(os.path.realpath('/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03Z0A5-if00-port0'))
    row = next(tl.data.iter())
    magXYZ = (row[0]/1000, row[1]/1000, row[2]/1000)  # nT -> uT
except Exception as e:
    print(f'{datetime.now().isoformat()} Twinleaf read failed: {e}')
    magXYZ = None

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

    chan = AnalogIn(ads, ads1x15.Pin.A0)
    igPressure = 10**((chan.voltage*4)-11)

    entry = {
        'time': datetime.now().isoformat(timespec='seconds'),
        'temp': round(bme.temperature, 1),
        'humidity': round(bme.relative_humidity, 2),
        'ambientPressure': round(bme.pressure, 1),
        'gas': round(bme.gas, 1),
        'temp2': round(bme2.temperature, 1),
        'humidity2': round(bme2.relative_humidity, 2),
        'igPressure': float(f'{igPressure:.4g}'),
    }
    if magXYZ:
        entry.update(magX=round(magXYZ[0], 3), magY=round(magXYZ[1], 3), magZ=round(magXYZ[2], 3))

    data.append(entry)
    data = data[-1152:]

    status = push_data(data, sha)
    print(f'Push status: {status}')
