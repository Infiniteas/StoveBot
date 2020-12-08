import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("eecs106a/stovebot/rightAngle")

def on_message(client, userdata, msg):
    print("Message received from " + msg.topic + " -> " + str(msg.payload))

client = mqtt.Client("stoveBotTestSubscriber")
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipse.org", 1883)
client.loop_forever()