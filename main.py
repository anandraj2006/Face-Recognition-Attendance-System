from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from src.student import Student
from src.attendance import Attendance
from src.train import Train
from src.helpdesk import Help_desk
from src.facerecogniton import FaceRecognition

# Project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURES_DIR = os.path.join(BASE_DIR, "pictures")


class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")

        img_frame = Frame(self.root, height=150, bd=0, bg="white", highlightthickness=0)
        img_frame.pack(side=TOP, fill=X)
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_columnconfigure(2, weight=1)

        # img1
        img = Image.open(os.path.join(PICTURES_DIR, "home.png"))
        img = img.resize((510, 150), Image.LANCZOS)
        self.photoimage = ImageTk.PhotoImage(img)
        f_label = Label(img_frame, image=self.photoimage, bd=0, highlightthickness=0)
        f_label.grid(row=0, column=0, sticky="nsew")

        # img2
        img1 = Image.open(os.path.join(PICTURES_DIR, "home.png"))
        img1 = img1.resize((510, 150), Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        f_label1 = Label(img_frame, image=self.photoimage1, bd=0, highlightthickness=0)
        f_label1.grid(row=0, column=1, sticky="nsew")

        # img3
        img2 = Image.open(os.path.join(PICTURES_DIR, "home.png"))
        img2 = img2.resize((510, 150), Image.LANCZOS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        f_label2 = Label(img_frame, image=self.photoimage2, bd=0, highlightthickness=0)
        f_label2.grid(row=0, column=2, sticky="nsew")

        # bg_img
        img3 = Image.open(os.path.join(PICTURES_DIR, "bgimg.jpeg"))
        img3 = img3.resize((1530, 690), Image.LANCZOS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        bg_img = Label(self.root, image=self.photoimage3, bd=0, highlightthickness=0)
        bg_img.place(x=0, y=150, relwidth=1, relheight=1)

        title_lbl = Label(bg_img, text="FACE RECOGNITION ATTENDANCE SYSTEM ", font=("times new roman", 30, "bold"), bg="white", fg="purple", justify="center")
        title_lbl.pack(fill=X)

        # student button
        img4 = Image.open(os.path.join(PICTURES_DIR, "student.jpeg"))
        img4 = img4.resize((150, 150), Image.LANCZOS)
        self.photoimage4 = ImageTk.PhotoImage(img4)
        b1 = Button(bg_img, image=self.photoimage4, cursor="hand2", command=self.student_data)
        b1.place(x=150, y=80, width=150, height=150)
        Button(bg_img, text="Student", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white", command=self.student_data).place(x=150, y=230, width=150, height=35)

        # face recognition button
        img5 = Image.open(os.path.join(PICTURES_DIR, "face_recognition.jpeg"))
        img5 = img5.resize((150, 150), Image.LANCZOS)
        self.photoimage5 = ImageTk.PhotoImage(img5)
        b2 = Button(bg_img, image=self.photoimage5, cursor="hand2", command=self.face_recognition)
        b2.place(x=410, y=80, width=150, height=150)
        Button(bg_img, text="Face Recognition", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white", command=self.face_recognition).place(x=410, y=230, width=150, height=35)

        # attendance
        img6 = Image.open(os.path.join(PICTURES_DIR, "attandance.jpeg"))
        img6 = img6.resize((150, 150), Image.LANCZOS)
        self.photoimage6 = ImageTk.PhotoImage(img6)
        b3 = Button(bg_img, image=self.photoimage6, cursor="hand2", command=self.attendance_data)
        b3.place(x=670, y=80, width=150, height=150)
        Button(bg_img, text="Attendance", cursor="hand2", command=self.attendance_data, font=("times new roman", 12, "bold"), bg="royalblue3", fg="white").place(x=670, y=230, width=150, height=35)

        # helpdesk
        img7 = Image.open(os.path.join(PICTURES_DIR, "helpdesk.jpeg"))
        img7 = img7.resize((150, 150), Image.LANCZOS)
        self.photoimage7 = ImageTk.PhotoImage(img7)
        b4 = Button(bg_img, image=self.photoimage7, cursor="hand2", command=self.helpdesk)
        b4.place(x=930, y=80, width=150, height=150)
        Button(bg_img, text="Help Desk", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white", command=self.helpdesk).place(x=930, y=230, width=150, height=35)

        # train data
        img8 = Image.open(os.path.join(PICTURES_DIR, "traindata.jpeg"))
        img8 = img8.resize((150, 150), Image.LANCZOS)
        self.photoimage8 = ImageTk.PhotoImage(img8)
        b5 = Button(bg_img, image=self.photoimage8, cursor="hand2", command=self.train_data)
        b5.place(x=150, y=300, width=150, height=150)
        Button(bg_img, text="Train Data", cursor="hand2", command=self.train_data, font=("times new roman", 12, "bold"), bg="royalblue3", fg="white").place(x=150, y=440, width=150, height=35)

        # photos
        img9 = Image.open(os.path.join(PICTURES_DIR, "photos.jpeg"))
        img9 = img9.resize((150, 150), Image.LANCZOS)
        self.photoimage9 = ImageTk.PhotoImage(img9)
        b6 = Button(bg_img, image=self.photoimage9, cursor="hand2")
        b6.place(x=410, y=300, width=150, height=150)
        Button(bg_img, text="Photos", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white").place(x=410, y=440, width=150, height=35)

        # developer
        img10 = Image.open(os.path.join(PICTURES_DIR, "developer.jpeg"))
        img10 = img10.resize((150, 150), Image.LANCZOS)
        self.photoimage10 = ImageTk.PhotoImage(img10)
        b7 = Button(bg_img, image=self.photoimage10, cursor="hand2")
        b7.place(x=670, y=300, width=150, height=150)
        Button(bg_img, text="Developer", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white").place(x=670, y=440, width=150, height=35)

        # exit button
        img11 = Image.open(os.path.join(PICTURES_DIR, "exit.jpeg"))
        img11 = img11.resize((150, 150), Image.LANCZOS)
        self.photoimage11 = ImageTk.PhotoImage(img11)
        b8 = Button(bg_img, image=self.photoimage11, cursor="hand2", command=self.exit_app)
        b8.place(x=930, y=300, width=150, height=150)
        Button(bg_img, text="Exit", cursor="hand2", font=("times new roman", 12, "bold"), bg="royalblue3", fg="white", command=self.exit_app).place(x=930, y=440, width=150, height=35)

    def student_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def exit_app(self):
        if messagebox.askyesno("Exit System", "Are you sure you want to exit?"):
            self.root.destroy()

    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = FaceRecognition(self.new_window)

    def helpdesk(self):
        self.new_window = Toplevel(self.root)
        self.app = Help_desk(self.new_window)


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
