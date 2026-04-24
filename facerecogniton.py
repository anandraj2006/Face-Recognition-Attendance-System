from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import os
import time
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    import winsound
import threading


class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")

        self.running = False
        self.marked_today = set()

        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 1.0)
            except:
                self.tts_engine = None
        else:
            self.tts_engine = None

        img_frame = Frame(self.root, height=150, bd=0, bg="white", highlightthickness=0)
        img_frame.pack(side=TOP, fill=X)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_columnconfigure(2, weight=1)

        img = Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img = img.resize((510,150),Image.LANCZOS)
        self.photoimage = ImageTk.PhotoImage(img)

        f_label = Label(img_frame,image=self.photoimage,bd=0, highlightthickness=0)
        f_label.grid(row=0, column=0, sticky="nsew")

        img1 = Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img1 = img1.resize((510,150),Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)

        f_label1 = Label(img_frame,image=self.photoimage1,bd=0, highlightthickness=0)
        f_label1.grid(row=0, column=1, sticky="nsew")

        img2 = Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\home.png")
        img2 = img2.resize((510,150),Image.LANCZOS)
        self.photoimage2 = ImageTk.PhotoImage(img2)

        f_label2 = Label(img_frame,image=self.photoimage2,bd=0, highlightthickness=0)
        f_label2.grid(row=0, column=2, sticky="nsew")

        img3 = Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\bgimg.jpeg")
        img3 = img3.resize((1530,690),Image.LANCZOS)
        self.photoimage3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root,image=self.photoimage3,bd=0,highlightthickness=0)
        bg_img.place(x=0,y=150,relwidth=1,relheight=1)

        title_lbl = Label(bg_img,text="ATTENDANCE MANAGEMENT SYSTEM",
                          font=("times new roman",30,"bold"),bg="white",fg="purple")
        title_lbl.pack(fill=X)

        info_frame = LabelFrame(self.root,bd=2,relief=RIDGE,
                                text="Recognition Status",
                                font=("times new roman",12,"bold"),bg="white")
        info_frame.place(x=20,y=220,width=400,height=530)

        self.status_label = Label(info_frame,text="Status: Camera Ready",
                                  font=("Segoe UI",16,"bold"),
                                  fg="blue",bg="white")
        self.status_label.pack(pady=30)

        self.name_label = Label(info_frame,text="Name: ---",
                                font=("Segoe UI",14),bg="white")
        self.name_label.pack(pady=10)

        self.time_label = Label(info_frame,text="Time: ---",
                                font=("Segoe UI",14),bg="white")
        self.time_label.pack(pady=10)

        Button(info_frame,text="Take Attendance",
               font=("times new roman",14,"bold"),
               bg="green",fg="white",
               command=self.start_camera).pack(pady=20,ipadx=20)

        Button(info_frame,text="Stop Camera",
               font=("times new roman",14,"bold"),
               bg="red",fg="white",
               command=self.stop_camera).pack(pady=10,ipadx=30)

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        try:
            self.recognizer.read("classifier.xml")
        except:
            print("classifier.xml not found")

        self.camera_window = None
        self.cap = None


    def start_camera(self):

        if self.running:
            return

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            messagebox.showerror("Camera Error","Cannot open camera")
            return

        self.running = True

        self.camera_window = Toplevel(self.root)
        self.camera_window.title("Live Camera - Face Recognition")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = screen_width // 2
        window_height = screen_height
        x_position = screen_width // 2

        self.camera_window.geometry(f"{window_width}x{window_height}+{x_position}+0")
        self.camera_window.configure(bg="black")

        self.video_label = Label(self.camera_window,bg="black")
        self.video_label.pack(fill=BOTH,expand=True)

        self.camera_window.protocol("WM_DELETE_WINDOW",self.stop_camera)

        self.status_label.config(text="Status: Scanning Faces...",fg="blue")

        self.update_frame()


    def stop_camera(self):

        self.running = False

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()

        if self.camera_window:
            self.camera_window.destroy()

        self.status_label.config(text="Status: Camera Stopped",fg="blue")


    def update_frame(self):

        if not self.running:
            return

        ret, frame = self.cap.read()

        if not ret:
            self.root.after(20,self.update_frame)
            return

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            id_, conf = self.recognizer.predict(gray[y:y+h,x:x+w])

            confidence = int(100*(1-conf/300))

            name = self.get_student_name(id_)

            # FIXED CONDITION
            if confidence>70 and name!="Unknown":

                if id_ not in self.marked_today:
                    self.mark_attendance(id_,name)
                    self.marked_today.add(id_)

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,name,(x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

            else:

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.putText(frame,"Unknown",(x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(img)

        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)

        self.root.after(20,self.update_frame)


    def get_student_name(self,student_id):

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )

            cur = conn.cursor()

            cur.execute(
                "SELECT name FROM students WHERE student_id=%s",
                (student_id,)
            )

            result = cur.fetchone()
            conn.close()

            if result:
                return result[0]
            else:
                return "Unknown"

        except:
            return "Unknown"


    def mark_attendance(self,student_id,name):

        today = datetime.now().strftime("%d-%m-%Y")
        now_time = datetime.now().strftime("%H:%M:%S")

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )

            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM attendance WHERE attendance_id=%s AND date=%s",
                (student_id,today)
            )

            if cur.fetchone():
                self.status_label.config(text="Status: Already Marked Today",fg="orange")
                self.name_label.config(text=f"Name: {name}")
                conn.close()
                return

            cur.execute(
            """INSERT INTO attendance 
            (attendance_id, roll, name, department, time, date, attendance, source)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (student_id, student_id, name,"CSE", now_time, today, "Present", "Face")

            )
 
            conn.commit()
            conn.close()

            self.status_label.config(text="Status: Attendance Marked ✓",fg="green")
            self.name_label.config(text=f"Name: {name}")
            self.time_label.config(text=f"Time: {now_time}")

        except Exception as e:
            print(e)


if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()