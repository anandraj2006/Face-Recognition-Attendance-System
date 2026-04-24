import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import mysql.connector
import cv2
import os

# Project root (one level up from src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICTURES_DIR = os.path.join(BASE_DIR, "pictures")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "src", "models")

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "piddii51242",
    "database": "mydb"
}


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")

        # variables
        self.var_dep = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_sem = tk.StringVar()
        self.var_std_id = tk.StringVar()
        self.var_std_name = tk.StringVar()
        self.var_sec = tk.StringVar()
        self.var_roll = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_search_by = tk.StringVar()
        self.var_search_txt = tk.StringVar()

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

        title_lbl = Label(bg_img, text="STUDENT MANAGEMENT SYSTEM ", font=("times new roman", 30, "bold"), bg="white", fg="purple", justify="center")
        title_lbl.pack(fill=X)

        # === Left frame ===
        left_frame = tk.LabelFrame(bg_img, bd=2, relief="ridge", text="STUDENT DETAILS", font=("times new roman", 12, "italic"))
        left_frame.place(x=20, y=60, width=610, height=420)

        # === Right frame ===
        right_frame = tk.LabelFrame(bg_img, bd=2, relief="ridge", text="", font=("times new roman", 12, "bold"))
        right_frame.place(x=640, y=60, width=610, height=420)

        # current course
        current_course = tk.LabelFrame(left_frame, bd=2, relief="ridge", text="Current Course Details", font=("times new roman", 12, "bold"))
        current_course.place(x=20, y=10, width=550, height=110)

        dept_label = tk.Label(current_course, text="Department Details", font=("georgia", 12,))
        dept_label.grid(row=0, column=0, padx=5, pady=10, sticky=W)
        dept_combo = ttk.Combobox(current_course, font=("georgia", 12), width=12, state="readonly", textvariable=self.var_dep)
        dept_combo["values"] = ("Select Department", "C.S.E.", "IT", "ECE", "ELECTRICAL", "MECHANICAL", "CIVIL", "PRINTING")
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        course_label = tk.Label(current_course, text="Course", font=("georgia", 12,))
        course_label.grid(row=0, column=2, padx=5, sticky=W)
        course_combo = ttk.Combobox(current_course, font=("georgia", 12), width=12, state="readonly", textvariable=self.var_course)
        course_combo["values"] = ("Select Course", "AI", "ML", "IoT", "VLSI")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        year_label = tk.Label(current_course, text="Year", font=("georgia", 12,))
        year_label.grid(row=1, column=0, padx=5, sticky=W)
        year_combo = ttk.Combobox(current_course, font=("georgia", 12), width=12, state="readonly", textvariable=self.var_year)
        year_combo["values"] = ("Select year", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26", "2026-27")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        sem_label = tk.Label(current_course, text="semester", font=("georgia", 12,))
        sem_label.grid(row=1, column=2, padx=5, sticky=W)
        sem_combo = ttk.Combobox(current_course, font=("georgia", 12), width=12, state="readonly", textvariable=self.var_sem)
        sem_combo["values"] = ("Select Semester", "1st Semester", "2nd Semester", "3rd Semester", "4th Semester", "5th Semester", "6th Semester", "7th Semester", "8th Semester")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        class_student = tk.LabelFrame(left_frame, bd=2, relief="ridge", text="Class Student Information", font=("times new roman", 12, "bold"))
        class_student.place(x=20, y=130, width=550, height=270)

        tk.Label(class_student, text="Student ID:", font=("georgia", 12,)).grid(row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student, width=20, font=("georgia", 12,), textvariable=self.var_std_id).grid(row=0, column=1, padx=10, pady=5, sticky=W)

        tk.Label(class_student, text="Student Name:", font=("georgia", 12,)).grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student, width=20, font=("georgia", 12,), textvariable=self.var_std_name).grid(row=1, column=1, padx=10, pady=5, sticky=W)

        tk.Label(class_student, text="Section:", font=("georgia", 12,)).grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student, width=20, font=("georgia", 12,), textvariable=self.var_sec).grid(row=2, column=1, padx=10, pady=5, sticky=W)

        tk.Label(class_student, text="Roll:", font=("georgia", 12,)).grid(row=3, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student, width=20, font=("georgia", 12,), textvariable=self.var_roll).grid(row=3, column=1, padx=10, pady=5, sticky=W)

        tk.Label(class_student, text="Email:", font=("georgia", 12,)).grid(row=4, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_student, width=20, font=("georgia", 12,), textvariable=self.var_email).grid(row=4, column=1, padx=10, pady=5, sticky=W)

        self.var_radio1 = tk.StringVar(value="No")
        radbutton1 = ttk.Radiobutton(class_student, text="Take Sample Photo", variable=self.var_radio1, value="Yes")
        radbutton1.grid(row=5, column=0, padx=10, pady=2)
        radbutton2 = ttk.Radiobutton(class_student, text="No Photo Sample", variable=self.var_radio1, value="No")
        radbutton2.grid(row=5, column=1, padx=10, pady=2)

        button_frame = tk.LabelFrame(class_student, bd=2, relief="ridge", text="")
        button_frame.place(x=10, y=200, width=525, height=40)

        save_button = Button(button_frame, text="Save", command=self.save_data, font=("georgia", 12,), bg="#48CAE4", fg="white")
        save_button.grid(column=0, row=0, padx=7, pady=2)
        update_button = Button(button_frame, text="Update", font=("georgia", 12,), bg="#48CAE4", fg="white", command=self.update)
        update_button.grid(column=1, row=0, padx=7, pady=2)
        delete_button = Button(button_frame, text="Delete", font=("georgia", 12,), bg="#48CAE4", fg="white", command=self.delete_data)
        delete_button.grid(column=2, row=0, padx=7, pady=2)
        reset_button = Button(button_frame, text="Reset", font=("georgia", 12,), bg="#48CAE4", fg="white", command=self.reset_data)
        reset_button.grid(column=3, row=0, padx=7, pady=2)
        take_photo_button = Button(button_frame, text="Take Photo", font=("georgia", 12,), bg="#48CAE4", fg="white", command=self.generate_Dataset)
        take_photo_button.grid(column=4, row=0, padx=7, pady=2)
        update_photo_button = Button(button_frame, text="Update Photo", font=("georgia", 12,), bg="#48CAE4", fg="white", command=self.generate_Dataset)
        update_photo_button.grid(column=5, row=0, padx=7, pady=2)

        def toggle_photo_button(*args):
            if self.var_radio1.get() == "No":
                take_photo_button.config(state=DISABLED)
                update_photo_button.config(state=DISABLED)
            else:
                take_photo_button.config(state=NORMAL)
                update_photo_button.config(state=NORMAL)

        self.var_radio1.trace_add("write", toggle_photo_button)
        toggle_photo_button()

        # search system
        search_frame = tk.LabelFrame(right_frame, bd=2, relief="ridge", text="Search system", font=("times new roman", 12, "bold"))
        search_frame.place(x=20, y=10, width=550, height=70)
        tk.Label(search_frame, text="Search by:", font=("georgia", 12,)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        search_combo = ttk.Combobox(search_frame, font=("georgia", 12), width=7, state="readonly", textvariable=self.var_search_by)
        search_combo["values"] = ("Select", "Roll no.", "E-mail")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        ttk.Entry(search_frame, width=12, font=("georgia", 12,), textvariable=self.var_search_txt).grid(row=0, column=2, padx=10, pady=5, sticky=W)
        Button(search_frame, text="Search", width=10, font=("georgia", 12,), bg="#48CAE4", fg="white", command=self.search_data).grid(column=3, row=0, padx=1, pady=2)
        Button(search_frame, text="Show all", width=10, font=("georgia", 12,), bg="#48CAE4", fg="white", command=lambda: [self.fetchdata(), self.var_search_txt.set(""), self.var_search_by.set("Select")]).grid(column=4, row=0, padx=1, pady=2)

        # table frame
        table_frame = tk.LabelFrame(right_frame, bd=2, relief="ridge", font=("georgia", 12, "bold"))
        table_frame.place(x=20, y=85, width=550, height=160)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.student_table = ttk.Treeview(table_frame, column=("dept", "course", "year", "semester", "stu_id", "name", "sec", "roll no", "email"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dept", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("semester", text="Semester")
        self.student_table.heading("stu_id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("sec", text="Section")
        self.student_table.heading("roll no", text="Roll no.")
        self.student_table.heading("email", text="email")
        self.student_table["show"] = "headings"
        for col in ("dept", "course", "year", "semester", "stu_id", "name", "sec", "roll no", "email"):
            self.student_table.column(col, width=100, anchor="center")
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetchdata()

    def save_data(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if (self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or
                self.var_std_id.get() == "" or self.var_course.get() == "Select Course" or
                self.var_year.get() == "Select year" or self.var_sem.get() == "Select Semester" or
                self.var_roll.get() == "" or self.var_sec.get() == "" or self.var_email.get() == ""):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        if not self.var_std_id.get().isdigit():
            messagebox.showerror("Error", "Student ID must be numeric", parent=self.root)
            return
        elif not re.match(email_pattern, self.var_email.get()):
            messagebox.showerror("Error", "Invalid Email!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(**db_config)
                cur = conn.cursor()
                cur.execute("SELECT student_id FROM students WHERE student_id=%s", (self.var_std_id.get(),))
                if cur.fetchone():
                    messagebox.showerror("Error", "Student ID already exists!", parent=self.root)
                    conn.close()
                    return
                cur.execute(
                    "insert into students(department,course,year,semester,student_id,name,section,roll,email,photo_sample) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (self.var_dep.get(), self.var_course.get(), self.var_year.get(), self.var_sem.get(),
                     self.var_std_id.get(), self.var_std_name.get(), self.var_sec.get(),
                     self.var_roll.get(), self.var_email.get(), self.var_radio1.get())
                )
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Success", "Student data saved", parent=self.root)
                self.fetchdata()
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def fetchdata(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cur = conn.cursor()
            cur.execute("SELECT department, course, year, semester, student_id, name, section, roll, email FROM students")
            row = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for i in row:
                self.student_table.insert("", END, values=i)
            self.student_table.update_idletasks()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)
        finally:
            if conn.is_connected():
                cur.close()
                conn.close()

    def get_cursor(self, event=""):
        cur_focus = self.student_table.focus()
        if cur_focus == "":
            return
        content = self.student_table.item(cur_focus)
        data = content["values"]
        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_sem.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_sec.set(data[6])
        self.var_roll.set(data[7])
        self.var_email.set(data[8])

    def update(self):
        if (self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or
                self.var_std_id.get() == "" or self.var_course.get() == "Select Course" or
                self.var_year.get() == "Select year" or self.var_sem.get() == "Select Semester" or
                self.var_roll.get() == "" or self.var_sec.get() == "" or self.var_email.get() == ""):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        if not self.var_std_id.get().isdigit():
            messagebox.showerror("Error", "Student ID must be numeric", parent=self.root)
            return
        else:
            try:
                if not messagebox.askyesno("Confirm Update", "Do you want to update this student record?", parent=self.root):
                    return
                conn = mysql.connector.connect(**db_config)
                cur = conn.cursor()
                cur.execute("""UPDATE students SET department=%s, course=%s, year=%s, semester=%s,
                    name=%s, section=%s, roll=%s, email=%s, photo_sample=%s WHERE student_id=%s""",
                            (self.var_dep.get(), self.var_course.get(), self.var_year.get(), self.var_sem.get(),
                             self.var_std_name.get(), self.var_sec.get(), self.var_roll.get(),
                             self.var_email.get(), self.var_radio1.get(), self.var_std_id.get()))
                conn.commit()
                cur.close()
                conn.close()
                self.fetchdata()
                messagebox.showinfo("Success", "Student record updated successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Update failed due to: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
        else:
            try:
                if messagebox.askyesno("Student detail page", "Do you want to delete this student info", parent=self.root):
                    conn = mysql.connector.connect(**db_config)
                    cur = conn.cursor()
                    cur.execute("delete from students where student_id=%s", (self.var_std_id.get(),))
                    conn.commit()
                    self.fetchdata()
                    conn.close()
                    messagebox.showinfo("Delete", "Successfully deleted", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Delete failed due to: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_std_name.set("")
        self.var_std_id.set("")
        self.var_course.set("Select Course")
        self.var_year.set("Select year")
        self.var_sem.set("Select Semester")
        self.var_roll.set("")
        self.var_sec.set("")
        self.var_email.set("")

    def generate_Dataset(self):
        if self.var_radio1.get() == "No":
            messagebox.showwarning("Photo Sample Disabled", "Please select 'Take Sample Photo' to capture images.", parent=self.root)
            return
        if (self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or
                self.var_std_id.get() == "" or self.var_course.get() == "Select Course" or
                self.var_year.get() == "Select year" or self.var_sem.get() == "Select Semester" or
                self.var_roll.get() == "" or self.var_sec.get() == "" or self.var_email.get() == ""):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(**db_config)
                cur = conn.cursor()
                id = self.var_std_id.get()
                cur.execute("""UPDATE students SET department=%s, course=%s, year=%s, semester=%s,
                    name=%s, section=%s, roll=%s, email=%s, photo_sample=%s WHERE student_id=%s""",
                            (self.var_dep.get(), self.var_course.get(), self.var_year.get(), self.var_sem.get(),
                             self.var_std_name.get(), self.var_sec.get(), self.var_roll.get(),
                             self.var_email.get(), self.var_radio1.get(), self.var_std_id.get()))
                conn.commit()
                self.fetchdata()
                self.reset_data()
                conn.close()

                # Use the bundled haarcascade model from src/models/
                cascade_path = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
                face_classifier = cv2.CascadeClassifier(cascade_path)

                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        face = img[y:y + h, x:x + w]
                        return face
                    return None

                # Make dataset folder if not present
                if not os.path.exists(DATA_DIR):
                    os.makedirs(DATA_DIR)

                cap = cv2.VideoCapture(0)
                img_id = 0

                while True:
                    ret, my_frame = cap.read()
                    if not ret:
                        break
                    face = face_cropped(my_frame)
                    if face is not None:
                        img_id += 1
                        face = cv2.resize(face, (450, 450))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path = os.path.join(DATA_DIR, f"user.{id}.{img_id}.jpg")
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        cv2.imshow("Cropped Face", face)
                    if cv2.waitKey(1) == 13 or img_id == 25:
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Dataset generated successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Update failed due to: {str(es)}", parent=self.root)

    def search_data(self):
        if self.var_search_by.get() == "Select" or self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Select search criteria and enter value", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(**db_config)
            cur = conn.cursor()
            if self.var_search_by.get() == "Roll no.":
                cur.execute("SELECT department, course, year, semester, student_id, name, section, roll, email FROM students WHERE roll=%s", (self.var_search_txt.get(),))
            else:
                cur.execute("SELECT department, course, year, semester, student_id, name, section, roll, email FROM students WHERE email=%s", (self.var_search_txt.get(),))
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", END, values=row)
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"{es}", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    obj = Student(root)
    root.mainloop()
