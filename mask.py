import cv2
import numpy as np
from sklearn.cluster import KMeans
import time

def auto_canny(image, sigma=0.33):

	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

image = cv2.imread('./maxres.jpg')

cv2.imshow("image", image)

r = 600.0/image.shape[1]
dim = (600, int(image.shape[0]*r))

image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("resized", image)

laplacian = cv2.filter2D(image_gray,-1,np.array((
	[0, 1, 0],
	[1, -4, 1],
	[0, 1, 0]), dtype="int"))
cv2.imshow("laplacian",laplacian)

image=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
cv2.imshow("colorized",image)

#image[:,:,1] = 255*np.ones((image.shape[0],image.shape[1]))

#color stuff
lower_red = np.array([0,0,50])
upper_red = np.array([80,80,255])

mask = cv2.inRange(image, lower_red, upper_red)
cv2.imshow('mask',mask)
res = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow('res', res)

#image[:,:,2] = 255*np.ones((image.shape[0],image.shape[1]))

#image = cv2.blur(image,(15,15))
image=cv2.GaussianBlur(image,(5,5),0)
#image=cv2.medianBlur(image,5)
cv2.imshow("blurred",image)

vector = image.reshape((-1,3))
vector = np.float32(vector)

print(vector.shape)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

K = 2 
attempts=10

ret,label,center=cv2.kmeans(vector,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
center = np.uint8(center)
print(center)

res = center[label.flatten()]
result = res.reshape((image.shape))

cv2.imshow("clustered",result)

cv2.waitKey(0)
