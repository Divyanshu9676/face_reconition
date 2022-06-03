import face_recognition as fr
import cv2
from face_recognition.api import face_distance
import numpy as np
import csv
import datetime
from subprocess import call
import speech_recognition as sr
from gtts import gTTS
from playsound import  playsound
import glob, os

video_capture=cv2.VideoCapture(0)

known_face_encodings=[]
known_face_names= []
names=[]

f=open("name.txt","r")
data=f.readlines()
data.sort()
for i in range(len(data)):
    known_face_names.append(data[i])
f.close()

for file in glob.glob("*.jpg"):
    divy_img=fr.load_image_file(str(file))
    divy_face=fr.face_encodings(divy_img)[0]
    known_face_encodings.append(divy_face)

now = datetime.datetime.now()

r = sr.Recognizer()

os.chdir("/files")

language='hi'
playsound("welcome1.mp3")
vn=int(input("Enter value: "))

while True:
    ret, frame =video_capture.read()
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    face_location=fr.face_locations(rgb_frame)
    face_encoding=fr.face_encodings(rgb_frame,face_location)
    if vn==1:
        playsound("welcome2.mp3")
        playsound("welcome3.mp3")
        with sr.Microphone() as source:
            print("Speak now :")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                mytext="आपने कहा : {}".format(text)
                myobj=gTTS(text=mytext,lang=language,slow=True)
                myobj.save("welcome4.mp3")
                playsound("welcome4.mp3")
                playsound("welcome7.mp3")
                n=str(input("Enter value: "))
                if n==" ":
                    img_name = "{}".format(text)
                    cv2.imwrite("{}.jpg".format(img_name), frame)
                    f=open("name.txt","a")
                    f.write(str(text) + "\n")
                    f.close()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    print("photo saved")
                else:
                    playsound("welcome6.mp3")
            except:
                playsound("welcome5.mp3")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        playsound("welcome1.mp3")
        vn=int(input("Enter value: "))

    elif vn==2:
        for (top, right, bottom, left), face_encoding in zip(face_location,face_encoding):
            matches= fr.compare_faces(known_face_encodings, face_encoding)
            name="Unknown"
            face_distance=fr.face_distance(known_face_encodings, face_encoding)
            best_match=np.argmin(face_distance)
            if matches[best_match]:
                name=known_face_names[best_match]
            cv2.rectangle(frame, (left,top), (right,bottom), (0,0,255),2)
            cv2.rectangle(frame, (left, bottom -35), (right,bottom),(0,0,255),cv2.FILLED)
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name,(left + 6, bottom -6), font, 1.0, (255,255,255),1)

            sme=now.strftime("%H:%M:%S" )
            if name not in names:
                with open("names.csv",'a') as csv_file:
                    csv_reader=csv.writer(csv_file)
                    csv_reader.writerow([name,sme])
                    csv_file.close
                    names.append(name)
                    f=open("nam.txt","w")
                    f.write(name)
                    f.close()
                    call(["python","7.py"])
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        vn=2

video_capture.release()
cv2.destroyAllWindows()