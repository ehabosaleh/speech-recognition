from tkinter import *
#from pytube import YouTube
#from IPython.display import YouTubeVideo
from tkinter import messagebox, filedialog,scrolledtext
from tkinter import ttk
import tkinter as tk
import time
import threading
import os
from datetime import datetime
import subprocess, platform
from google_trans_new import google_translator
import arabic_reshaper
#from bidi.algorithm import get_display
from gtts import gTTS
from playsound import playsound
from sys import exit

class Speech_Recognition:
	def __init__(self):
		self.frame=Tk()
		self.frame.title("Research Scholar:  Reem Rostom || Speech Recognition || Audio Streaming")
		self.frame.geometry("800x580")
		self.frame.resizable(False, False)
	
		
	
		f_1=LabelFrame(self.frame,text="Subtitles",width=400,height=500)
		f_1.place(x=1,y=20)
		f_2=LabelFrame(self.frame,text="Translated",width=395,height=500)
		f_2.place(x=405,y=20)
		self.subtitles = scrolledtext.ScrolledText(f_1, wrap = tk.WORD, bg="black",fg="green",width = 37, height = 20, font = ("Times New Roman",15)) 
		self.translated = scrolledtext.ScrolledText(f_2, wrap = tk.WORD,bg="black",fg="green", width = 37, height = 20, font = ("Times New Roman",15))
		
		self.translated.tag_configure("tag-right",justify="right")
		self.subtitles.place(x=0,y=0)
		
		self.translated.place(x=0,y=0)
		self.t_1=threading.Thread(target=self.coincided_reading)
		self.t_2=threading.Thread(target=self.listening,args=())
		self.start_listening()
		Button(self.frame, text="Quit", command=self.frame.destroy).place(x=380,y=540)
		#time.sleep(1)
		self.frame.mainloop()
	
	def start_listening(self):
	
			now =datetime.now()
			self.dt_string = now.strftime("%d.%m.%Y-%H:%M:%S")

			os.mkdir(self.dt_string)

			self.t_2.start()

			time.sleep(0.01)
			self.t_1.start()


			
		
			
		
	def listening(self):


		if platform.system() == 'Windows': 
			f = open("{}\{}(en).txt".format(self.dt_string,self.dt_string), "a")
			
			subprocess.call(("python3","DeepSpeech-examples-r0.9\mic_vad_streaming\mic_vad_streaming.py","-m", "deepspeech-0.9.3\deepspeech-0.9.3-models.pbmm",  "-s", "deepspeech-0.9.3\deepspeech-0.9.3-models.scorer","-w",self.dt_string),stdout=f)
			
		else:
			
			f = open("{}/{}(en).txt".format(self.dt_string,self.dt_string), "a")
			audio='{}/{}(en).mp3'.format(self.dt_string,self.dt_string)
			subprocess.call(("python3","DeepSpeech-examples-r0.9/mic_vad_streaming/mic_vad_streaming.py","-m", "deepspeech-0.9.3/deepspeech-0.9.3-models.pbmm", "-s", "deepspeech-0.9.3/deepspeech-0.9.3-models.scorer","-w",self.dt_string),stdout=f)
		
	def coincided_reading(self):
		if platform.system()=="Windows":
			enfile = open("{}\{}(en).txt".format(self.dt_string,self.dt_string), "r")
			
		else:
			enfile = open("{}/{}(en).txt".format(self.dt_string,self.dt_string), "r")
			
		enfile.seek(0,2)
		translator = google_translator()
		i=0

		while True:

			line = enfile.readline()
			if not line or line=="\n":
				time.sleep(0.05)
				continue
			self.subtitles.insert("0.0",line)	

			result=translator.translate(line,lang_tgt='ar')
			result="\n" +result
			result=arabic_reshaper.reshape(result)
			self.translated.insert("1.0",result[::-1],"tag-right")
			#ar_text=self.translated.get("1.0",END)
			
			sound = gTTS(text=result, lang="ar", slow=False)
			if platform.system()=="Windows":
				sound.save("{}\{}(ar).wav".format(self.dt_string,i))
				playsound("{}\{}(ar).wav".format(self.dt_string,i)) 
				arfile = open("{}\{}(ar).txt".format(self.dt_string,self.dt_string), "a")
			else:
				sound.save("{}/{}(ar).wav".format(self.dt_string,i))
				playsound("{}/{}(ar).wav".format(self.dt_string,i))
				arfile = open("{}/{}(ar).txt".format(self.dt_string,self.dt_string), "a")
			arfile.write(result)
			arfile.close() 
			i=i+1
						
	
sr=Speech_Recognition()

