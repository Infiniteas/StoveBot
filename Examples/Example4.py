# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:39:48 2020

@author: janic
"""
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

# read the input image
img_base = cv2.imread("./images/doublebase.jpg")
img_rot = cv2.imread("./images/double4.jpg")

#     *********************************    
#     *                               *
#     *   Detects Circles in Images   *
#     *                               *
#     *********************************

img = cv2.imread("./images/double4.jpg", cv2.IMREAD_COLOR) 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
output = img.copy()

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3))
  
# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT,1,40,
                                    param1=50,param2=30,minRadius=295,maxRadius=300)
origin_l = []
origin_r = [] 
# Draw circles that are detected. 
if detected_circles is not None: 
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles))
    
#     *********************************    
#     *                               *
#     *        for Debugging          *
#     *                               *
#     *********************************
    
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
      
        # Draw the circumference of the circle. 
        cv2.circle(img, (a, b), r, (0, 255, 0), 5)
        
#    print("shape", detected_circles.shape)
#    x, y, z = detected_circles.shape
#    print("x ", x, " y ", y, " z ", z)

    
    if detected_circles[0][0][0] < 1000:
        xl, yl, rl = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
        xr, yr, rr = detected_circles[0][1][0], detected_circles[0][1][1], detected_circles[0][1][2]
    else:
        xr, yr, rr = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
        xl, yl, rl = detected_circles[0][1][0], detected_circles[0][1][1], detected_circles[0][1][2]
    
    origin_l = np.array([xl, yl, 1])
    origin_r = np.array([xr, yr, 1])
    print("origin_l ", origin_l)
    print("origin_r ", origin_r)
        
    # Draw the circumference of the circle. 
    cv2.circle(img_rot, (xr, yr), rr, (0, 0, 255), 5)
    cv2.circle(img_rot, (xl, yl), rl, (0, 0, 255), 5)
        
plt.imshow(img),plt.show()

#     *********************************    
#     *                               *
#     *    Applies Filter on Image    *
#     *                               *
#     *********************************

img_base_hsv = cv2.cvtColor(img_base, cv2.COLOR_BGR2HSV)

# find HSV using BGR
blue = np.uint8([[[226,211,99]]])
#print(cv2.cvtColor(pink,cv2.COLOR_BGR2HSV))
blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)

# define range of pink color in HSV
# (H - 10, 100, 100)
# (H + 10, 255, 255)
lower_blue = np.array([blue[0][0][0] - 10,100,100])
upper_blue = np.array([blue[0][0][0] + 10,255,255])

# Threshold the HSV image to get only pink colors
mask_base_blue = cv2.inRange(img_base_hsv, lower_blue, upper_blue)

# Bitwise-AND mask and rotated image
res_base_blue = cv2.bitwise_and(img_base,img_base, mask=mask_base_blue)
res_base_blue = cv2.cvtColor(res_base_blue, cv2.COLOR_BGR2RGB)

# make copys of the results to display them
filtered_base_blue = res_base_blue.copy()

cv2.putText(filtered_base_blue, "Filtered Base Blue", (400, 800),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (255, 255, 255), 5)
plt.imshow(filtered_base_blue),plt.show()

################################################################################

img_rot_hsv = cv2.cvtColor(img_rot, cv2.COLOR_BGR2HSV)

# find HSV using BGR
blue = np.uint8([[[226,211,99]]])
#print(cv2.cvtColor(pink,cv2.COLOR_BGR2HSV))
blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)

# define range of pink color in HSV
# (H - 10, 100, 100)
# (H + 10, 255, 255)
lower_blue = np.array([blue[0][0][0] - 10,100,100])
upper_blue = np.array([blue[0][0][0] + 10,255,255])

# Threshold the HSV image to get only pink colors
mask_rot_blue = cv2.inRange(img_rot_hsv, lower_blue, upper_blue)

# Bitwise-AND mask and rotated image
res_rot_blue = cv2.bitwise_and(img_rot,img_rot, mask=mask_rot_blue)
res_rot_blue = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2RGB)

# make copys of the results to display them
filtered_rot_blue = res_rot_blue.copy()

cv2.putText(filtered_rot_blue, "Filtered Rotated Blue", (500, 800),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (255, 255, 255), 5)
plt.imshow(filtered_rot_blue),plt.show()


#     *********************************    
#     *                               *
#     *    Finds Center of Shape      *
#     *                               *
#     *********************************

# Calculate the center of the shape after filter is applied
gray_base = cv2.cvtColor(res_base_blue, cv2.COLOR_BGR2GRAY)
blurred_base = cv2.GaussianBlur(gray_base, (5, 5), 0)
thresh_base = cv2.threshold(blurred_base, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the binary image
contours_base, hierarchy = cv2.findContours(thresh_base,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

base_pt_l  = []
base_pt_r = []

for c in contours_base:
    # calculate moments for each contour
    M = cv2.moments(c)
    
    # calculate x,y coordinate of center
    if M["m00"] != 0:
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
    else:
     cX, cY = 0, 0
    cv2.circle(img_rot, (cX, cY), 5, (255, 255, 255), 10)
    #print("rot center:", cX, cY)
    t = np.array([(cX - a), -1*(cY - b), 0])
    if cX < 1000: #left side 
        base_pt_l = np.array([cX, cY, 1])
        cv2.putText(img_rot, "base_l", (cX - 50, cY - 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)

        #print("base_l ", base_pt_l)
    else: #right side
        base_pt_r = np.array([cX, cY, 1])
        cv2.putText(img_rot, "base_r", (cX - 50, cY - 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)

        #print("base_r ", base_pt_r)

# Calculate the center of the shape after filter is applied
gray_rot = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2GRAY)
blurred_rot = cv2.GaussianBlur(gray_rot, (5, 5), 0)
thresh_rot = cv2.threshold(blurred_rot, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the binary image
contours_rot, hierarchy = cv2.findContours(thresh_rot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

rot_pt_l  = []
rot_pt_r = []

for c in contours_rot:
    # calculate moments for each contour
    M = cv2.moments(c)
    
    # calculate x,y coordinate of center
    if M["m00"] != 0:
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
    else:
     cX, cY = 0, 0
    cv2.circle(img_rot, (cX, cY), 5, (255, 255, 255), 10)
    #print("rot center:", cX, cY)
    if cX < 1000:
        rot_pt_l = np.array([cX, cY, 1])
        cv2.putText(img_rot, "rot_l", (cX - 50, cY - 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
        #print("rot_l ", rot_pt_l)
    else:
        rot_pt_r = np.array([cX, cY, 1])
        cv2.putText(img_rot, "rot_r", (cX - 50, cY - 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
        #print("rot_r ", rot_pt_r)


print("base_l ", base_pt_l)
print("base_r ", base_pt_r)
print("rot_l ", rot_pt_l)
print("rot_r ", rot_pt_r)

#     *********************************    
#     *                               *
#     *       Calculates Angle        *
#     *                               *
#     *********************************

#TODO: check the point vaaaalluuuesss
omega = np.array([0, 0, 1])
#w = np.array([0, 1, 0])

u_pt_l = base_pt_l - origin_l
v_pt_l = rot_pt_l - origin_l

print("u_pt_l", u_pt_l)
print("v_pt_l", v_pt_l)


#u_prime_l = u_pt_l - np.dot(omega, np.dot(np.transpose(omega),u_pt_l))
#v_prime_l = v_pt_l - np.dot(omega, np.dot(np.transpose(omega),v_pt_l))

#print("u_prime_l", u_prime_l)
#print("v_prime_l", v_prime_l)

y = np.dot(np.transpose(omega), np.cross(u_pt_l, v_pt_l))
x = np.dot(u_pt_l, v_pt_l)
theta = math.atan2(y, x)
degree_left = np.rad2deg(theta)
degree_left = '%1.0f' % (degree_left)
print("degree left: ", degree_left)

u_pt_r = base_pt_r - origin_r
v_pt_r = rot_pt_r - origin_r

print("u_pt_r", u_pt_r)
print("v_pt_r", v_pt_r)

#u_prime_r = u_pt_r - np.dot(omega, np.dot(np.transpose(omega),u_pt_r))
#v_prime_r = v_pt_r - np.dot(omega, np.dot(np.transpose(omega),v_pt_r))

#print("u_prime_r", u_prime_r)
#print("v_prime_r", v_prime_r)

y = np.dot(np.transpose(omega), np.cross(u_pt_r, v_pt_r))
x = np.dot(u_pt_r, v_pt_r)
theta = math.atan2(y, x)
degree_right = np.rad2deg(theta)
degree_right = '%1.0f' % (degree_right)
print("degree right: ", degree_right)

cv2.putText(img_rot, degree_left, (xl + 20, yl),cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 0, 0), 4)
cv2.putText(img_rot, degree_right, (xr + 20, yr),cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 0, 0), 4)

# convert from BGR to RGB so we can plot using matplotlib
img_rot = cv2.cvtColor(img_rot, cv2.COLOR_BGR2RGB)
plt.imshow(img_rot),plt.show()
