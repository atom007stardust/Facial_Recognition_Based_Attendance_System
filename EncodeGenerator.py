import os
import cv2
import face_recognition
import dlib
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-cf1cd-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-cf1cd.appspot.com"
})





folderPath = 'Images'
pathList = os.listdir(folderPath) #os.listdir lists all the file names and stores them in modePathList
print(pathList)

imgList =  [] #a list to store the images
studentIds = []


for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
   # print(path)
    print(os.path.splitext(path)[0])  #remove png from the filename
    studentIds.append(os.path.splitext(path)[0]) #storing it one by one

    fileName = f'{folderPath}/{path}' #once we have the filename, we can create a bucket
    bucket = storage.bucket()
    blob = bucket.blob(fileName) #create a blob to send the filename
    blob.upload_from_filename(fileName)
    #this will create a folder called images, and in that folder have all the content


print(studentIds)
print(len(imgList))



#look through all the images and encode every single image
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("No face found in the image, skipping...")
    return encodeList


'''
In summary, generating face encodings is essential for converting complex facial features into a format that can be efficiently used for recognition,
 comparison, and storage in facial recognition systems.
'''

#we need to save two things, std id and the encodings, to determine which id belongs to which encoding


print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]

print(encodeListKnown)
print("Encoding Complete")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file) #dump the encoding list with IDs in the file
file.close()
print("File saved")