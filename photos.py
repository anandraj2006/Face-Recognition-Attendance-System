from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from tkcalendar import Calendar
from datetime import date
from tkinter import filedialog
import csv
from datetime import datetime



class Photos:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")
        # self.attendance_data = []  # stores attendance records


        img_frame = Frame(self.root,height=150,bd=0,bg="white", highlightthickness=0)
        img_frame.pack(side=TOP, fill=X)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_columnconfigure(2, weight=1)
        # img_frame.place(x=0, y=0, width=1530, height=150)


        # img1
        img=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img=img.resize((510,150),Image.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img)

        f_label=Label(img_frame,image=self.photoimage,bd=0, highlightthickness=0)
        f_label.grid(row=0, column=0, sticky="nsew")

        # img2
        img1=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img1=img1.resize((510,150),Image.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)

        f_label1=Label(img_frame,image=self.photoimage1,bd=0, highlightthickness=0)
        f_label1.grid(row=0, column=1, sticky="nsew")

        # img3
        img2=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img2=img2.resize((510,150),Image.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)

        f_label2=Label(img_frame,image=self.photoimage2,bd=0, highlightthickness=0)
        f_label2.grid(row=0, column=2, sticky="nsew")

        # bg_img
        img3=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\bgimg.jpeg")
        img3=img3.resize((1530,690),Image.LANCZOS)
        self.photoimage3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimage3,bd=0,highlightthickness=0)
        bg_img.place(x=0,y=150,relwidth=1,relheight=1)

        title_lbl=Label(bg_img,text="PHOTOS ", font=("times new roman",30,"bold"),bg="white",fg="purple",justify="center")
        title_lbl.pack(fill=X)
        
if __name__ == "__main__":
    root=Tk()
    obj=Photos(root)
    root.mainloop()