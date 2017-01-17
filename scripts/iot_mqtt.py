import paho.mqtt.client as mqtt
import sqlite3
import time

MQTT_HOST = "localhost"
MQTT_PASS = "yt#ua4dhfsWN"
MQTT_USERNAME = "co657_5"
DB_NAME = "co657.db"
TOPICS = {
    "/temp/live": "temp_live",
    "/temp/rolling": "temp_rolling",
    "/hum/live": "hum_live",
    "/hum/rolling": "hum_rolling"
}

"""
static mqtt_topics_t mqtt_topics = {
    temperature_live: "/temp/live",
    temperature_rolling: "/temp/rolling",
    temperature_max: "/temp/max",
    temperature_min: "/temp/min",
    humidity_live: "/hum/live",
    humidity_rolling: "/hum/rolling",
    humidity_max: "/hum/max",
    humidity_min: "/hum/min",
    commands: "/cmd"
};
"""


def on_connect(client: mqtt.Client, userdata, flags, rc):
    cursor = db_conn.cursor()
    for topic, table_name in TOPICS.items():
        client.subscribe(topic)
        cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (read_at INT, payload REAL)")


def on_message(client, userdata, msg):
    cmd = "INSERT INTO " + TOPICS[str(msg.topic)] + " VALUES (?, ?)"
    db_conn.cursor().execute(cmd, ((int(time.time())), msg.payload.decode()))
    db_conn.commit()
    print("%s: %f" % (msg.topic, float(msg.payload)))


db_conn = sqlite3.connect(DB_NAME)

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST)

client.loop_forever()
