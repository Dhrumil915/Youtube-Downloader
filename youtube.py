from tkinter import *
from tkinter import ttk
from pytube import *
from PIL import Image,ImageTk
import requests
import io
import os

class Youtube_download:
    def __init__(self,root):
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry("500x420+300+50")
        self.root.resizable(False,False)
        self.root.config(bg='white')

        tittle = Label(self.root,text="Youtube Download",font=("times new roman",15),bg="#262626",fg='white')
        tittle.pack(side=TOP,fill=X)

        self.var_url = StringVar()
        lbl_url = Label(self.root,text="Video Url",font=("times new roman",15,'bold'),bg="white")
        lbl_url.place(x=10,y=50)
        txt_url = Entry(self.root,font=("times new roman",13),textvariable=self.var_url,bg="lightyellow")
        txt_url.place(x=120,y=50,width=350)
        
        lbl_filetype = Label(self.root,text="File Type",font=("times new roman",15,'bold'),bg="white")
        lbl_filetype.place(x=10,y=90)
        self.var_filetype = StringVar()
        video_radio = Radiobutton(self.root,text="Video",variable=self.var_filetype,value='Video',font=("times new roman",15,'bold'),bg="white",activebackground="white")
        video_radio.place(x=120,y=90)
        audio_radio = Radiobutton(self.root,text="Audio",variable=self.var_filetype,value='Audio',font=("times new roman",15,'bold'),bg="white",activebackground="white")
        audio_radio.place(x=220,y=90)


        btn_search = Button(self.root,text='Search',command=self.search, font=("times new roman",15),bg='blue',fg='white')
        btn_search.place(x=350,y=90,h=30,w=120)


        Frame1 = Frame(self.root,bd=2,relief=RIDGE,bg='lightyellow')
        Frame1.place(x=10,y=130,w=480,h=180)

        self.video_title = Label(Frame1,text="Video title Here",font=("times new roman",15),bg="lightgray")
        self.video_title.place(x=0,y=0,relwidth=1)

        self.video_image = Label(Frame1,text="Video \nImage",font=("times new roman",15),bg="lightgray",bd=2,relief=RIDGE)
        self.video_image.place(x=5,y=30,w=180,h=140)

        lbl_desc = Label(Frame1,text="Decription",font=("times new roman",15),bg="lightyellow")
        lbl_desc.place(x=190,y=30)

        self.video_desc = Text(Frame1,font=("times new roman",12),bg="lightyellow")
        self.video_desc.place(x=190,y=60,w=280,h=110)

        self.lbl_size = Label(self.root,text="Total Size: MB",font=("times new roman",13,'bold'),bg="white")
        self.lbl_size.place(x=10,y=320)

        self.lbl_percent = Label(self.root,text="Downloading: 0%",font=("times new roman",13,'bold'),bg="white")
        self.lbl_percent.place(x=165,y=320)

        btn_clear = Button(self.root,text='Clear',command=self.clear ,font=("times new roman",13),bg='red',fg='white')
        btn_clear.place(x=330,y=320,h=25,w=70)
        self.btn_download = Button(self.root,text='Download',state=DISABLED,command=self.download,font=("times new roman",13),bg='green',fg='white')
        self.btn_download.place(x=405,y=320,h=25,w=90)


        self.prog = ttk.Progressbar(self.root,orient=HORIZONTAL,length=590,mode='determinate')
        self.prog.place(x=10,y=360,w=485,h=20)


        self.lbl_message = Label(self.root,text="",font=("times new roman",13),bg="white")
        self.lbl_message.place(x=0,y=385,relwidth=1)

        ##========maiing dircetry
        if os.path.exists('Audios')==False:
            os.mkdir('Audios')
        if os.path.exists('Videos')==False:
            os.mkdir('Videos')    

        #==========Function==========

    def search(self):
        if self.var_url.get()=='':
            self.lbl_message.config(text="Video URL required",fg='red')
        else:    
            yt=YouTube(self.var_url.get())
            response=requests.get(yt.thumbnail_url)
            img_bytes=io.BytesIO(response.content)
            self.img=Image.open(img_bytes)
            self.img=self.img.resize((180,140),Image.ANTIALIAS)
            self.img=ImageTk.PhotoImage(self.img)
            self.video_image.config(imag=self.img)
            if self.var_filetype.get()=='Video':
                select_file=yt.streams.filter(progressive=True).first()
            if self.var_filetype.get()=='Audio':
                select_file=yt.streams.filter(only_audio=True).first()
            self.size_inbytes=select_file.filesize
            max_size=self.size_inbytes/1024000
            self.mb=str(round(max_size,2))+'MB'
            self.lbl_size.config(text='Total Size: '+self.mb) 
            self.video_title.config(text=yt.title)
            self.video_desc.delete('1.0',END)
            self.video_desc.insert(END,yt.description[:200])
            self.btn_download.config(state=NORMAL)

    def progess_(self,streams,chunk,bytes_remaining):
        percentage=(float(abs(bytes_remaining-self.size_inbytes)/self.size_inbytes))*float(100)
        self.prog['value']=percentage
        self.prog.update()
        self.lbl_percent.config(text=f"Downloading: {str(round(percentage,2))}%")
        if round(percentage,2)==100:
            self.lbl_message.config(text="Download Completed...",fg='green')
            self.btn_download.config(state=DISABLED)


    def clear(self):
        self.var_filetype.set('Video')
        self.var_url.set('')
        self.prog['value']=0
        self.btn_download.config(state=DISABLED)
        self.lbl_message.config(text='')
        self.video_title.config(text='Video Title Here')
        self.video_image.config(image='')
        self.video_desc.delete('1.0',END)
        self.lbl_size.config(text='Downloading:0%')
        self.lbl_percent.config(text='Total Size: MB')
        
    def download(self):
        yt=YouTube(self.var_url.get(),on_progress_callback=self.progess_)
        if self.var_filetype.get()=='Video':
             select_file=yt.streams.filter(progressive=True).first()
             select_file.download('Videos/')
        if self.var_filetype.get()=='Audio':
            select_file=yt.streams.filter(only_audio=True).first()
            select_file.download('Audios/')


root = Tk()
obj = Youtube_download(root)
root.mainloop()
