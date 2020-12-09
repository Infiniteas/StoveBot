import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import os

from stoveBotCV import *

BROKER = "broker.hivemq.com"
IMAGE_MQTT_TOPIC = "eecs106a/stovebot/images"
ANGLE_MQTT_TOPIC = "stoveBot/project/motor"

TMP_IMAGE = "/tmp/stovebot_tmp_img.jpg"

def publishLeftAngle(window):
	angle = window.getLeftAngle()
	print("Turning off left stove with angle=" + str(angle) + "\n")
	publish.single(ANGLE_MQTT_TOPIC, str(angle) + ",0", hostname=BROKER)

def publishRightAngle(window):
	angle = window.getRightAngle()
	print("Turning off right stove with angle=" + str(angle) + "\n")
	publish.single(ANGLE_MQTT_TOPIC, "0," + str(angle), hostname=BROKER)

def startCVSubscriber(windowToUpdate):
	test = 0

	def on_connect(client, userdata, flags, rc):
		print("Connected with result code {0}".format(str(rc)))
		client.subscribe(IMAGE_MQTT_TOPIC)

	def on_message(client, userdata, msg):
		#print("Message received from " + msg.topic + " -> " + str(msg.payload))
		f = open(TMP_IMAGE, "w+b")
		f.write(msg.payload)
		f.close()

		leftAngle, rightAngle = cv_angles(TMP_IMAGE)
		print("Received image, CV returned left angle=" + str(leftAngle) +
			" right angle=" + str(rightAngle) + "\n")

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
	if os.path.exists(TMP_IMAGE):
		os.remove(TMP_IMAGE)