import time
import paho.mqtt.client as mqtt

# Cayenne MQTT Credentials (replace with your real credentials from Cayenne dashboard)
CAYENNE_USERNAME = "your-username"
CAYENNE_PASSWORD = "your-password"
CAYENNE_CLIENT_ID = "your-client-id"

# MQTT Topics used by Cayenne
CONTROL_TOPIC = "v1/{}/things/{}/cmd/".format(CAYENNE_USERNAME, CAYENNE_CLIENT_ID)
DATA_TOPIC = "v1/{}/things/{}/data/1".format(CAYENNE_USERNAME, CAYENNE_CLIENT_ID)

# Sample device control function
def on_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"Message received on topic {message.topic}: {payload}")
    if "on" in payload.lower():
        print("Turning ON device")
    elif "off" in payload.lower():
        print("Turning OFF device")

# MQTT Connection Setup
client = mqtt.Client()
client.username_pw_set(CAYENNE_USERNAME, password=CAYENNE_PASSWORD)
client.on_message = on_message

client.connect("mqtt.mydevices.com", 1883, 60)
client.loop_start()

# Subscribe to command topic
client.subscribe(CONTROL_TOPIC + "#")

try:
    print("IoT Home Controller Running...")
    while True:
        # Publish dummy sensor data (0 or 1)
        value = int(time.time()) % 2
        client.publish(DATA_TOPIC, value)
        print(f"Published value: {value}")
        time.sleep(10)
except KeyboardInterrupt:
    print("Disconnected.")
    client.loop_stop()
    client.disconnect()
