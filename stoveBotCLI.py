"""
stoveBotCLI.py
Author: Bernard Chen
A quick and dirty CLI to interface directly with MQTT and CV components
of the stoveBot project.
"""

import sys
import os

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from stoveBotCV import *

BROKER = "broker.hivemq.com"
PORT = 1883
ANGLE_MQTT_TOPIC = "stoveBot/project/motor"

def subscriberLoop(topic):
	print("Press x then enter at any time to exit")

	def on_connect(client, userdata, flags, rc):
		print("Connected with result code {0}".format(str(rc)))
		client.subscribe(topic)

	def on_message(client, userdata, msg):
		print("Message received from " + msg.topic + " -> " + str(msg.payload))

	client = mqtt.Client("stoveBotCLISubscriber")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(BROKER, PORT)
	client.loop_start()

	while (1):
		command = input("")
		if (command == "x"):
			client.loop_stop()
			return

def publisherLoop():
	while (1):
		command = input("Enter [leftAngle] [rightAngle] on a single line or x to exit: ")
		if (command == "x"):
			return
		else:
			command = command.split()
			if (len(command) != 2 or not command[0].isdigit() or not command[1].isdigit()):
				print("Must enter \'[leftAngle] [rightAngle]\' as integers")
			else:
				publish.single(ANGLE_MQTT_TOPIC, command[1] + "," + command[0], hostname=BROKER)

def runCV(image):
	if not os.path.exists(image):
		print("Image does not exist")
		return

	leftAngle, rightAngle = cvAngles(image)

	if (leftAngle > 0):
		leftAngle -= 360
	leftAngle *= -1

	if (rightAngle > 0):
		rightAngle -= 360
	rightAngle *= -1

	print("Angles to turn off stove: ")
	print("leftAngle = {}, rightAngle = {}".format(leftAngle, rightAngle))

def main():
	print("StoveBot Command Line Interface Tool:")
	print("Commands:\tsubscribe [topic]")
	print("\t\tpublishAngle")
	print("\t\trunCV [image path]")
	print("\t\texit")
	while (1):
		command = input("\nEnter a command: ")
		if (len(command) > 8 and command[:9] == "subscribe"):
			if (len(command) < 11):
				print("subscribe requires a topic: subscribe [topic]")
				print("StoveBot currently uses:\t\'eecs106a/stovebot/images\'")
				print("\t\t\t\t\'stoveBot/project/motor\'")
			else:
				subscriberLoop(command[10:])
		elif (command == "publishAngle"):
			publisherLoop()
		elif (len(command) > 4 and command[:5] == "runCV"):
			if (len(command) < 7):
				print("runCV requires an image: runCV [image path]")
			else:
				runCV(command[6:])
		elif (command == "exit"):
			return
		else:
			print("Command not supported")

if __name__ == "__main__":
	main()