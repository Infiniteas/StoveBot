import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import os

from stoveBotCV import *

BROKER = "mqtt.eclipse.org"
IMAGE_MQTT_TOPIC = "eecs106a/stovebot/images"
LEFT_ANGLE_MQTT_TOPIC = "eecs106a/stovebot/leftAngle"
RIGHT_ANGLE_MQTT_TOPIC = "eecs106a/stovebot/rightAngle"

TMP_IMAGE = "/tmp/stovebot_tmp_img.jpg"

def publishLeftAngle(window):
	angle = window.getLeftAngle()
	publish.single(LEFT_ANGLE_MQTT_TOPIC, angle, hostname=BROKER)

def publishRightAngle(window):
	angle = window.getRightAngle()
	publish.single(RIGHT_ANGLE_MQTT_TOPIC, angle, hostname=BROKER)

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

		leftAngle, rightAngle = cv_real(TMP_IMAGE)

		# nonlocal test
		# if (test % 4 == 0):
		# 	leftAngle = 0
		# 	rightAngle = 30
		# test += 1

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
	os.remove(TMP_IMAGE)