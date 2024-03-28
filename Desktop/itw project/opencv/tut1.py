import cv2
img1 =cv2.imread('city.jpg',1)
img1 =cv2.resize(img1,(700,700))
# img1=cv2.rotate(img1,cv2.ROTATE_90_COUNTERCLOCKWISE)

# cut=img1[100:300,300:400]
# img1[100:300,600:700]=cut

cv2.imshow('img_win',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()  