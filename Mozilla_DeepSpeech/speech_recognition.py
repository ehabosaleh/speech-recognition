from tkinter import *
from pytube import YouTube
from IPython.display import YouTubeVideo
from tkinter import messagebox, filedialog
from tkinter import ttk
import time
import threading
import os
import subprocess, platform
class Speech_Recognition:
	def __init__(self):
		self.frame=Tk()
		self.frame.title("PhD Project for Speech Recognition. Research Scholar:  Reem Rostom")
		self.frame.geometry("600x500")
		self.frame.resizable(False, False)
		Label(self.frame,text="Youtube URL:").place(x=0,y=20)
		self.url=Entry(self.frame,font=("time",12,"italic"),width=40)
		self.url.place(x=90,y=20)

		self.progress = ttk.Progressbar(self.frame, orient = HORIZONTAL,length = 600, mode = 'indeterminate')

		Button(self.frame,text="Download",command=self.run).place(x=500,y=17)
		Button(self.frame,text="Open",padx=23,command=self.open).place(x=0,y=50)
		self.path=Entry(self.frame,font=("time",10,"italic"),width=63)
		self.path.place(x=90,y=55)
		self.path.insert(0,os.path.abspath(os.getcwd()))
		self.title=Label(self.frame,text=" ",font=("time",10,"normal"))
		self.title.place(x=100,y=90)
		Label(self.frame,text="File name:").place(x=0,y=90)
		self.frame.mainloop() 
	def run(self):
		self.t1=threading.Thread(target=self.progress_bar)
		self.t2=threading.Thread(target=self.download)
		self.t1.start()
		self.t2.start()


	def display(self):
		url=self.url.get()
		print(url[url.index("=")+1:])
		YouTubeVideo(url)

	def progress_bar(self):
		self.progress.place(x=0,y=0)
		self.progress.start(5)
	def download(self):
		Youtube_link = self.url.get()
		getVideo = YouTube(Youtube_link)
		videoStream = getVideo.streams.first()
		videoStream.download()
		messagebox.showinfo("SUCCESSFULLY",
                        "DOWNLOADED")
		self.progress.stop()
		self.progress.place_forget()
	def open(self):
		filepath=filedialog.askopenfilename(initialdir=self.path.get(),title="Open video file",filetypes=(("Video File",".mp4"),("Audio File",".mp3")))
		if platform.system() == 'Darwin':       # macOS
			subprocess.call(('open', filepath))
		elif platform.system() == 'Windows':    # Windows
    			os.startfile(filepath)
		else:                                   # linux variants
			subprocess.call(('xdg-open', filepath))
		self.path.delete(0,END)
		self.path.insert(0,filepath)
		self.title.config(text=os.path.basename(filepath))
sr=Speech_Recognition()

