import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
## LOAD IMAGE
matplotlib.use('TKAgg')

def unsharp_mask(image,k1,k2):
    gaussian_image = cv2.GaussianBlur(image,(3,3),0)
    return cv2.addWeighted(image, k1, gaussian_image, k2, 0)

bottom_pixel_frames = []

cap = cv2.VideoCapture('./coop60fps.mov')
count = 0
while(cap.isOpened()):

    ret,image = cap.read()
    
    if count == 0:
        roi = cv2.selectROI(image)

    image = image[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]

    r = 600.0/image.shape[1]
    dim = (600, int(image.shape[0]*r))

    # image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #image sharpening
    image_gray = unsharp_mask(image_gray,1.5,-1)

    image_can = cv2.Canny(image_gray,100,200)
    #print(image_can)

    flip_image = image_can[::-1,:]
    bottom_values = np.array([np.argmax(flip_image[:,i]) for i in range(image.shape[1])])
    bottom_pixel_frames.append(bottom_values)

    flip_image = cv2.cvtColor(flip_image,cv2.COLOR_GRAY2BGR)
    pixel_c = 1
    for pixel in bottom_values:
        try:
            flip_image[pixel_c][pixel][2] = 255
            pixel_c += 1
        except:
            pass
        print(pixel_c)

    cv2.imshow('frame', image_can)
    count = count + 1
# cv2.imshow('frame',image_can)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r.')

def init():
    ax.set_xlim(0, len(bottom_pixel_frames[0]))
    ax.set_ylim(-1, 1000)
    return ln,

def update(frame):
    xdata = range(0,len(frame))
    ydata = frame
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=bottom_pixel_frames,
                    init_func=init, blit=True)
plt.show()
