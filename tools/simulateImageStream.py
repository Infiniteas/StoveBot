#!/usr/bin/env python3

import sys
import time
import os.path

import paho.mqtt.publish as publish

BROKER = "broker.hivemq.com"
MQTT_TOPIC = "eecs106a/stovebot/images"

def help():
	print("Usage: {} interval image_file num_times [image_file num_times ... ]".format(sys.argv[0]))
	print("Will publish specified [image_file](s) every [interval] seconds. [num_times] represents " +
		"the number of times the [image_file] will be published")

def verify_args(interval, images, num_times):
	if (not (isinstance(interval, str) and interval.isdigit())):
		print("Interval must be a positive integer")
		return False

	for image in images:
		if (not (isinstance(image,str) and os.path.isfile(image))):
			print("File " + image + " does not exist")
			return False

	for num_times in num_times:
		if (not (isinstance(num_times, str) and num_times.isdigit())):
			print("num_times must be a positive integer")
			return False

	return True

def main():
	if (len(sys.argv) < 4 or len(sys.argv) % 2 != 0):
		help()
		return

	interval = sys.argv[1]
	images = sys.argv[2::2]
	num_times = sys.argv[3::2]
	
	if (not verify_args(interval, images, num_times)):
		help()
		return

	for i in range(len(images)):
		image = open(images[i], "rb")
		imageString = image.read()
		byteArray = bytes(imageString)

		for j in range(int(num_times[i])):
			publish.single(MQTT_TOPIC, byteArray, hostname=BROKER)
			print("Sent " + images[i] + " x" + str(j + 1))
			if (j != int(num_times[i]) - 1):
				time.sleep(int(interval))

	print("\"Playback\" complete")

if __name__ == "__main__":
	main()