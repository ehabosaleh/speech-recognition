from tkinter import *
from pytube import YouTube
from IPython.display import YouTubeVideo
from tkinter import messagebox, filedialog
from tkinter import ttk
import time
import threading
class Speech_Recognition:
	def __init__(self):
		self.frame=Tk()
		self.frame.title("PhD Project for Speech Recognition. Research Scholar:  Reem Rustom")
		self.frame.geometry("600x500")
		self.frame.resizable(False, False)
		Label(self.frame,text="Youtube URL:").grid(row=0,column=0)
		self.url=Entry(self.frame,font=("time",12,"italic"),width=50)
		self.url.grid(row=0,column=1)
		#Button(self.frame,text="Open",command=self.display).grid(row=1,column=1)
		self.progress = ttk.Progressbar(self.frame, orient = HORIZONTAL,length = 200, mode = 'indeterminate')
		#self.progress.grid(row=1,column=1)
		Button(self.frame,text="Download",command=self.run).grid(row=1,column=0)
		self.frame.mainloop()
	def run(self):
		t1=threading.Thread(target=self.progress_bar)
		t2=threading.Thread(target=self.download)
		t1.start()
		t2.start()

		
	def display(self):
		url=self.url.get()
		print(url[url.index("=")+1:])
		YouTubeVideo(url)

	def progress_bar(self):
		self.progress.grid(row=1,column=1)
		self.progress.start(5)
	def download(self):
		Youtube_link = self.url.get()
		getVideo = YouTube(Youtube_link)
		videoStream = getVideo.streams.first()
		videoStream.download()
		messagebox.showinfo("SUCCESSFULLY",
                        "DOWNLOADED")
		self.progress.stop()
		self.progress.grid_forget()
sr=Speech_Recognition()

