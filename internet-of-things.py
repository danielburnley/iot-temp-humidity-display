import sqlite3
import time

import math
from flask import Flask, jsonify
import copy

DATABASE_NAME = "test.db"
DATABASE = sqlite3.connect(DATABASE_NAME)
app = Flask(__name__)


def get_cursor():
    return DATABASE.cursor()


def get_readings_from_last_hour(table):
    c = get_cursor()
    results = []
    timestamp = int(time.time()) - (60 * 60)  # number of seconds in an hour
    for row in c.execute("SELECT * FROM " + table + " WHERE read_at > ? ORDER BY read_at DESC", (timestamp,)):
        results.append(result_to_data(row))
    return results


def result_to_data(row):
    return {"time": row[0], "data": row[1]}


def generate_rolling_average(raw_results):
    rolled_results = []
    for i in range(5, len(raw_results)):
        result = copy.copy(raw_results[i])
        data = [r["data"] for r in raw_results[i - 5:i]]
        result["data"] = sum(data) / len(data)
        rolled_results.append(result)
    return rolled_results


def get_average(data):
    readings = [item["data"] for item in data]
    return math.ceil((sum(readings) / len(readings)) * 10) / 10


@app.route("/api/get/overview")
def get_overview():
    raw_temperature = get_readings_from_last_hour("temperature")
    raw_humidity = get_readings_from_last_hour("humidity")
    avg_temperature = get_average(raw_temperature)
    avg_humidity = get_average(raw_humidity)
    return jsonify({
        "latest_temperature": raw_temperature[0]["data"],
        "average_temperature": avg_temperature,
        "latest_humidity": raw_humidity[0]["data"],
        "average_humidity": avg_humidity
    })


@app.route("/api/get/hum/hour/raw")
def get_raw_hum_readings_from_last_hour():
    return jsonify(get_readings_from_last_hour("humidity"))


@app.route("/api/get/hum/hour/rolling")
def get_rolling_hum_from_last_hour():
    raw_results = get_readings_from_last_hour("humidity")
    rolled_results = generate_rolling_average(raw_results)
    return jsonify(rolled_results)


@app.route("/api/get/temp/hour/raw")
def get_raw_temp_readings_from_last_hour():
    return jsonify(get_readings_from_last_hour("temperature"))


@app.route("/api/get/temp/hour/rolling")
def get_rolling_temp_from_last_hour():
    raw_results = get_readings_from_last_hour("temperature")
    rolled_results = generate_rolling_average(raw_results)
    return jsonify(rolled_results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
