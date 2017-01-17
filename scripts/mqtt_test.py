import paho.mqtt.client as mqtt
import sqlite3
import time


def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code: %s" % str(rc))
    client.subscribe("test")
    cursor = db_conn.cursor()
    cursor.execute("DROP TABLE test")
    cursor.execute("CREATE TABLE test (read_at int, payload real)")


def on_message(client, userdata, msg):
    cmd = "INSERT INTO test VALUES (?, ?)"
    db_conn.cursor().execute(cmd, ((int(time.time())), msg.payload.decode()))
    db_conn.commit()
    print("%s: %f" % (msg.topic, float(msg.payload)))


db_conn = sqlite3.connect("test.db")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost")

client.loop_forever()
