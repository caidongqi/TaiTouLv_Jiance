import numpy as np
import cv2

cap = cv2.VideoCapture(0)
print(cap.isOpened())
ret, img = cap.read()
print(ret, img)
cv2.imshow("Image", img)
cv2.imwrite(r"C:\Users\86132\Desktop\dlib\dlib-master\examples\faces\example4.png", img)
cv2.waitKey(0)

# 释放摄像头资源
cap.release()