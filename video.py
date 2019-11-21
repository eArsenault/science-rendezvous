import cv2
import numpy as np
import matplotlib.pyplot as plt

## LOAD IMAGE

cap = cv2.VideoCapture('./WIN_20191115_14_17_02_Pro.mp4')
count = 0
while(cap.isOpened()):
    ret,image = cap.read()

    r = 600.0/image.shape[1]
    dim = (600, int(image.shape[0]*r))

    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    image_can = cv2.Canny(image_gray,100,200)
    #print(image_can)

    flip_image = image_can[::-1,:]
    bottom_values = np.array([np.argmax(flip_image[:,i]) for i in range(image.shape[1])])
    print(bottom_values)
    plt.plot(bottom_values)
    
    if (count%10 == 0):
        plt.show()
    
    count = count + 1
    cv2.imshow('frame',image_can)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
