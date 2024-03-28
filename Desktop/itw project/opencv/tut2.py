import numpy as np
import cv2
vdo=cv2.VideoCapture(0)
while True:
    rv,frame=vdo.read()
    height=int(vdo.get(4))
    width=int(vdo.get(3))
    canvus=np.zeros(frame.shape,np.uint8)
    
    smaller_frame=cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
    smaller_frame_flip=cv2.flip(smaller_frame,1)
    smaller_frame_180=cv2.rotate(smaller_frame,cv2.ROTATE_180)
    smaller_frame_180_flip=cv2.flip(smaller_frame_180,1)
    
    canvus[:height//2,:width//2]=smaller_frame_180_flip
    canvus[height//2:,:width//2]=smaller_frame
    canvus[:height//2,width//2:]=smaller_frame_180
    canvus[height//2:,width//2:]=smaller_frame_flip
    
    cv2.imshow('framed',canvus)
    if(cv2.waitKey(1 ))==ord('q'):
        break;
vdo.release()
cv2.destroyAllWindows()



# import numpy as np
# import cv2

# vdo=cv2.VideoCapture(0)
# while True:
#     rv,frame=vdo.read()
    
#     cv2.imshow('framed',frame)
#     if(cv2.waitKey(1 ))==ord('q'):
#         break;
# vdo.release()
# cv2.destroyAllWindows()
    
    