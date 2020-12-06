#!/usr/bin/env python3

import sys
import os.path

#import paho.mqtt.client as paho
import paho.mqtt.publish as publish

BROKER = "mqtt.eclipse.org"
MQTT_TOPIC = "eecs106a/stovebot/angle"

"""
Computer vision to retrieve angle turned on a specified image.
"""
def getAngle(file):
	return 0xDEADBEEF

def help():
	print("Usage: {} image_file".format(sys.argv[0]))

def main():
	if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
		help()
		return

	image_file = sys.argv[1]
	angleToTurn = getAngle(image_file)

	publish.single(MQTT_TOPIC, angleToTurn, hostname=BROKER)

if __name__ == "__main__":
	main()