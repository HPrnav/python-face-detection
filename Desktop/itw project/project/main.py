import cv2
import os
import numpy as np
import pickle
import face_recognition
import cvzone
from datetime import datetime



import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceaccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://students-attendence-9b56a-default-rtdb.firebaseio.com/",
    'storageBucket':"students-attendence-9b56a.appspot.com"
})

ref=db.reference("students")

bucket=storage.bucket()


vdo=cv2.VideoCapture(0)

bg_img=cv2.imread('templet.jpg')
bg_img =cv2.resize(bg_img,(900,600))
overlap=cv2.imread('overlap.jpg')  #900 x 60


# making the lsit of the image for differernt modes
folder_mode='MODES'
pathlist_mode=os.listdir('MODES')
image_list_mode=[]
for img in pathlist_mode:
    image_list_mode.append(cv2.imread(os.path.join(folder_mode,img)))
    
# print(image_list_mode[0]);

    
 # storing the encoding into "encoding_listwithid" the encoding which we prepared in the encoding.py and transfered to encoding.p .
file=open("encoding.p",'rb')
encoding_listwithId=pickle.load(file);
encodelistknown,student_id=encoding_listwithId
file.close()
# print("encoding printed")

modeType=0
counter=0
imageStudent=[]
while True:
    success,scr=vdo.read() 
    scr=cv2.resize(scr,(647,490))
    
    imgS=cv2.resize(scr,(0,0),None,0.25,0.25) # reducing the size according to scale to reduce the size
    imgS=cv2.cvtColor(scr,cv2.COLOR_BGR2RGB)
    
    facecurrframe=face_recognition.face_locations(imgS)  #finding the location of the frame in the current frame
    encodecurrface=face_recognition.face_encodings(imgS,facecurrframe) #finding the encoding of the curr location
    
    bg_img[30:30+490,2:2+647]=scr
    bg_img[28:28+500,670:670+230]=image_list_mode[modeType]
    
    if facecurrframe:
        for encode,faceloc in zip(encodecurrface,facecurrframe):
            match =face_recognition.compare_faces(encodelistknown,encode)
            face_dist =face_recognition.face_distance(encodelistknown,encode)
            # print(match)           # face distance is the measure that the encoding is how much different from another encoding
            # print(face_dist)
            
            matchIndex= np.argmin(face_dist)
            
            if(match[matchIndex]):
                # print("known face detected")
                # print(student_id[matchIndex])
                
                y1,x2,y2,x1= faceloc
                bbox=2+x1,30+y1,x2-x1,y2-y1
                bg_img = cvzone.cornerRect(bg_img,bbox,rt=0)

                id=student_id[matchIndex]
                if counter==0:
                    counter=1
                    modeType=1
        if counter!=0:
            
            if counter==1:
                studentInfo=db.reference(f'students/{id}').get()
                print(studentInfo)
                print(id)
                
                # taking image from bucket
                blob=bucket.get_blob(f'faces/{id}.jpeg')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imageStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                
                # date and time
                date_timeobj = datetime.strptime(studentInfo['last_attendence_time'],"%Y-%m-%d %H:%M:%S")
                sec_ellapsed=(datetime.now()-date_timeobj).total_seconds()
                print(sec_ellapsed)
                
                if(sec_ellapsed >90):
                    #  updating the attendence value
                    ref=db.reference(f'students/{id}')
                    studentInfo['total_attendence'] = str(int(studentInfo['total_attendence']) +1)
                    ref.child('total_attendence').set(studentInfo['total_attendence'])
                    ref.child('last_attendence_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType=3
                    counter=0
                    bg_img[28:28+500,670:670+230]=image_list_mode[modeType]
                
            if(modeType!=3):
                if( 10< counter <20):
                    modeType=2
                bg_img[28:28+500,670:670+230]=image_list_mode[modeType]
                bg_img[540:540+60,0:0+900]=overlap  # bg[height:height+size , width : width+size]
                    
                    
                if(counter <= 10):
                    cv2.putText(bg_img,str(':' + studentInfo['name']),(5,580),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0))
                    cv2.putText(bg_img,str(' majour:' + studentInfo['major']),(250,580),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0))
                    cv2.putText(bg_img,str(' year:' + studentInfo['year']),(500,580),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0))
                    cv2.putText(bg_img,str('attendence:' + studentInfo['total_attendence']),(700,580),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0))
                    #   bg_img[50:50+200,660:660+200]=imageStudent
                    
                counter+=1
                if counter>=20:
                    modeType=0
                    counter=0
                    studentInfo=[]
                    imageStudent=[]
                    bg_img[28:28+500,670:670+230]=image_list_mode[modeType]
    else:
        modeType=0
        counter=0
            
            
    cv2.imshow("screen",bg_img)
      
    if(cv2.waitKey(1))==ord('q'):
        break;
    
cv2.destroyAllWindows()



