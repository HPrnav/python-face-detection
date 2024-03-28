import cv2
import pickle
import os
import face_recognition


# making a list of the num py  array of the faces and along side adding the id with the face encoding
folder_face='faces'                               #saving the folder name in form of string
pathlist_face=os.listdir(folder_face)             # adding all element inside folder into the lsit using  os.listdir
image_list_face=[]                                # making  two empty list one for the face another for id 
student_id=[]                                # the imread function returns the numpy array 

for path in pathlist_face:  
    image_list_face.append(cv2.imread(os.path.join(folder_face,path)))
    student_id.append(os.path.splitext(path)[0])
     
#function to conver the image into encoding
def find_encode(image_list_faces):              
    encoded_list=[]
    for img in image_list_face:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]    # function in the face recognition library to convert our numpy arrray into encoding
        encoded_list.append(encode)                        # we used [0] bcox we want the first face from the image
    return encoded_list


encoded_list=find_encode(image_list_face)          
encoded_listwithid=[encoded_list,student_id]             # list which contain the encoding and id

file=open("encoding.p",'wb')
pickle.dump(encoded_listwithid,file)
file.close()
print("file saved")