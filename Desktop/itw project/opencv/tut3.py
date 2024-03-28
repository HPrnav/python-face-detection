import numpy as np
import cv2

# vdo=cv2.VideoCapture()
main_img=cv2.imread('image.jpg',0) 
main_img=cv2.resize(main_img,(0,0),fx=0.8,fy=0.8)
template=cv2.imread('templete.png',0)
template=cv2.resize(template,(0,0),fx=0.8,fy=0.8)
cv2.imshow('finished_img',template)
cv2.waitKey(0)

h,w=template.shape

 
result=cv2.matchTemplate(main_img,template,cv2.TM_CCORR_NORMED)
min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(result)

top_left=max_loc
# //THE LOCATION is min location i.e the top left corner
bottom_right=(top_left[0]+w,top_left[1]+h)
cv2.rectangle(main_img,top_left,bottom_right,0,5)
cv2.imshow('finished_img',main_img)
cv2.waitKey(0)
cv2.destroyAllWindows()



