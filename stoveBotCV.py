# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:39:48 2020

@author: Jasmine Anica
"""
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

BASE_IMG_PATH = "./Examples/images/stovebot-base.jpg"

def cvAngles(image_path):
	# read the input image
	img_base = cv2.imread(BASE_IMG_PATH)
	img_rot = cv2.imread(image_path)

	y_res, x_res, _ = img_rot.shape


	#     *********************************
	#     *                               *
	#     *    Applies Filter on Image    *
	#     *                               *
	#     *      Base and Rot points      *
	#     *                               *
	#     *********************************

	############## BASE POINTS ################

	img_base_hsv = cv2.cvtColor(img_base, cv2.COLOR_BGR2HSV)

	# find HSV using BGR
	blue = np.uint8([[[227,168,0]]])
	blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)

	# find HSV using BGR
	green = np.uint8([[[94,158,97]]])
	green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	# (H - 10, 100, 100)
	# (H + 10, 255, 255)
	lower_blue = np.array([blue[0][0][0] - 10,100,100])
	upper_blue = np.array([blue[0][0][0] + 10,255,255])

	# define range of dark blue color in HSV
	# (H - 10, 100, 100)
	# (H + 10, 255, 255)
	lower_green = np.array([green[0][0][0] - 10,100,100])
	upper_green = np.array([green[0][0][0] + 10,255,255])

	# Threshold the HSV image to get only blue colors
	mask_base_blue = cv2.inRange(img_base_hsv, lower_blue, upper_blue)
	mask_base_green = cv2.inRange(img_base_hsv, lower_green, upper_green)

	# Bitwise-AND mask and rotated image
	res_base_blue = cv2.bitwise_and(img_base,img_base, mask=mask_base_blue)
	res_base_blue = cv2.cvtColor(res_base_blue, cv2.COLOR_BGR2RGB)

	res_base_green = cv2.bitwise_and(img_base,img_base, mask=mask_base_green)
	res_base_green = cv2.cvtColor(res_base_green, cv2.COLOR_BGR2RGB)

	# make copys of the results to display them
	# filtered_base_blue = res_base_blue.copy()
	# filtered_base_green = res_base_green.copy()

	# plt.title("Filtered Base Blue")
	# plt.axis('off')
	# plt.imshow(filtered_base_blue),plt.show()
	# plt.title("Filtered Base Green")
	# plt.axis('off')
	# plt.imshow(filtered_base_green),plt.show()

	############## ROTATED POINTS ################

	img_rot_hsv = cv2.cvtColor(img_rot, cv2.COLOR_BGR2HSV)

	# find HSV using BGR
	blue = np.uint8([[[227,168,0]]])
	blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)

	# find HSV using BGR
	green = np.uint8([[[94,158,97]]])
	green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	# (H - 10, 100, 100)
	# (H + 10, 255, 255)
	lower_blue = np.array([blue[0][0][0] - 10,100,100])
	upper_blue = np.array([blue[0][0][0] + 10,255,255])

	# define range of dark blue color in HSV
	# (H - 10, 100, 100)
	# (H + 10, 255, 255)
	lower_green = np.array([green[0][0][0] - 10,100,100])
	upper_green = np.array([green[0][0][0] + 10,255,255])

	# Threshold the HSV image to get only blue colors
	mask_rot_blue = cv2.inRange(img_rot_hsv, lower_blue, upper_blue)
	mask_rot_green = cv2.inRange(img_rot_hsv, lower_green, upper_green)

	# Bitwise-AND mask and rotated image
	res_rot_blue = cv2.bitwise_and(img_rot,img_rot, mask=mask_rot_blue)
	res_rot_blue = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2RGB)

	res_rot_green = cv2.bitwise_and(img_rot,img_rot, mask=mask_rot_green)
	res_rot_green = cv2.cvtColor(res_rot_green, cv2.COLOR_BGR2RGB)

	# make copys of the results to display them
	# filtered_rot_blue = res_rot_blue.copy()
	# filtered_rot_green = res_rot_green.copy()

	# plt.title("Filtered Rot Blue")
	# plt.axis('off')
	# plt.imshow(filtered_rot_blue),plt.show()
	# plt.title("Filtered Rot Green")
	# plt.axis('off')
	# plt.imshow(filtered_rot_green),plt.show()

	#     *********************************
	#     *                               *
	#     *    Applies Filter on Image    *
	#     *                               *
	#     *            Origin             *
	#     *                               *
	#     *********************************

	# find HSV using BGR
	orange = np.uint8([[[76,122,206]]])
	orange = cv2.cvtColor(orange,cv2.COLOR_BGR2HSV)

	# define range of orange color in HSV
	# (H - 10, 100, 100)
	# (H + 10, 255, 255)
	lower_orange = np.array([orange[0][0][0] - 10,100,100])
	upper_orange = np.array([orange[0][0][0] + 10,255,255])

	# Threshold the HSV image to get only blue colors
	mask_base_orange = cv2.inRange(img_base_hsv, lower_orange, upper_orange)

	# Bitwise-AND mask and rotated image
	res_base_orange = cv2.bitwise_and(img_base,img_base, mask=mask_base_orange)
	res_base_orange = cv2.cvtColor(res_base_orange, cv2.COLOR_BGR2RGB)

	# make copys of the results to display them
	# filtered_base_orange = res_base_orange.copy()

	# plt.title("Filtered Base Orange")
	# plt.axis('off')
	# plt.imshow(filtered_base_orange),plt.show()

	#     *********************************
	#     *                               *
	#     *    Finds Center of Base       *
	#     *                               *
	#     *********************************

	# Calculate the center of the shape after filter is applied
	gray_base = cv2.cvtColor(res_base_blue, cv2.COLOR_BGR2GRAY)
	blurred_base = cv2.GaussianBlur(gray_base, (5, 5), 0)
	thresh_base = cv2.threshold(blurred_base, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the binary image
	contours_base, hierarchy = cv2.findContours(thresh_base,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# calculate moments for each contour
	M = cv2.moments(contours_base[0])

	# calculate x,y coordinate of center
	if M["m00"] != 0:
	 cX = int(M["m10"] / M["m00"])
	 cY = int(M["m01"] / M["m00"])
	else:
	 cX, cY = 0, 0
	cv2.circle(img_base, (cX, cY), 2, (255, 255, 255), 2)
	cv2.putText(img_base, "base_l", (cX - 15, cY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	base_pt_l = np.array([cX, cY, 1])

	# Calculate the center of the shape after filter is applied
	gray_base = cv2.cvtColor(res_base_green, cv2.COLOR_BGR2GRAY)
	blurred_base = cv2.GaussianBlur(gray_base, (5, 5), 0)
	thresh_base = cv2.threshold(blurred_base, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the binary image
	contours_base, hierarchy = cv2.findContours(thresh_base,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# calculate moments for each contour
	M = cv2.moments(contours_base[0])

	# calculate x,y coordinate of center
	if M["m00"] != 0:
	 cX = int(M["m10"] / M["m00"])
	 cY = int(M["m01"] / M["m00"])
	else:
	 cX, cY = 0, 0
	cv2.circle(img_base, (cX, cY), 2, (255, 255, 255), 2)
	cv2.putText(img_base, "base_r", (cX - 15, cY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	base_pt_r = np.array([cX, cY, 1])


	#     *********************************
	#     *                               *
	#     *   Finds Center of Rotated     *
	#     *                               *
	#     *********************************

	# Calculate the center of the shape after filter is applied
	gray_rot = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2GRAY)
	blurred_rot = cv2.GaussianBlur(gray_rot, (5, 5), 0)
	thresh_rot = cv2.threshold(blurred_rot, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the binary image
	contours_rot, hierarchy = cv2.findContours(thresh_rot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# calculate moments for each contour
	M = cv2.moments(contours_rot[0])

	# calculate x,y coordinate of center
	if M["m00"] != 0:
	 cX = int(M["m10"] / M["m00"])
	 cY = int(M["m01"] / M["m00"])
	else:
	 cX, cY = 0, 0
	#cv2.circle(img_base, (cX, cY), 2, (255, 255, 255), 2)
	#cv2.putText(img_base, "rot_l", (cX - 15, cY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	cv2.circle(img_rot, (cX, cY), 2, (255, 255, 255), 2)
	cv2.putText(img_rot, "rot_l", (cX - 15, cY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	rot_pt_l = np.array([cX, cY, 1])


	# Calculate the center of the shape after filter is applied
	gray_rot = cv2.cvtColor(res_rot_green, cv2.COLOR_BGR2GRAY)
	blurred_rot = cv2.GaussianBlur(gray_rot, (5, 5), 0)
	thresh_rot = cv2.threshold(blurred_rot, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the binary image
	contours_rot, hierarchy = cv2.findContours(thresh_rot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# calculate moments for each contour
	M = cv2.moments(contours_rot[0])

	# calculate x,y coordinate of center
	if M["m00"] != 0:
	 cX = int(M["m10"] / M["m00"])
	 cY = int(M["m01"] / M["m00"])
	else:
	 cX, cY = 0, 0
	#cv2.circle(img_base, (cX, cY), 2, (255, 255, 255), 2)
	#cv2.putText(img_base, "rot_r", (cX - 15, cY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	cv2.circle(img_rot, (cX, cY), 2, (255, 255, 255), 2)
	cv2.putText(img_rot, "rot_l", (cX - 15, cY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	rot_pt_r = np.array([cX, cY, 1])

	#     *********************************
	#     *                               *
	#     *    Finds Center of Origin     *
	#     *                               *
	#     *********************************

	# Calculate the center of the shape after filter is applied
	gray_base = cv2.cvtColor(res_base_orange, cv2.COLOR_BGR2GRAY)
	blurred_base = cv2.GaussianBlur(gray_base, (5, 5), 0)
	thresh_base = cv2.threshold(blurred_base, 60, 255, cv2.THRESH_BINARY)[1]
	# find contours in the binary image
	contours_base, hierarchy = cv2.findContours(thresh_base,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	for c in contours_base:
		# calculate moments for each contour
		M = cv2.moments(c)

		# calculate x,y coordinate of center
		if M["m00"] != 0:
		 cX = int(M["m10"] / M["m00"])
		 cY = int(M["m01"] / M["m00"])
		else:
		 cX, cY = 0, 0
		cv2.circle(img_base, (cX, cY), 2, (255, 255, 255), 2)

		if cX < (x_res // 2): #left side
			origin_l = np.array([cX, cY, 1])
			cv2.putText(img_base, "origin_l", (cX - 20, cY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

		else: #right side
			origin_r = np.array([cX, cY, 1])
			cv2.putText(img_base, "origin_r", (cX - 20, cY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

	# convert from BGR to RGB so we can plot using matplotlib
	img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2RGB)
	# plt.title("Base Points")
	# plt.axis('off')
	# plt.imshow(img_base),plt.show()

	# # convert from BGR to RGB so we can plot using matplotlib
	# img_rot = cv2.cvtColor(img_rot, cv2.COLOR_BGR2RGB)
	# plt.title("Rot Points")
	# plt.axis('off')
	# plt.imshow(img_rot),plt.show()

	#     *********************************
	#     *                               *
	#     *       Calculates Angle        *
	#     *                               *
	#     *********************************

	omega = np.array([0, 0, 1])

	u_pt_l = base_pt_l - origin_l
	v_pt_l = rot_pt_l - origin_l

	y = np.dot(np.transpose(omega), np.cross(u_pt_l, v_pt_l))
	x = np.dot(u_pt_l, v_pt_l)
	theta = math.atan2(y, x)
	degree_left = np.rad2deg(theta)
	#degree_left = '%1.0f' % (degree_left)

	u_pt_r = base_pt_r - origin_r
	v_pt_r = rot_pt_r - origin_r

	y = np.dot(np.transpose(omega), np.cross(u_pt_r, v_pt_r))
	x = np.dot(u_pt_r, v_pt_r)
	theta = math.atan2(y, x)
	degree_right = np.rad2deg(theta)
	#degree_right = '%1.0f' % (degree_right)

	return (int) (degree_left), (int) (degree_right)