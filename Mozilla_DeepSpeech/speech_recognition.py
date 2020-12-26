from tkinter import *
from pytube import YouTube
from IPython.display import YouTubeVideo
from tkinter import messagebox, filedialog
from tkinter import ttk
import time
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
		self.progress.grid(row=1,column=1)
		Button(self.frame,text="Download",command=self.download).grid(row=1,column=0)
		self.frame.mainloop()
	def display(self):
		url=self.url.get()
		print(url[url.index("=")+1:])
		YouTubeVideo(url)

	def download(self): 
		self.progress.start(10)
		Youtube_link = self.url.get()
		getVideo = YouTube(Youtube_link)
		videoStream = getVideo.streams.first()

		videoStream.download()

		messagebox.showinfo("SUCCESSFULLY",
                        "DOWNLOADED")
		self.progress.stop()
sr=Speech_Recognition()

