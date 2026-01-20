import board
import busio
import adafruit_bme680
import adafruit_mmc56x3
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = busio.I2C(board.SCL, board.SDA)

bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)
mag = adafruit_mmc56x3.MMC5603(i2c)
ads = ADS1115(i2c)

print("=== BME680 ===")
print(f"Temperature: {bme.temperature:.2f} C")
print(f"Humidity: {bme.relative_humidity:.2f} %")
print(f"Pressure: {bme.pressure:.2f} hPa")
print(f"Gas: {bme.gas:.0f} ohms")

print("\n=== MLX90393 ===")
x, y, z = mag.magnetic
print(f"X: {x:.2f} uT")
print(f"Y: {y:.2f} uT")
print(f"Z: {z:.2f} uT")

print("\n=== ADS1115 ===")
chan = AnalogIn(ads, ads1x15.Pin.A0)
print(f"A0 value: {chan.value}")
print(f"A0 Voltage: {chan.voltage}")
