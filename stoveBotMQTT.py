import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from stoveBotCV import *

BROKER = "mqtt.eclipse.org"
IMAGE_MQTT_TOPIC = "eecs106a/stovebot/images"
LEFT_ANGLE_MQTT_TOPIC = "eecs106a/stovebot/leftAngle"
RIGHT_ANGLE_MQTT_TOPIC = "eecs106a/stovebot/rightAngle"

def publishLeftAngle(angle):
	publish.single(LEFT_ANGLE_MQTT_TOPIC, angle, hostname=BROKER)

def publishRightAngle(angle):
	publish.single(RIGHT_ANGLE_MQTT_TOPIC, angle, hostname=BROKER)

def startCVSubscriber(windowToUpdate):
	test = 0

	def on_connect(client, userdata, flags, rc):
		print("Connected with result code {0}".format(str(rc)))
		client.subscribe(IMAGE_MQTT_TOPIC)

	def on_message(client, userdata, msg):
		#print("Message received from " + msg.topic + " -> " + str(msg.payload))
		leftAngle, rightAngle = cv_test("test string")

		nonlocal test
		if (test % 4 == 0):
			leftAngle = 0
			rightAngle = 30
		test += 1

		windowToUpdate.updateLeftDial.emit(leftAngle)
		windowToUpdate.updateRightDial.emit(rightAngle)

	client = mqtt.Client("stoveBotCVSubscriber")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(BROKER, 1883)
	client.loop_start()

	return client

def stopCVSubscriber(client):
	client.loop_stop()