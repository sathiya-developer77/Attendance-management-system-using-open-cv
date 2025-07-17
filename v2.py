import os
import cv2
import numpy as np
import pandas as pd
import face_recognition
from datetime import datetime

path = 'C:\\Users\\chezh\\OneDrive\\Desktop\\cv\\photos' #Enter the path where you have stored the preprocessing images
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

csvpath = 'C:\\Users\\chezh\\OneDrive\\Desktop\\cv\\attendancesystemcsv.csv'
os.remove(csvpath)
with open(csvpath,'w') as f:
    pass

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance():
    resultData = []
    presentdict.update(absentdict)    
    for i in presentdict:
        tempDict = {}
        tempDict["Name"] = i
        tempDict["Status"] = presentdict[i][1]
        tempDict["Time"] = presentdict[i][0]
        resultData.append(tempDict)        
    df = pd.DataFrame(resultData)
    df.to_csv('C:\\Users\\chezh\\OneDrive\\Desktop\\cv\\attendancesystemcsv.csv', index=False, header=True)

presentdict = {}
def presentdictionary(name):
    if name not in presentdict:
        now = datetime.now()
        presentdict[name] = [now.strftime('%H:%M:%S'), 'Present']

absentdict = {}
def absentdictionary(name):
    if name not in absentdict:
        reset = datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        absentdict[name] = [reset.strftime('%H:%M:%S'), 'Absent']    

encodeListKnown = findEncodings(images)
print("encoding completed")

cam = cv2.VideoCapture(0)

while True:
    success, img = cam.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    facelocCurframe = face_recognition.face_locations(imgS)
    encodeCurrentface = face_recognition.face_encodings(imgS,facelocCurframe)

    for encodeface, faceloc in zip(encodeCurrentface,facelocCurframe):
        matches = face_recognition.compare_faces(encodeListKnown,encodeface)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeface)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,255),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            presentdictionary(name)

    cv2.imshow('webcam',img)
    if cv2.waitKey(100) & 0xff == ord('q'):
        break

for i in classNames:
    if i not in presentdict:
        absentdictionary(i)

markAttendance()

cam.release()
cv2.destroyAllWindows()

