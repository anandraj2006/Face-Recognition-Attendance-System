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



class Attendance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="white")
        self.create_attendance_table()
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

        title_lbl=Label(bg_img,text="ATTENDANCE MANAGEMENT SYSTEM ", font=("times new roman",30,"bold"),bg="white",fg="purple",justify="center")
        title_lbl.pack(fill=X)
        
        # main_frame=Frame(bg_img,bg="white")
        # main_frame.place(x=20,y=55,width=1229,height=420)
        
        # left frame 
        left_frame=LabelFrame(bg_img,bd=2,bg="white",relief=RIDGE,text="Student Attendance Details",font=("times new roman",12,"bold"))
        left_frame.place(x=20, y=60, width=610, height=420)
        
        img_left=Image.open(r"C:\Users\KIIT0001\OneDrive\Desktop\Face recognition system\pictures\attendance1.jpeg")
        img_left=img_left.resize((585,165),Image.LANCZOS)
        self.photoimage_left=ImageTk.PhotoImage(img_left)

        f_label = Label( left_frame, image=self.photoimage_left, bd=0, highlightthickness=0)
        f_label.place(x=5, y=5,width=585,height=165)
        
        left_inside_frame=Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        left_inside_frame.place(x=5,y=170,width=585,height=220)
        
        # attendanceid 
        attendanceid_label=Label(left_inside_frame,text="Attendance ID",font=("times new roman",12),bg="white")
        attendanceid_label.grid(row=0,column=0,sticky=E)
        
        self.attendanceid_entry=ttk.Entry(left_inside_frame,width=15,font=("Segoe UI",12))
        self.attendanceid_entry.grid(row=0, column=1,padx=(6,50),pady=5,sticky=W)
        
        # roll no
        rollno_label=Label(left_inside_frame,text="Roll",font=("times new roman",12),bg="white")
        rollno_label.grid(row=0,column=3,sticky=E)
        
        self.rollno_entry=ttk.Entry(left_inside_frame,width=15,font=("Segoe UI",12))
        self.rollno_entry.grid(row=0, column=4,padx=10,pady=5,sticky=W)
        
         # name
        name_label=Label(left_inside_frame,text="Name",font=("times new roman",12),bg="white")
        name_label.grid(row=2,column=0,sticky=E)
        
        self.name_entry=ttk.Entry(left_inside_frame,width=15,font=("Segoe UI",12))
        self.name_entry.grid(row=2, column=1,padx=(6,50),pady=5,sticky=W)
        
        # department 
        department_label=Label(left_inside_frame,text="Department",font=("times new roman",12),bg="white")
        department_label.grid(row=2,column=3,sticky=E)
        
        self.department_entry=ttk.Entry(left_inside_frame,width=15,font=("Segoe UI",12))
        self.department_entry.grid(row=2, column=4,padx=10,pady=5,sticky=W)
        
        # time
        time_label=Label(left_inside_frame,text="Time",font=("times new roman",12),bg="white")
        time_label.grid(row=3,column=0,sticky=E)
        
        self.time_var = StringVar()
        time_entry=ttk.Entry(left_inside_frame,width=15,font=("Segoe UI",12),textvariable=self.time_var )
        time_entry.grid(row=3, column=1,padx=(6,50),pady=5,sticky=W)
        
        # to edit the automatically filled time 
        # self.edit_time_var = IntVar()
        # edit_time_chk = Checkbutton(
        #     left_inside_frame,
        #     text="Edit Time",
        #     variable=self.edit_time_var,
        #     bg="white",
        #     command=self.toggle_time_edit
        # )
        # edit_time_chk.grid(row=4, column=1, padx=5, sticky=W)

        
        # date 
        date_label=Label(left_inside_frame,text="Date",font=("times new roman",12),bg="white")
        date_label.grid(row=3,column=3,sticky=E)

        self.date_var = StringVar()
        date_entry = ttk.Entry(left_inside_frame, width=15, font=("Segoe UI",12), textvariable=self.date_var)
        date_entry.grid(row=3, column=4, padx=10, pady=5, sticky=W)

        #to open calendar
        date_entry.bind("<1>", self.open_calendar) #just a click on the entry and the calender will be poped up
        
        now = datetime.now()
        self.date_var.set(now.strftime("%d-%m-%Y"))
        self.time_var.set(now.strftime("%H:%M:%S"))
        # attendance
        attendance_label=Label(left_inside_frame,text="Attendance",font=("times new roman",12),bg="white")
        attendance_label.grid(row=5,column=0,sticky=E)
        
        self.attendance_status=ttk.Combobox(left_inside_frame,width=20,font=("times new roman",12),state="readonly") #readonly-non editable
        self.attendance_status["values"]=("Status","Present","Absent")
        self.attendance_status.grid(row=5,column=1,padx=(0,0))
        self.attendance_status.current(0) #selects value at index 0 as default to display if not selected by the user
        
        # buttons
        b1=Button(left_inside_frame,text="Import csv",cursor="hand2",font=("times new roman",12,"bold"),bg="royalblue3",fg="white",command=self.import_csv)
        b1.place(x=7,y=180,width=110,height=35)
        
        b1=Button(left_inside_frame,text="Export csv",cursor="hand2",font=("times new roman",12,"bold"),bg="royalblue3",fg="white",command=self.export_csv)
        b1.place(x=125,y=180,width=110,height=35)
        
        b1=Button(left_inside_frame,text="Update",cursor="hand2",font=("times new roman",12,"bold"),bg="royalblue3",fg="white",command=self.update_attendance)
        b1.place(x=243,y=180,width=90,height=35)
        
        b1=Button(left_inside_frame,text="Reset",cursor="hand2",font=("times new roman",12,"bold"),bg="royalblue3",fg="white",command=self.reset_fields)
        b1.place(x=341,y=180,width=90,height=35)
        
        b1=Button(left_inside_frame,text="Mark Attendance",cursor="hand2",font=("times new roman",12,"bold"),bg="royalblue3",fg="white",command=self.mark_attendance)
        b1.place(x=439, y=180, width=130, height=35)

        
        # rigth frame 
        right_frame=LabelFrame(bg_img,bd=2,bg="white",relief=RIDGE,text="Attendance Details",font=("times new roman",12,"bold"))
        right_frame.place(x=640, y=60, width=615, height=420)
        
        table_frame=Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=3,width=600,height=388)
        
        table_scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        table_scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        
        self.Attendancereport=ttk.Treeview(table_frame,columns=("id","roll","name","department","time","date","attendance","source"),xscrollcommand=table_scroll_x.set,yscrollcommand=table_scroll_y.set)
        
        table_scroll_x.pack(side=BOTTOM,fill=X)
        table_scroll_y.pack(side=RIGHT,fill=Y)
        
        table_scroll_x.config(command=self.Attendancereport.xview)
        table_scroll_y.config(command=self.Attendancereport.yview) #i can also add this feature directly unto table_scroll_x 
        
        self.Attendancereport.heading("id",text="Attendance Id")
        self.Attendancereport.heading("roll",text="Roll No")
        self.Attendancereport.heading("name",text="Name")
        self.Attendancereport.heading("department",text="Department")
        self.Attendancereport.heading("time",text="Time")
        self.Attendancereport.heading("date",text="Date")
        self.Attendancereport.heading("attendance",text="Attendance")
        self.Attendancereport.heading("source", text="Source")

        
        self.Attendancereport["show"] = "headings"  # this hides the first empty column 

        self.Attendancereport.column("id", width=100,anchor=CENTER)
        self.Attendancereport.column("roll", width=100,anchor=CENTER)
        self.Attendancereport.column("name", width=150,anchor=CENTER)
        self.Attendancereport.column("department", width=150,anchor=CENTER)
        self.Attendancereport.column("time", width=100,anchor=CENTER)
        self.Attendancereport.column("date", width=100,anchor=CENTER)
        self.Attendancereport.column("attendance", width=120,anchor=CENTER)
        self.Attendancereport.column("source", width=100, anchor=CENTER)

        
        self.Attendancereport.pack(fill=BOTH, expand=1) # makes the table visible inside the frame 
        self.Attendancereport.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()




        
    def open_calendar(self, event):
            # Create a popup window
            top = Toplevel(self.root)
            top.grab_set()  # makes popup modal
            top.geometry("300x300+500+200")
            
            today=date.today()

            # Create a calendar inside the popup
            cal = Calendar(top, selectmode='day', year=today.year, month=today.month, day=today.day)
            cal.pack(pady=20)

            # Button to select the date
            def select_date():
                selected_date = cal.selection_get()  # datetime.date object
                formatted_date = selected_date.strftime("%d-%m-%Y")  # format as dd-mm-yyyy
                self.date_var.set(formatted_date)  # update the Entry
                top.destroy()  # close the popup

            Button(top, text="Select Date", command=select_date).pack(pady=10)   
            
    #create attendance table without visiting MYSQL to create one 
    def create_attendance_table(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )
            cur = conn.cursor()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id VARCHAR(20) PRIMARY KEY,
                roll VARCHAR(20),
                name VARCHAR(100),
                department VARCHAR(50),
                time VARCHAR(20),
                date VARCHAR(20),
                attendance VARCHAR(10),
                source VARCHAR(10) DEFAULT 'Face',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            conn.commit()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    
    # def toggle_time_edit(self):
    #     if self.edit_time_var.get() == 1:
    #         self.time_entry.config(state="normal")   # unlock
    #     else:
    #         self.time_entry.config(state="readonly") # lock
          
    def import_csv(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file:
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )
            cur = conn.cursor()

            with open(file, newline="", encoding="utf-8-sig") as f:
                reader = csv.reader(f)

                next(reader)  # skip header

                for row in reader:

                    if len(row) < 8:
                        continue

                    row = row[:8]

                    cur.execute("""
                    INSERT IGNORE INTO attendance
                    (attendance_id, roll, name, department, time, date, attendance, source)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                            row[0],
                            row[1],
                            row[2],
                            row[3],
                            str(row[4]),
                            row[5],
                            row[6],
                            row[7]
                        ))

            conn.commit()
            conn.close()

            self.fetch_data()

            messagebox.showinfo("Success", "CSV imported successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )
            cur = conn.cursor()

            cur.execute("""
                SELECT attendance_id, roll, name, department, time, date, attendance, source
                FROM attendance
            """)
            rows = cur.fetchall()

            self.Attendancereport.delete(*self.Attendancereport.get_children())
            for row in rows:
                self.Attendancereport.insert("", END, values=row)

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    
    def export_csv(self):
        try:
            file = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Attendance CSV"
            )
            if not file:
                return

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )
            cur = conn.cursor()

            cur.execute("""
                SELECT attendance_id, roll, name, department, time, date, attendance, source
                FROM attendance
            """)
            rows = cur.fetchall()

            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)

                # CSV header
                writer.writerow([
                    "attendance_id",
                    "roll",
                    "name",
                    "department",
                    "time",
                    "date",
                    "attendance",
                    "source"
                ])

                # CSV data
                for row in rows:
                    writer.writerow(row)

            conn.close()
            messagebox.showinfo("Success", "Attendance exported successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    
    def get_cursor(self, event=""):
        selected = self.Attendancereport.focus()
        if not selected:
            return

        data = self.Attendancereport.item(selected, "values")
        
        self.selected_attendance_id = data[0]
        self.selected_date = data[5]

        # Fill fields
        self.attendanceid_entry.delete(0, END)
        self.attendanceid_entry.insert(0, data[0])

        self.rollno_entry.delete(0, END)
        self.rollno_entry.insert(0, data[1])

        self.name_entry.delete(0, END)
        self.name_entry.insert(0, data[2])

        self.department_entry.delete(0, END)
        self.department_entry.insert(0, data[3])

        self.time_var.set(data[4])
        self.date_var.set(data[5])
        self.attendance_status.set(data[6])
        
    
    def update_attendance(self):
        # 1️⃣ Ensure a row is selected
        if not hasattr(self, "selected_attendance_id") or not self.selected_attendance_id:
            messagebox.showerror(
                "Error",
                "Please select a record from the table to update",
                parent=self.root
            )
            return
        
        if not messagebox.askyesno("Confirm", "Update attendance?"):
            return

        # 2️⃣ Validate attendance status
        status = self.attendance_status.get()
        if status == "Status":
            messagebox.showerror(
                "Error",
                "Please select attendance status",
                parent=self.root
            )
            return
        

        # 3️⃣ Generate new update time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )
            cur = conn.cursor()

            # 4️⃣ Update EXACT record (id + original date)
            cur.execute(
                """
                UPDATE attendance
                SET roll = %s,
                    name = %s,
                    department = %s,
                    attendance = %s,
                    time = %s,
                    source = 'Manual'
                WHERE attendance_id = %s
                """,
                (
                    self.rollno_entry.get().strip(),
                    self.name_entry.get().strip(),
                    self.department_entry.get().strip(),
                    status,
                    current_time,
                    self.selected_attendance_id
                )
            )
            
            if cur.rowcount == 0:
                messagebox.showerror(
                    "Update Failed",
                    "No record was updated. Please reselect the row.",
                    parent=self.root
                )
                conn.close()
                return

            conn.commit()
            conn.close()

            # 5️⃣ Update UI
            self.time_var.set(current_time)
            self.fetch_data()

            messagebox.showinfo(
                "Updated",
                "Attendance updated successfully",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.root
            )


    
    def reset_fields(self):
        # Clear entry fields
        self.attendanceid_entry.delete(0, END)
        self.rollno_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.department_entry.delete(0, END)

        # Reset attendance dropdown
        self.attendance_status.current(0)

        # Clear TreeView selection
        self.Attendancereport.selection_remove(self.Attendancereport.selection())

        # Clear stored selected record (important for update safety)
        self.selected_attendance_id = None
        self.selected_date = None
        
    def mark_attendance(self):
        attendance_id = self.attendanceid_entry.get().strip()
        roll = self.rollno_entry.get().strip()
        name = self.name_entry.get().strip()
        department = self.department_entry.get().strip()
        status = self.attendance_status.get()

        if not attendance_id or not roll or not name or not department:
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if status == "Status":
            messagebox.showerror("Error", "Please select attendance status", parent=self.root)
            return

        now = datetime.now()
        current_date = now.strftime("%d-%m-%Y")
        current_time = now.strftime("%H:%M:%S")

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="piddii51242",
                database="mydb"
            )
            cur = conn.cursor()

            # 🔍 Duplicate check (same student, same day)
            cur.execute(
                "SELECT * FROM attendance WHERE attendance_id=%s AND date=%s",
                (attendance_id, current_date)
            )
            if cur.fetchone():
                messagebox.showwarning(
                    "Duplicate",
                    "Attendance already marked for today",
                    parent=self.root
                )
                conn.close()
                return

            # ✅ Insert new attendance
            cur.execute("""
                INSERT INTO attendance
                (attendance_id, roll, name, department, time, date, attendance, source)
                VALUES (%s,%s,%s,%s,%s,%s,%s,'Manual')
            """, (
                attendance_id,
                roll,
                name,
                department,
                current_time,
                current_date,
                status
            ))

            conn.commit()
            conn.close()

            self.fetch_data()
            messagebox.showinfo("Success", "Attendance marked successfully", parent=self.root)
            self.reset_fields()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)


       
        
if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()