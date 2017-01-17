import sqlite3
import time
from random import uniform
import math

MAX_HUMIDITY_CHANGE = 1
MAX_TEMP_CHANGE = 1
START_EPOCH = int(time.time()) - (60 * 60 * 24 * 3)
END_EPOCH = int(time.time())
TIME_DIFFERENCE = 30
MIN_TEMP = 10
MAX_TEMP = 25
MIN_HUM = 20
MAX_HUM = 70


def get_temp(previous_temp):
    if previous_temp == MIN_TEMP:
        temp = (uniform(MIN_TEMP, MIN_TEMP + MAX_TEMP_CHANGE))
    elif previous_temp == MAX_TEMP:
        temp = (uniform(MAX_TEMP - MAX_TEMP_CHANGE, MAX_TEMP))
    else:
        temp = (uniform(previous_temp - MAX_TEMP_CHANGE, previous_temp + MAX_TEMP_CHANGE))
    if temp > MAX_TEMP:
        temp = MAX_TEMP
    elif temp < MIN_TEMP:
        temp = MIN_TEMP
    return math.ceil((temp * 10)) / 10


def get_hum(previous_hum):
    if previous_hum == MIN_HUM:
        hum = (uniform(MIN_HUM, MIN_HUM + MAX_HUMIDITY_CHANGE))
    elif previous_hum == MAX_HUM:
        hum = (uniform(MAX_HUM - MAX_HUMIDITY_CHANGE, MAX_HUM))
    else:
        hum = (uniform(previous_hum - MAX_HUMIDITY_CHANGE, previous_hum + MAX_HUMIDITY_CHANGE))
    if hum > MAX_HUM:
        hum = MAX_HUM
    elif hum < MIN_HUM:
        hum = MIN_HUM
    return math.ceil((hum * 10)) / 10


db_conn = sqlite3.connect("test.db")
c = db_conn.cursor()
c.execute("CREATE TABLE temperature (read_at INT PRIMARY KEY, value REAL)")
c.execute("CREATE TABLE humidity (read_at INT PRIMARY KEY, value REAL)")

print("Generating %d data points" % ((END_EPOCH - START_EPOCH) / TIME_DIFFERENCE))
temperature = 10
humidity = 20
for i in range(START_EPOCH, END_EPOCH, TIME_DIFFERENCE):
    humidity = get_hum(humidity)
    temperature = get_temp(temperature)
    c.execute("INSERT INTO temperature VALUES (?, ?)", (i, temperature))
    c.execute("INSERT INTO humidity VALUES (?, ?)", (i, humidity))

db_conn.commit()
db_conn.close()
