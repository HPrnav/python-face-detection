import cv2
import os
import numpy as np
import pickle
import face_recognition

vdo=cv2.VideoCapture(0)

bg_img=cv2.imread('templet.jpg')
bg_img =cv2.resize(bg_img,(900,600))



# making the lsit of the image for differernt modes
folder_mode='MODES'
pathlist_mode=os.listdir('MODES')
image_list_mode=[]
for img in pathlist_mode:
    image_list_mode.append(cv2.imread(os.path.join(folder_mode,img)))
    
print(image_list_mode[0]);

    
 # storing the encoding into "encoding_listwithid" the encoding which we prepared in the encoding .py and transfered to encoding.p .
file=open("encoding.p",'rb')
encoding_listwithId=pickle.load(file);
encodelistknown,student_id=encoding_listwithId
file.close()
print("encoding printed")


while True:
    success,scr=vdo.read() 
    scr=cv2.resize(scr,(647,490))
    
    imgS=cv2.resize(scr,(0,0),None,0.25,0.25) # reducing the size according to scale to reduce the size
    imgS=cv2.cvtColor(scr,cv2.COLOR_BGR2RGB)
    
    facecurrframe=face_recognition.face_locations(imgS)  #finding the location of the frame in the current frame
    encodecurrface=face_recognition.face_encodings(imgS,facecurrframe) #finding the encoding of the curr location
    
    for encode in encodecurrface:
        match=face_recognition.compare_faces(encodelistknown,encode)
        face_dist=face_recognition.face_distance(encodelistknown,encode)
        print(match)           # face distance is the measure that the encoding is how much different from another encoding
        print(face_dist)
    
    
    bg_img[30:30+490,2:2+647]=scr
    bg_img[28:28+500,670:670+230]=image_list_mode[2]
    
    cv2.imshow("screen",bg_img)
    
    if(cv2.waitKey(1))==ord('q'):
        break;
    
cv2.destroyAllWindows()



