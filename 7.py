from playsound import  playsound
from win32com.client import Dispatch

f=open("nam.txt","r")
a=f.read()
f.close()
speak=Dispatch(("SAPI.SpVoice"))
speak.Speak(a)
playsound("welcome10.mp3")