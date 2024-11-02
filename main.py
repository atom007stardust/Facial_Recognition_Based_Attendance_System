import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-cf1cd-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-cf1cd.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640) #width
cap.set(4, 480) #height

#Importing the mode images into a list
imgBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath) #os.listdir lists all the file names and stores them in modePathList
imgModeList =  [] #a list to store the images
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList))

#Load the encoding file
print("Loading Encode File...")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = -1 # to download the information once only in the first iteration
studentInfo = None
imgStudent = []
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25) #imgS means image small
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    #Feed values to facial recognition,faces in current frame and encodings in the current frame
    faceCurFrame = face_recognition.face_locations(imgS)
    #find encodings of the new ones and then compare with the previous encodings
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    #loop through all the encodings and compare with generate encodings

    # overlaying the img and the background
    imgBackground[162: 162 + 480, 55: 55 + 640] = img  # starting point of height is 162, and that of width is 640
    imgBackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modeType]
    if faceCurFrame:
        for encodeFace, faceLocation in zip(encodeCurFrame, faceCurFrame): #extracted info of encodeCurFrame goes into encodeFace, and extracted info of faceCurFrame goes into faceLocation
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace) #the lower the distance, the better will be the match
            #print("matches", matches)
            #print("faceDistance", faceDistance)

        #get the matching index value
        matchIndex = np.argmin(faceDistance)
        #print(matchIndex)
        if matches[matchIndex]:
            #print("Known Face Detected")
            #print(studentIds[matchIndex])
            y1, x2 , y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 # We reduced the size by 4 earlier , so we need to multiply by 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1 #actual image starts from 0,0,  so we will give the image background's offset, #also, we don't need x1, x2 , we need a starting point i.e., x1, y1 then we need the width and the height, so how can we get it?  by doing x2-x1 and y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox=bbox, rt = 0)  #rt means rectangle thickness

            id = studentIds[matchIndex] #save the id of the matching face

             #draw rectangle around the face so we know that something is being detected
            if counter == 0:
                cvzone.putTextRect(imgBackground, "Loading", (275,400))
                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)
                counter =1
                modeType = 1
        if counter !=0:

            if counter ==1: #for the first frame
                #Download the student information
                #get the data
                studentInfo = db.reference(f'Students/{id}').get() #getting the student info
                print(studentInfo) #it downloads all the student's information, only on the first try
                #get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8) #standard procedure of converting so we can use it with opencv
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR) #THIS WILL GIVE US THE IMAGE

                ##Update the data of the attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                  "%Y-%m-%d %H:%M:%S")
                #whatever we get from database is string, we need to convert it into an object understood by datetime, then minus it from this time
                #it will be object-object and not string - string
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else: #if greater than 30
                    modeType = 3
                    counter = 0
                    imgBackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modeType]

            if modeType!=3:

                if 10<counter<20:
                    modeType = 2

                imgBackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modeType]


                if studentInfo is not None and counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861,125), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

                    cv2.putText(imgBackground, str(studentInfo['major']),(1006,550), cv2.FONT_HERSHEY_COMPLEX,0.3,(255,255,255),1)

                    cv2.putText(imgBackground, str(id),(1006,493), cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

                    cv2.putText(imgBackground, str(studentInfo['standing']),(910,625), cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

                    cv2.putText(imgBackground, str(studentInfo['year']),(1025,625), cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

                    cv2.putText(imgBackground, str(studentInfo['starting_year']),(1125,625), cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

                    #take total width-50px(my name length) and divide by 2 to get the center
                    (w,h),_ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414 - w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']),(808+offset,445), cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)

                    if studentInfo is not None:
                        # Ensure the imgStudent is properly loaded and not empty
                        if imgStudent is not None and len(imgStudent) > 0:
                            # Resize imgStudent to match the region size
                            imgStudent = cv2.resize(imgStudent, (216, 216))    ##################################################

                            # Now assign the resized image to the region
                            imgBackground[175:175 + 216, 909:909 + 216] = imgStudent



                counter+=1

                if counter>=20:
                    #resetting all the settings
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
        imgBackground[44: 44 + 633, 808: 808 + 414] = imgModeList[modeType]
    cv2.imshow("Webcam",img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)