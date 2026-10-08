import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
#                     MAIN APPLICATION
# ============================================================

class AdaptiveApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("ADAPTIVE - Personalized Learning System")
        self.geometry("1200x720")
        self.minsize(1000, 650)
        self.configure(bg="#0B1220")

        self.current_user = None
        self.current_role = None

        self.show_login()

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_button(self, parent, text, command, width=20):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Arial", 11, "bold"),
            bg="#1677FF",
            fg="white",
            activebackground="#0D5DD7",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8
        )

    # ========================================================
    #                         LOGIN
    # ========================================================

    def show_login(self):
        self.clear_window()

        main = tk.Frame(self, bg="#0B1220")
        main.pack(fill="both", expand=True)

        # Left branding panel
        left = tk.Frame(main, bg="#101B31", width=600)
        left.pack(side="left", fill="both", expand=True)
        left.pack_propagate(False)

        tk.Label(
            left,
            text="ADAPTIVE",
            font=("Arial", 38, "bold"),
            fg="#38BDF8",
            bg="#101B31"
        ).pack(pady=(150, 10))

        tk.Label(
            left,
            text="AI-Based Personalized Learning\n"
                 "& Student Performance Management System",
            font=("Arial", 17),
            fg="white",
            bg="#101B31",
            justify="center"
        ).pack()

        tk.Label(
            left,
            text="\nLearn • Analyze • Improve",
            font=("Arial", 14, "italic"),
            fg="#94A3B8",
            bg="#101B31"
        ).pack()

        # Right login panel
        right = tk.Frame(main, bg="#0B1220")
        right.pack(side="right", fill="both", expand=True)

        login_box = tk.Frame(
            right,
            bg="#111C30",
            padx=45,
            pady=35
        )
        login_box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            login_box,
            text="LOGIN",
            font=("Arial", 25, "bold"),
            fg="white",
            bg="#111C30"
        ).pack(pady=(0, 25))

        tk.Label(
            login_box,
            text="Login as",
            font=("Arial", 11),
            fg="#94A3B8",
            bg="#111C30"
        ).pack(anchor="w")

        role_var = tk.StringVar(value="Student")

        role_box = ttk.Combobox(
            login_box,
            textvariable=role_var,
            values=["Student", "Teacher / Host"],
            state="readonly",
            width=30,
            font=("Arial", 11)
        )
        role_box.pack(pady=(5, 18), ipady=5)

        tk.Label(
            login_box,
            text="User ID",
            font=("Arial", 11),
            fg="#94A3B8",
            bg="#111C30"
        ).pack(anchor="w")

        user_entry = tk.Entry(
            login_box,
            width=32,
            font=("Arial", 12),
            bg="#1E293B",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        user_entry.pack(pady=(5, 15), ipady=8)

        tk.Label(
            login_box,
            text="Password",
            font=("Arial", 11),
            fg="#94A3B8",
            bg="#111C30"
        ).pack(anchor="w")

        pass_entry = tk.Entry(
            login_box,
            width=32,
            font=("Arial", 12),
            bg="#1E293B",
            fg="white",
            insertbackground="white",
            show="*",
            relief="flat"
        )
        pass_entry.pack(pady=(5, 25), ipady=8)

        def login():
            user_id = user_entry.get().strip()
            password = pass_entry.get().strip()
            role = role_var.get()

            if not user_id or not password:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter User ID and Password."
                )
                return

            # Temporary frontend login
            # Database authentication will be connected later.
            if role == "Teacher / Host":
                self.current_user = user_id
                self.current_role = "teacher"
                self.show_teacher_dashboard()
            else:
                self.current_user = user_id
                self.current_role = "student"
                self.show_student_dashboard()

        self.create_button(
            login_box,
            "LOGIN",
            login,
            width=30
        ).pack()

        tk.Label(
            login_box,
            text="ADAPTIVE • PBL Project",
            font=("Arial", 9),
            fg="#64748B",
            bg="#111C30"
        ).pack(pady=(25, 0))


    # ========================================================
    #                    DASHBOARD BASE
    # ========================================================

    def create_dashboard(self, title, menu_items):

        self.clear_window()

        # Sidebar
        sidebar = tk.Frame(
            self,
            bg="#101B31",
            width=240
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="ADAPTIVE",
            font=("Arial", 23, "bold"),
            fg="#38BDF8",
            bg="#101B31"
        ).pack(pady=(30, 5))

        tk.Label(
            sidebar,
            text="Personalized Learning",
            font=("Arial", 9),
            fg="#64748B",
            bg="#101B31"
        ).pack(pady=(0, 25))

        for name, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=name,
                command=command,
                anchor="w",
                padx=20,
                font=("Arial", 11),
                bg="#101B31",
                fg="#CBD5E1",
                activebackground="#1E3A5F",
                activeforeground="white",
                relief="flat",
                cursor="hand2"
            )
            btn.pack(fill="x", pady=2, ipady=7)

        tk.Button(
            sidebar,
            text="Logout",
            command=self.show_login,
            anchor="w",
            padx=20,
            font=("Arial", 11, "bold"),
            bg="#101B31",
            fg="#F87171",
            activebackground="#3F1D25",
            relief="flat",
            cursor="hand2"
        ).pack(side="bottom", fill="x", pady=20, ipady=8)

        # Main content
        content = tk.Frame(
            self,
            bg="#0B1220"
        )
        content.pack(side="right", fill="both", expand=True)

        header = tk.Frame(
            content,
            bg="#0B1220",
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=title,
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#0B1220"
        ).pack(side="left", padx=30, pady=25)

        tk.Label(
            header,
            text=f"Welcome, {self.current_user}",
            font=("Arial", 11),
            fg="#94A3B8",
            bg="#0B1220"
        ).pack(side="right", padx=30)

        self.content_area = tk.Frame(
            content,
            bg="#0B1220"
        )
        self.content_area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        return self.content_area


    # ========================================================
    #                  STUDENT DASHBOARD
    # ========================================================

    def show_student_dashboard(self):

        menu = [
            ("🏠  Dashboard", self.student_home),
            ("👤  My Profile", self.student_profile),
            ("📚  Subjects", self.student_subjects),
            ("📄  Notes & Notepad", self.student_notes),
            ("📝  Tests", self.student_tests),
            ("📅  My Schedule", self.student_schedule),
            ("🏆  Ranking", self.student_ranking),
            ("📊  Reports", self.student_reports),
        ]

        self.create_dashboard(
            "Student Dashboard",
            menu
        )

        self.student_home()


    def card(self, parent, title, value, subtitle, column):

        box = tk.Frame(
            parent,
            bg="#111C30",
            padx=20,
            pady=18
        )

        box.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        tk.Label(
            box,
            text=title,
            font=("Arial", 10),
            fg="#94A3B8",
            bg="#111C30"
        ).pack(anchor="w")

        tk.Label(
            box,
            text=value,
            font=("Arial", 24, "bold"),
            fg="#38BDF8",
            bg="#111C30"
        ).pack(anchor="w", pady=5)

        tk.Label(
            box,
            text=subtitle,
            font=("Arial", 9),
            fg="#64748B",
            bg="#111C30"
        ).pack(anchor="w")


    def student_home(self):

        for widget in self.content_area.winfo_children():
            widget.destroy()

        stats = tk.Frame(
            self.content_area,
            bg="#0B1220"
        )
        stats.pack(fill="x")

        for i in range(4):
            stats.columnconfigure(i, weight=1)

        self.card(
            stats,
            "Overall Performance",
            "76%",
            "Current average",
            0
        )

        self.card(
            stats,
            "Attendance",
            "84%",
            "Academic attendance",
            1
        )

        self.card(
            stats,
            "Study Hours",
            "18.5h",
            "This week",
            2
        )

        self.card(
            stats,
            "Current Rank",
            "#4",
            "Among students",
            3
        )

        # Today's plan
        plan = tk.Frame(
            self.content_area,
            bg="#111C30",
            padx=25,
            pady=20
        )
        plan.pack(
            fill="both",
            expand=True,
            pady=25
        )

        tk.Label(
            plan,
            text="Today's Recommended Study Plan",
            font=("Arial", 17, "bold"),
            fg="white",
            bg="#111C30"
        ).pack(anchor="w")

        tasks = [
            ("Data Structures - Stack", "60 min", "HIGH"),
            ("Data Structures - Graph", "45 min", "HIGH"),
            ("Python - OOP", "35 min", "MEDIUM"),
            ("DBMS - Revision", "25 min", "LOW"),
        ]

        for topic, time, priority in tasks:

            row = tk.Frame(
                plan,
                bg="#18243A",
                padx=15,
                pady=10
            )
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=topic,
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#18243A"
            ).pack(side="left")

            tk.Label(
                row,
                text=time,
                font=("Arial", 10),
                fg="#94A3B8",
                bg="#18243A"
            ).pack(side="right", padx=15)

            tk.Label(
                row,
                text=priority,
                font=("Arial", 9, "bold"),
                fg="#38BDF8",
                bg="#18243A"
            ).pack(side="right")


    # ========================================================
    #                     STUDENT PROFILE
    # ========================================================

    def student_profile(self):

        self.clear_content()

        self.page_title(
            "My Profile",
            "Your personal and academic information"
        )

        profile = tk.Frame(
            self.content_area,
            bg="#111C30",
            padx=30,
            pady=25
        )
        profile.pack(fill="x", pady=20)

        details = [
            ("Student ID", self.current_user),
            ("Name", "Student Name"),
            ("Course", "BCA (AI & DS)"),
            ("Section", "A3"),
            ("Semester", "4th"),
            ("Attendance", "84%"),
            ("Overall Marks", "76%"),
        ]

        for label, value in details:

            row = tk.Frame(
                profile,
                bg="#111C30"
            )
            row.pack(fill="x", pady=7)

            tk.Label(
                row,
                text=label,
                width=20,
                anchor="w",
                font=("Arial", 11),
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#111C30"
            ).pack(side="left")


    # ========================================================
    #                     SUBJECTS
    # ========================================================

    def student_subjects(self):

        self.clear_content()

        self.page_title(
            "My Subjects",
            "Subjects, units and topics"
        )

        subjects = [
            ("Data Structures", "4 Units", "68% completed"),
            ("Python", "5 Units", "75% completed"),
            ("DBMS", "4 Units", "82% completed"),
            ("Machine Learning", "4 Units", "60% completed"),
        ]

        for name, units, progress in subjects:

            box = tk.Frame(
                self.content_area,
                bg="#111C30",
                padx=20,
                pady=18
            )
            box.pack(fill="x", pady=6)

            tk.Label(
                box,
                text=name,
                font=("Arial", 14, "bold"),
                fg="white",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                box,
                text=f"{units}  •  {progress}",
                font=("Arial", 10),
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="right")


    # ========================================================
    #                       NOTES
    # ========================================================

    def student_notes(self):

        self.clear_content()

        self.page_title(
            "Notes & Notepad",
            "Read study material and create your own notes"
        )

        container = tk.Frame(
            self.content_area,
            bg="#0B1220"
        )
        container.pack(fill="both", expand=True)

        pdf_box = tk.Frame(
            container,
            bg="#111C30",
            padx=20,
            pady=20
        )
        pdf_box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            pdf_box,
            text="📄 PDF Notes",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111C30"
        ).pack(anchor="w")

        tk.Label(
            pdf_box,
            text="\nSelected Topic: Stack\n\n"
                 "PDF reader will be connected here.\n\n"
                 "Teacher-uploaded study material\n"
                 "will appear in this section.",
            font=("Arial", 11),
            fg="#94A3B8",
            bg="#111C30",
            justify="left"
        ).pack(anchor="w", pady=20)

        notes_box = tk.Frame(
            container,
            bg="#111C30",
            padx=20,
            pady=20
        )
        notes_box.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            notes_box,
            text="📝 My Notepad",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#111C30"
        ).pack(anchor="w")

        text = tk.Text(
            notes_box,
            bg="#18243A",
            fg="white",
            insertbackground="white",
            font=("Arial", 11),
            relief="flat",
            wrap="word"
        )
        text.pack(
            fill="both",
            expand=True,
            pady=15
        )

        buttons = tk.Frame(
            notes_box,
            bg="#111C30"
        )
        buttons.pack(fill="x")

        self.create_button(
            buttons,
            "Save Notes",
            lambda: messagebox.showinfo(
                "Saved",
                "Notes saved successfully."
            ),
            width=15
        ).pack(side="left", padx=5)

        self.create_button(
            buttons,
            "Improve with AI",
            lambda: messagebox.showinfo(
                "AI Notes",
                "AI note improvement will be connected in the backend."
            ),
            width=18
        ).pack(side="right", padx=5)


    # ========================================================
    #                       TESTS
    # ========================================================

    def student_tests(self):

        self.clear_content()

        self.page_title(
            "Tests",
            "Assess your knowledge"
        )

        tests = [
            ("Topic-wise Test", "Test a specific topic"),
            ("Unit-wise Test", "Test your complete unit"),
            ("Overall Test", "Test the complete syllabus"),
        ]

        for title, subtitle in tests:

            box = tk.Frame(
                self.content_area,
                bg="#111C30",
                padx=25,
                pady=20
            )
            box.pack(fill="x", pady=7)

            tk.Label(
                box,
                text=title,
                font=("Arial", 15, "bold"),
                fg="white",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                box,
                text=subtitle,
                font=("Arial", 10),
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="left", padx=20)

            self.create_button(
                box,
                "Start Test",
                lambda t=title: messagebox.showinfo(
                    "Test",
                    f"{t} module will be connected to the backend."
                ),
                width=15
            ).pack(side="right")


    # ========================================================
    #                       SCHEDULE
    # ========================================================

    def student_schedule(self):

        self.clear_content()

        self.page_title(
            "My Schedule",
            "Personalized study plan based on your performance"
        )

        schedule = [
            ("06:00 PM", "Linked List", "45 min", "HIGH"),
            ("06:45 PM", "Break", "10 min", ""),
            ("06:55 PM", "Stack", "50 min", "HIGH"),
            ("07:45 PM", "Break", "10 min", ""),
            ("07:55 PM", "Graph", "45 min", "HIGH"),
            ("08:40 PM", "Quick Revision", "20 min", "MEDIUM"),
            ("09:00 PM", "Topic Quiz", "15 min", "TEST"),
        ]

        for start, topic, duration, priority in schedule:

            row = tk.Frame(
                self.content_area,
                bg="#111C30",
                padx=20,
                pady=12
            )
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=start,
                width=12,
                anchor="w",
                font=("Arial", 11, "bold"),
                fg="#38BDF8",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=topic,
                width=25,
                anchor="w",
                font=("Arial", 11),
                fg="white",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=duration,
                width=12,
                anchor="w",
                font=("Arial", 10),
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=priority,
                font=("Arial", 10, "bold"),
                fg="#38BDF8",
                bg="#111C30"
            ).pack(side="right")


    # ========================================================
    #                       RANKING
    # ========================================================

    def student_ranking(self):

        self.clear_content()

        self.page_title(
            "Student Ranking",
            "Your performance compared with other students"
        )

        ranking = [
            ("1", "Ayush Kumar", "94%"),
            ("2", "Aarij Tyagi", "89%"),
            ("3", "Student A", "86%"),
            ("4", self.current_user, "84%"),
            ("5", "Student B", "81%"),
        ]

        for rank, name, score in ranking:

            row = tk.Frame(
                self.content_area,
                bg="#111C30",
                padx=20,
                pady=13
            )
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=f"#{rank}",
                width=8,
                font=("Arial", 12, "bold"),
                fg="#38BDF8",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=name,
                width=30,
                anchor="w",
                font=("Arial", 11),
                fg="white",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=score,
                font=("Arial", 11, "bold"),
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="right")


    # ========================================================
    #                       REPORTS
    # ========================================================

    def student_reports(self):

        self.clear_content()

        self.page_title(
            "Reports",
            "Your academic progress and improvement"
        )

        report = tk.Frame(
            self.content_area,
            bg="#111C30",
            padx=25,
            pady=25
        )
        report.pack(fill="both", expand=True)

        tk.Label(
            report,
            text="Daily Learning Report",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#111C30"
        ).pack(anchor="w")

        information = [
            ("Study Time", "2h 40m"),
            ("Tests Attempted", "2"),
            ("Average Score", "76%"),
            ("Improvement", "+8%"),
            ("Strong Topics", "Arrays, Queue"),
            ("Weak Topics", "Graph, Recursion"),
        ]

        for title, value in information:

            row = tk.Frame(
                report,
                bg="#18243A",
                padx=15,
                pady=10
            )
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=title,
                font=("Arial", 10),
                fg="#94A3B8",
                bg="#18243A"
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                font=("Arial", 10, "bold"),
                fg="white",
                bg="#18243A"
            ).pack(side="right")

        tk.Label(
            report,
            text="\nRecommended Improvements",
            font=("Arial", 15, "bold"),
            fg="#38BDF8",
            bg="#111C30"
        ).pack(anchor="w", pady=(15, 5))

        recommendations = (
            "• Revise Graph Traversal concepts.\n"
            "• Practice BFS and DFS questions.\n"
            "• Attempt another Graph topic test.\n"
            "• Maintain your current study consistency."
        )

        tk.Label(
            report,
            text=recommendations,
            font=("Arial", 11),
            fg="#CBD5E1",
            bg="#111C30",
            justify="left"
        ).pack(anchor="w")


    # ========================================================
    #                    TEACHER DASHBOARD
    # ========================================================

    def show_teacher_dashboard(self):

        menu = [
            ("🏠  Dashboard", self.teacher_home),
            ("👥  Students", self.teacher_students),
            ("➕  Add Student", self.teacher_add_student),
            ("📊  Marks", self.teacher_marks),
            ("📅  Attendance", self.teacher_attendance),
            ("📚  Syllabus", self.teacher_syllabus),
            ("📄  Notes", self.teacher_notes),
            ("📝  Tests", self.teacher_tests),
            ("🏆  Rankings", self.teacher_rankings),
            ("📑  Reports", self.teacher_reports),
        ]

        self.create_dashboard(
            "Teacher / Host Dashboard",
            menu
        )

        self.teacher_home()


    def teacher_home(self):

        for widget in self.content_area.winfo_children():
            widget.destroy()

        stats = tk.Frame(
            self.content_area,
            bg="#0B1220"
        )
        stats.pack(fill="x")

        for i in range(4):
            stats.columnconfigure(i, weight=1)

        self.card(stats, "Students", "45", "Total students", 0)
        self.card(stats, "Average Marks", "74%", "Class average", 1)
        self.card(stats, "Attendance", "82%", "Class average", 2)
        self.card(stats, "Test Score", "76%", "Average", 3)

        analytics = tk.Frame(
            self.content_area,
            bg="#111C30",
            padx=25,
            pady=25
        )
        analytics.pack(fill="both", expand=True, pady=25)

        tk.Label(
            analytics,
            text="Class Performance Overview",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#111C30"
        ).pack(anchor="w")

        data = [
            ("Strongest Topic", "Arrays", "88%"),
            ("Weakest Topic", "Graphs", "57%"),
            ("Most Improved", "Student A", "+21%"),
            ("Average Study Time", "2.8 hours/day", ""),
        ]

        for label, value, score in data:

            row = tk.Frame(
                analytics,
                bg="#18243A",
                padx=15,
                pady=12
            )
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=label,
                font=("Arial", 10),
                fg="#94A3B8",
                bg="#18243A"
            ).pack(side="left")

            tk.Label(
                row,
                text=f"{value} {score}",
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#18243A"
            ).pack(side="right")


    # ========================================================
    #                   TEACHER PAGES
    # ========================================================

    def teacher_students(self):

        self.clear_content()

        self.page_title(
            "Student Management",
            "View and manage students"
        )

        students = [
            ("STU001", "Ayush Kumar", "94%", "88%"),
            ("STU002", "Aarij Tyagi", "89%", "91%"),
            ("STU003", "Prateek Negi", "84%", "84%"),
            ("STU004", "Student A", "81%", "79%"),
        ]

        for sid, name, marks, attendance in students:

            row = tk.Frame(
                self.content_area,
                bg="#111C30",
                padx=15,
                pady=12
            )
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=sid,
                width=12,
                fg="#38BDF8",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=name,
                width=25,
                anchor="w",
                fg="white",
                bg="#111C30"
            ).pack(side="left")

            tk.Label(
                row,
                text=f"Marks: {marks}",
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="left", padx=20)

            tk.Label(
                row,
                text=f"Attendance: {attendance}",
                fg="#94A3B8",
                bg="#111C30"
            ).pack(side="left")

    def teacher_add_student(self):
        self.simple_page(
            "Add Student",
            "Teacher can add a new student account here."
        )

    def teacher_marks(self):
        self.simple_page(
            "Marks Management",
            "Teacher can view and edit student marks here."
        )

    def teacher_attendance(self):
        self.simple_page(
            "Attendance Management",
            "Teacher can view and update student attendance here."
        )

    def teacher_syllabus(self):
        self.simple_page(
            "Syllabus Management",
            "Teacher can manage subjects, units and topics here."
        )

    def teacher_notes(self):
        self.simple_page(
            "Study Notes",
            "Teacher can upload and manage PDF study material here."
        )

    def teacher_tests(self):
        self.simple_page(
            "Test Management",
            "Teacher can create and manage topic, unit and overall tests here."
        )

    def teacher_rankings(self):
        self.simple_page(
            "Student Rankings",
            "Teacher can view complete student rankings here."
        )

    def teacher_reports(self):
        self.simple_page(
            "Student Reports",
            "Teacher can view individual and class performance reports here."
        )


    # ========================================================
    #                       HELPERS
    # ========================================================

    def clear_content(self):

        if hasattr(self, "content_area"):
            for widget in self.content_area.winfo_children():
                widget.destroy()

    def page_title(self, title, subtitle):

        tk.Label(
            self.content_area,
            text=title,
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#0B1220"
        ).pack(anchor="w")

        tk.Label(
            self.content_area,
            text=subtitle,
            font=("Arial", 10),
            fg="#64748B",
            bg="#0B1220"
        ).pack(anchor="w", pady=(3, 15))

    def simple_page(self, title, description):

        self.clear_content()

        self.page_title(title, description)

        box = tk.Frame(
            self.content_area,
            bg="#111C30",
            padx=30,
            pady=30
        )
        box.pack(fill="x", pady=20)

        tk.Label(
            box,
            text=description,
            font=("Arial", 12),
            fg="#CBD5E1",
            bg="#111C30"
        ).pack(anchor="w")


# ============================================================
#                       RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app = AdaptiveApp()
    app.mainloop()
