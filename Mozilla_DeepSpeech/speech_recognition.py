from tkinter import *
from pytube import YouTube
from IPython.display import YouTubeVideo
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
from bidi.algorithm import get_display
class Speech_Recognition:
	def __init__(self):
		self.frame=Tk()
		self.frame.title("PhD Project for Speech Recognition. Research Scholar:  Reem Rostom")
		self.frame.geometry("800x700")
		self.frame.resizable(False, False)
		canvas_1=Canvas(self.frame)
		#Label(self.frame,text="Youtube URL:").place(x=0,y=20)
		self.url=Entry(self.frame,text="Youtube URL",font=("time",10,"italic"),width=85)
		self.url.place(x=95,y=20)

		self.progress = ttk.Progressbar(self.frame, orient = HORIZONTAL,length = 800, mode = 'indeterminate')

		Button(self.frame,text="Download",command=self.run).place(x=0,y=17)
		var_1 =IntVar()
		var_1.set(1)

		r1=Radiobutton(self.frame,text="Batching",indicatoron=0,variable=var_1,value=1,command=self.batching)
		r2=Radiobutton(self.frame,text="Streaming",indicatoron=0,variable=var_1,value=2,command=self.streaming)
		self.speak=Button(self.frame,text="Start Speaking",command=self.start_speaking)
		r1.place(x=300,y=70)
		r2.place(x=400,y=70)
		self.speak.place(x=350,y=190)
		self.speak.place_forget()
		self.open_file=Button(self.frame,text="Open",padx=27,command=self.open)
		self.open_file.place(x=0,y=90)
		self.path=Entry(self.frame,font=("time",10,"italic"),width=105)
		self.path.place(x=95,y=95)
		self.path.insert(0,os.path.abspath(os.getcwd()))
		self.title=Label(self.frame,text=" ",font=("time",8,"normal"))
		self.title.place(x=100,y=140)
		self.file_name=Label(self.frame,text="File name:")
		self.file_name.place(x=0,y=140)
		self.conv2wav=Button(self.frame,text="convert 2 wav",command=self.conv_2_wav)
		self.conv2wav.place(x=660,y=140)
		self.conv2wav["state"]="disable"
		
		self.extract=Button(self.frame,text="Extract",padx=23,command=self.extract_subtitles)
		self.extract.place(x=150,y=190)
		self.extract["state"]="disable"
		self.translate=Button(self.frame,text="Translate",command=self.translate)
		self.translate["state"]="disable"
		self.translate.place(x=550,y=190)
		canvas_1.create_line(0,150,600,150,dash=(4,2))
		canvas_1.pack()
		f_1=LabelFrame(self.frame,text="Subtitles",width=400,height=500)
		f_1.place(x=1,y=220)
		f_2=LabelFrame(self.frame,text="Translated",width=395,height=500)
		f_2.place(x=405,y=220)
		self.subtitles = scrolledtext.ScrolledText(f_1, wrap = tk.WORD, bg="black",fg="green",width = 37, height = 20, font = ("Times New Roman",15)) 
		self.translated = scrolledtext.ScrolledText(f_2, wrap = tk.WORD,bg="black",fg="green", width = 37, height = 20, font = ("Times New Roman",15))
		
		self.translated.tag_configure("tag-right",justify="right")
		self.subtitles.place(x=0,y=0)
		
		self.translated.place(x=0,y=0)
		self.m = Menu(self.frame, tearoff=0)
		self.m.add_command(label="Cut")
		self.m.add_separator()
		self.m.add_command(label="Copy")
		self.m.add_separator()
		self.m.add_command(label="Paste")
		self.m.add_separator()
		self.m.add_command(label="Select all")

		self.frame.bind_class("Entry", "<Button-3><ButtonRelease-3>", self.show_textmenu)
		self.frame.bind_class("Entry", "<Control-a>", self.callback_select_all)
		self.frame.bind_class("Text", "<Button-3><ButtonRelease-3>", self.show_textmenu)
		self.frame.bind_class("Text", "<Control-a>", self.callback_select_all)
		self.frame.mainloop()
	
	def callback_select_all(self,event):

		self.frame.after(50, lambda:event.widget.select_range(0, 'end'))
	def batching(self):
		self.open_file["state"]="active"
		self.path["state"]="normal"
		self.title["state"]="active"
		self.file_name["state"]="active"
		self.speak.place_forget()
	def streaming(self):
		self.open_file["state"]="disable"
		self.path["state"]="disable"
		self.title["state"]="disable"
		self.file_name["state"]="disable"
		self.speak.place(x=320,y=170)
	def start_speaking(self):
		now =datetime.now()
		#self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		self.dt_string="ehab"
		t_1=threading.Thread(target=self.coincided_reading)
		t_2=threading.Thread(target=self.listen)
		t_1.start()
		t_2.start()	
	def listen(self):

		f = open("{}.txt".format(self.dt_string), "w")
		if platform.system() == 'Windows': 
			subprocess.call(("python3","DeepSpeech-examples-r0.6\mic_vad_streaming\mic_vad_streaming.py","-m", "deepspeech-0.6.1-models\output_graph.pbmm", "-l", "deepspeech-0.6.1-models\lm.binary"),stdout=f)
		else:
			subprocess.call(("python3","DeepSpeech-examples-r0.6/mic_vad_streaming/mic_vad_streaming.py","-m", "deepspeech-0.6.1-models/output_graph.pbmm", "-l", "deepspeech-0.6.1-models/lm.binary"),stdout=f)
		
	def coincided_reading(self):
		thefile=open("{}.txt".format(self.dt_string),'r') 
		thefile.seek(0,2)
		while True:
			line = thefile.readline()
			if not line:
				time.sleep(0.1)
				continue
			#self.subtitles.delete("1.0",END)
			self.subtitles.insert("0.0",line)	
					
	def show_textmenu(self,event):
		e_widget = event.widget
		self.m.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
		self.m.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
		self.m.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
		self.m.entryconfigure("Select all",command=lambda: e_widget.select_range(0, 'end'))
		self.m.tk.call("tk_popup", self.m, event.x_root, event.y_root)
		

			
	def conv_2_wav(self):
		path=self.path.get()
		t=threading.Thread(target=self.progress_bar)
		if platform.system() == 'Windows':    # Windows
			t.start()
			subprocess.call(("ffmpeg","-i","{}".format(path),"{}.wav".format(os.path.splitext(path)[0])))
		else:   
			t.start()                                # linux variants
			subprocess.call(("ffmpeg","-i","{}".format(path),"{}.wav".format(os.path.splitext(path)[0])))
		
		messagebox.showinfo("SUCCESSFULLY",
                        "Video converted to audio successfully")
		self.progress.stop()
		self.progress.place_forget()
		
			
	def translate(self):
		path=self.path.get()
		english_text=self.subtitles.get("1.0",END)
		translator = google_translator()
		result=translator.translate(english_text,lang_tgt='ar') 
		self.translated.delete("1.0",END)
		result=arabic_reshaper.reshape(result)
		self.translated.insert("1.0",result[::-1],"tag-right")

		f = open("{}.txt".format(os.path.splitext(path)[0]), "a") 
		f.write("\n")
		f.write(result)
		f.close()	
		
	def extract_subtitles(self):
		
			path=self.path.get()
			f = open("{}.txt".format(os.path.splitext(path)[0]), "w") 
		
			if platform.system() == 'Windows':    # Windows
				
				subprocess.call(("deepspeech","--model","deepspeech-0.6.1-models\output_graph.pbmm","--lm","deepspeech-0.6.1-models\lm.binary","--trie","deepspeech-0.6.1-models\Trie","--audio","{}".format(os.path.basename(path))),stdout=f)
			else:   
				
				subprocess.call(("deepspeech","--model","deepspeech-0.6.1-models/output_graph.pbmm","--lm","deepspeech-0.6.1-models/lm.binary","--trie","deepspeech-0.6.1-models/Trie","--audio","{}".format(os.path.basename(path))),stdout=f)
			

			f.close()
			f = open("{}.txt".format(os.path.splitext(path)[0]), "r") 
			self.subtitles.delete("1.0",END)
			self.subtitles.insert("0.0",f.read())	
			f.close()
			
	def run(self):
		t1=threading.Thread(target=self.progress_bar)
		t2=threading.Thread(target=self.download)
		t1.start()
		t2.start()

	def progress_bar(self):
		self.progress.place(x=0,y=0)
		self.progress.start(5)
	def download(self):
		t=threading.Thread(target=self.progress_bar)
		try:
			
			Youtube_link = self.url.get()
			getVideo = YouTube(Youtube_link)
			t.start()
			videoStream = getVideo.streams.first()
			videoStream.download()
			self.progress.stop()
			self.progress.place_forget()
			messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED")
		except:
			self.progress.stop()
			self.progress.place_forget()
			messagebox.showerror("Error", "Please insert a valid Youtube URL!")
			
	def open(self):
		filepath=filedialog.askopenfilename(initialdir=self.path.get(),title="Open video file",filetypes=(("Video File",".mp4"),("Audio File",".wav")))
		if platform.system() == 'Darwin':       # macOS
			subprocess.call(('open', filepath))
		elif platform.system() == 'Windows':    # Windows
    			os.startfile(filepath)
		else:                                   # linux variants
			subprocess.call(('xdg-open', filepath))
		self.path.delete(0,END)
		self.path.insert(0,filepath)
		self.title.config(text=os.path.basename(filepath))
		print(self.path.get())
		if os.path.splitext(self.path.get())[1]==".mp4":
			self.conv2wav["state"]="active"
			self.extract["state"]="disable"
			self.translate["state"]="disable"
		else:
			self.conv2wav["state"]="disable"
			self.extract["state"]="active"
			self.translate["state"]="active"
sr=Speech_Recognition()
