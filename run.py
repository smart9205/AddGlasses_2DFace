from imutils import face_utils
import imutils
import time
import cv2
import dlib
from watermarking import watermarking
import numpy as np
from scipy.ndimage import rotate as rotate_image
import argparse



def parse(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', dest='image', type=str, default='4.jpg')
    parser.add_argument('--attr', dest='attrnum', type=int, default=1)
    return parser.parse_args(args)

args_ = parse()
if args_.attrnum > 2:
    args_.attrnum = 2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

glass = cv2.imread("data/glass.png", cv2.IMREAD_UNCHANGED)
moustache = cv2.imread("data/moustache.png", cv2.IMREAD_UNCHANGED)


frame = cv2.imread(args_.image)
frame = imutils.resize(frame, height=550)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
rects = detector(gray, 0)

# loopop over found faces
for rect in rects:
    shape = predictor(frame, rect)
    shape = face_utils.shape_to_np(shape)

    eyeLeftSide = 0
    eyeRightSide = 0
    eyeTopSide = 0
    eyeBottomSide = 0

    moustacheLeftSide = 0
    moustacheRightSide = 0
    moustacheTopSide = 0
    moustacheBottomSide = 0

    for (i, (x, y)) in enumerate(shape):
        # cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        if (i + 1) == 37:
            eyeLeftSide_x = x 
            eyeLeftSide_y = y 
        if (i + 1) == 46:
            eyeRightSide_x = x 
            eyeRightSide_y = y
        if (i + 1) == 2:
            moustacheLeftSide = x
            moustacheTopSide = y - 10
        if (i + 1) == 16:
            moustacheRightSide = x
        if (i + 1) == 9:
            moustacheBottomSide = y
        if (i + 1) == 28:
            center_x = x
            center_y = y
        if (i + 1) == 63:
            mouth_center_x = x
            mouth_center_y = y

    eyesWidth= eyeRightSide_x - eyeLeftSide_x
    eyesHeight = eyeRightSide_y - eyeLeftSide_y
    angle1 = np.arctan(eyesHeight/eyesWidth)    
    glassWidth = int(eyesWidth*1.62)
    sinValue = np.sin(angle1)
    if sinValue < 0:
        x_plus = 0
        y_plus = int(glassWidth * sinValue)
    else:
        x_plus = int(glassWidth * sinValue * -1)
        y_plus = 0
    fitedGlass = imutils.resize(glass, width=glassWidth)
    fitedGlass = imutils.rotate_bound(fitedGlass,angle1*180/np.pi)

    gray_image = cv2.cvtColor(fitedGlass, cv2.COLOR_BGR2GRAY)

    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    
    # calculate moments of binary image
    M = cv2.moments(thresh)    
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    # cv2.circle(fitedGlass, (cX, cY), 1, (255, 0, 0), -1)    
    if args_.attrnum == 1:
        frame = watermarking(frame, fitedGlass, x= center_x-cX, y= center_y - cY)
        cv2.imshow("Face Mask", frame)
        cv2.imwrite("result.jpg", frame)
    if args_.attrnum ==2:
        moustacheWidth= int((moustacheRightSide - moustacheLeftSide)*1.05)    
        fitedMoustache = imutils.resize(moustache, width=moustacheWidth)
        fitedMoustache = imutils.rotate_bound(fitedMoustache,angle1*180/np.pi)
        gray_image = cv2.cvtColor(fitedMoustache, cv2.COLOR_BGR2GRAY) 
        # convert the grayscale image to binary image
        ret,thresh = cv2.threshold(gray_image,127,255,0)    
        # calculate moments of binary image
        M = cv2.moments(thresh)    
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        frame = watermarking(frame, fitedMoustache, x= mouth_center_x-cX, y= mouth_center_y-cY)
        cv2.imshow("Face Mask", frame)
        cv2.imwrite("result.jpg", frame)
cv2.waitKey()




