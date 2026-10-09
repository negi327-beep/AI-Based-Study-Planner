import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# ============================================================
# ADAPTIVE: Tkinter frontend prototype
# Course selection -> Subject selection -> Unit selection -> Learning dashboard
# Authentication, persistent database, real AI and C integration are future stages.
# ============================================================

BG = "#0B1220"
SIDEBAR = "#101B31"
PANEL = "#111C30"
CARD = "#18243A"
TEXT = "#F3F7FF"
MUTED = "#94A3B8"
ACCENT = "#38BDF8"
GREEN = "#34D399"
RED = "#F87171"

def make_units(subject):
    return [f"Unit {i}: {subject} - Topic {i}" for i in range(1, 6)]

CURRICULUM = {
    "BCA": {
        "Computer Fundamentals": make_units("Computer Fundamentals"),
        "Programming in C": make_units("Programming in C"),
        "Mathematics": make_units("Mathematics"),
        "Database Management Systems": make_units("Database Management Systems"),
        "Introduction to Data Structures": make_units("Introduction to Data Structures"),
    },
    "B.Ed": {
        "Childhood and Growing Up": make_units("Childhood and Growing Up"),
        "Contemporary India and Education": make_units("Contemporary India and Education"),
        "Learning and Teaching": make_units("Learning and Teaching"),
        "Assessment for Learning": make_units("Assessment for Learning"),
        "Pedagogy of School Subject": make_units("Pedagogy of School Subject"),
    },
    "B.Sc Science": {
        "Physics": make_units("Physics"),
        "Chemistry": make_units("Chemistry"),
        "Mathematics": make_units("Mathematics"),
        "Botany": make_units("Botany"),
        "Zoology": make_units("Zoology"),
    },
    "B.Com": {
        "Financial Accounting": make_units("Financial Accounting"),
        "Business Law": make_units("Business Law"),
        "Economics": make_units("Economics"),
        "Business Mathematics": make_units("Business Mathematics"),
        "Business Communication": make_units("Business Communication"),
    },
    "BBA": {
        "Principles of Management": make_units("Principles of Management"),
        "Marketing Management": make_units("Marketing Management"),
        "Human Resource Management": make_units("Human Resource Management"),
        "Business Economics": make_units("Business Economics"),
        "Financial Management": make_units("Financial Management"),
    },
}

class AdaptiveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ADAPTIVE - Personalized Learning System")
        self.geometry("1200x760")
        self.minsize(950, 650)
        self.configure(bg=BG)

        self.current_user = None
        self.current_role = None
        self.selected_course = None
        self.selected_subject = None
        self.selected_unit = None
        self.personal_notes = {}
        self.completed_topics = set()
        self.study_log = []
        self.last_page = "home"

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                             foreground=TEXT, arrowcolor=TEXT, padding=7)
        self.style.map("TCombobox", fieldbackground=[("readonly", CARD)],
                       foreground=[("readonly", TEXT)])

        self.show_login()

    # ------------------------ helpers ------------------------
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_content(self):
        if hasattr(self, "content_area"):
            for widget in self.content_area.winfo_children():
                widget.destroy()

    def create_button(self, parent, text, command, width=20, secondary=False):
        return tk.Button(
            parent, text=text, command=command, width=width,
            font=("Arial", 10, "bold"),
            bg=CARD if secondary else ACCENT,
            fg=TEXT if secondary else BG,
            activebackground="#263650" if secondary else "#7DD3FC",
            activeforeground=TEXT if secondary else BG,
            relief="flat", bd=0, cursor="hand2", padx=12, pady=8
        )

    def label(self, parent, text, size=11, bold=False, fg=TEXT, bg=None, **kwargs):
        return tk.Label(parent, text=text, font=("Arial", size, "bold" if bold else "normal"),
                        fg=fg, bg=bg or BG, **kwargs)

    def page_title(self, title, subtitle=""):
        self.label(self.content_area, title, 22, True).pack(anchor="w")
        if subtitle:
            self.label(self.content_area, subtitle, 10, fg=MUTED).pack(anchor="w", pady=(4, 16))

    def info_card(self, parent, title, value, subtitle="", column=0):
        box = tk.Frame(parent, bg=PANEL, padx=18, pady=16)
        box.grid(row=0, column=column, padx=6, sticky="nsew")
        self.label(box, title, 10, fg=MUTED, bg=PANEL).pack(anchor="w")
        self.label(box, value, 23, True, ACCENT, PANEL).pack(anchor="w", pady=5)
        if subtitle:
            self.label(box, subtitle, 9, fg=MUTED, bg=PANEL).pack(anchor="w")

    def show_login(self):
        self.clear_window()
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg=SIDEBAR)
        left.pack(side="left", fill="both", expand=True)
        self.label(left, "ADAPTIVE", 38, True, ACCENT, SIDEBAR).pack(pady=(130, 12))
        self.label(left, "AI-Based Personalized Learning\n& Student Performance Management System",
                   16, fg=TEXT, bg=SIDEBAR, justify="center").pack()
        self.label(left, "\nLearn  •  Analyze  •  Improve", 13, fg=MUTED, bg=SIDEBAR).pack()
        self.label(left, "\n5 Courses  •  25 Subjects  •  125 Units", 11, fg=ACCENT, bg=SIDEBAR).pack()

        right = tk.Frame(main, bg=BG)
        right.pack(side="right", fill="both", expand=True)
        box = tk.Frame(right, bg=PANEL, padx=42, pady=32)
        box.place(relx=0.5, rely=0.5, anchor="center")
        self.label(box, "LOGIN", 25, True, TEXT, PANEL).pack(pady=(0, 22), anchor="w")

        self.label(box, "Login as", 10, fg=MUTED, bg=PANEL).pack(anchor="w")
        self.role_var = tk.StringVar(value="Student")
        ttk.Combobox(box, textvariable=self.role_var, values=["Student", "Teacher / Host"],
                     state="readonly", width=30).pack(fill="x", pady=(5, 16), ipady=4)

        self.label(box, "User ID", 10, fg=MUTED, bg=PANEL).pack(anchor="w")
        self.user_entry = tk.Entry(box, width=32, font=("Arial", 12), bg=CARD, fg=TEXT,
                                   insertbackground=TEXT, relief="flat")
        self.user_entry.pack(fill="x", pady=(5, 14), ipady=8)

        self.label(box, "Password", 10, fg=MUTED, bg=PANEL).pack(anchor="w")
        self.pass_entry = tk.Entry(box, width=32, font=("Arial", 12), bg=CARD, fg=TEXT,
                                   insertbackground=TEXT, show="*", relief="flat")
        self.pass_entry.pack(fill="x", pady=(5, 22), ipady=8)
        self.create_button(box, "LOGIN", self.login, width=30).pack(fill="x")
        self.label(box, "Demo login only • Database authentication not connected yet",
                   8, fg=MUTED, bg=PANEL).pack(pady=(20, 0))

    def login(self):
        user_id = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not user_id or not password:
            messagebox.showwarning("Missing Information", "Please enter User ID and Password.")
            return
        self.current_user = user_id
        self.current_role = "teacher" if self.role_var.get() == "Teacher / Host" else "student"
        if self.current_role == "student":
            # Required flow: every student selects course, then subject, then unit.
            self.show_course_selection()
        else:
            self.show_teacher_dashboard()

    # ---------------------- app shell ------------------------
    def create_dashboard(self, title, menu_items):
        self.clear_window()
        shell = tk.Frame(self, bg=BG)
        shell.pack(fill="both", expand=True)

        sidebar = tk.Frame(shell, bg=SIDEBAR, width=235)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self.label(sidebar, "ADAPTIVE", 23, True, ACCENT, SIDEBAR).pack(pady=(28, 4))
        self.label(sidebar, "Personalized Learning", 9, fg=MUTED, bg=SIDEBAR).pack(pady=(0, 22))

        for name, command in menu_items:
            tk.Button(sidebar, text=name, command=command, anchor="w", padx=16,
                      font=("Arial", 10), bg=SIDEBAR, fg="#CBD5E1",
                      activebackground="#1E3A5F", activeforeground="white",
                      relief="flat", cursor="hand2").pack(fill="x", pady=1, ipady=7)

        tk.Button(sidebar, text="Logout", command=self.show_login, anchor="w", padx=16,
                  font=("Arial", 10, "bold"), bg=SIDEBAR, fg=RED,
                  activebackground="#3F1D25", relief="flat", cursor="hand2").pack(
                      side="bottom", fill="x", pady=18, ipady=8)

        main = tk.Frame(shell, bg=BG)
        main.pack(side="right", fill="both", expand=True)
        header = tk.Frame(main, bg=BG, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)
        self.label(header, title, 21, True).pack(side="left", padx=26, pady=20)
        self.label(header, f"Welcome, {self.current_user}", 10, fg=MUTED).pack(side="right", padx=26)
        self.content_area = tk.Frame(main, bg=BG)
        self.content_area.pack(fill="both", expand=True, padx=26, pady=10)
        return self.content_area

    def student_menu(self):
        return [
            ("🏠  Dashboard", self.student_home),
            ("👤  My Profile", self.student_profile),
            ("🎓  Change Course", self.show_course_selection),
            ("📚  Subjects & Units", self.student_subjects),
            ("📄  Notes & Notepad", self.student_notes),
            ("📝  Tests", self.student_tests),
            ("📅  My Schedule", self.student_schedule),
            ("🏆  Ranking", self.student_ranking),
            ("📊  Reports", self.student_reports),
        ]

    def ensure_selection(self):
        if not self.selected_course:
            self.show_course_selection()
            return False
        if not self.selected_subject:
            self.show_subject_selection()
            return False
        if not self.selected_unit:
            self.show_units()
            return False
        return True

    def show_student_dashboard(self):
        if not self.selected_course:
            self.show_course_selection()
            return
        self.create_dashboard("Student Dashboard", self.student_menu())
        self.student_home()

    # ---------------- course -> subject -> unit --------------
    def show_course_selection(self):
        self.clear_window()
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=24)
        self.label(frame, "Choose Your Course", 25, True).pack(anchor="w")
        self.label(frame, "Step 1 of 3 • Select a course before choosing a subject and unit.",
                   11, fg=MUTED).pack(anchor="w", pady=(5, 20))

        cards = tk.Frame(frame, bg=BG)
        cards.pack(fill="both", expand=True)
        descriptions = {
            "BCA": "Bachelor of Computer Applications",
            "B.Ed": "Bachelor of Education",
            "B.Sc Science": "Bachelor of Science",
            "B.Com": "Bachelor of Commerce",
            "BBA": "Bachelor of Business Administration",
        }
        for index, course in enumerate(CURRICULUM):
            row, col = divmod(index, 2)
            card = tk.Frame(cards, bg=PANEL, padx=20, pady=17)
            card.grid(row=row, column=col, sticky="nsew", padx=7, pady=7)
            self.label(card, course, 18, True, ACCENT, PANEL).pack(anchor="w")
            self.label(card, descriptions[course], 10, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(6, 12))
            self.label(card, "5 subjects  •  25 units", 10, fg=TEXT, bg=PANEL).pack(anchor="w", pady=(0, 12))
            self.create_button(card, f"Select {course}",
                               lambda c=course: self.select_course(c), width=18).pack(anchor="w")
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        tk.Button(frame, text="Logout", command=self.show_login, bg=CARD, fg=TEXT,
                  relief="flat", padx=14, pady=7).pack(anchor="w", pady=(12, 0))

    def select_course(self, course):
        self.selected_course = course
        self.selected_subject = None
        self.selected_unit = None
        self.show_subject_selection()

    def show_subject_selection(self):
        if not self.selected_course:
            self.show_course_selection()
            return
        frame = self.simple_selection_shell(
            f"{self.selected_course} • Select Subject",
            "Step 2 of 3 • Choose one of the five subjects in your course."
        )
        for subject in CURRICULUM[self.selected_course]:
            row = tk.Frame(frame, bg=PANEL, padx=15, pady=12)
            row.pack(fill="x", pady=5)
            self.label(row, subject, 12, True, TEXT, PANEL).pack(side="left", anchor="w")
            self.create_button(row, "Choose Subject",
                               lambda s=subject: self.select_subject(s), width=16).pack(side="right")
        self.create_button(frame, "← Change Course", self.show_course_selection,
                           secondary=True).pack(anchor="w", pady=(14, 0))

    def select_subject(self, subject):
        self.selected_subject = subject
        self.selected_unit = None
        self.show_units()

    def show_units(self):
        if not self.selected_course:
            self.show_course_selection()
            return
        if not self.selected_subject:
            self.show_subject_selection()
            return
        frame = self.simple_selection_shell(
            f"{self.selected_subject} • Select Unit",
            f"Step 3 of 3 • {self.selected_course} → {self.selected_subject}"
        )
        for unit in CURRICULUM[self.selected_course][self.selected_subject]:
            row = tk.Frame(frame, bg=PANEL, padx=15, pady=11)
            row.pack(fill="x", pady=5)
            self.label(row, unit, 11, fg=TEXT, bg=PANEL).pack(side="left", anchor="w")
            self.create_button(row, "Open Unit",
                               lambda u=unit: self.select_unit(u), width=14).pack(side="right")
        self.create_button(frame, "← Back to Subjects", self.show_subject_selection,
                           secondary=True).pack(anchor="w", pady=(14, 0))

    def simple_selection_shell(self, title, subtitle):
        self.clear_window()
        shell = tk.Frame(self, bg=BG)
        shell.pack(fill="both", expand=True, padx=32, pady=28)
        self.label(shell, "ADAPTIVE", 17, True, ACCENT).pack(anchor="w")
        self.label(shell, title, 23, True).pack(anchor="w", pady=(16, 4))
        self.label(shell, subtitle, 10, fg=MUTED).pack(anchor="w", pady=(0, 18))
        body = tk.Frame(shell, bg=BG)
        body.pack(fill="both", expand=True)
        return body

    def select_unit(self, unit):
        self.selected_unit = unit
        self.show_student_dashboard()

    # --------------------- student pages ---------------------
    def student_home(self):
        self.clear_content()
        self.page_title("Your Learning Overview", "Study, test, analyze and improve.")
        stats = tk.Frame(self.content_area, bg=BG)
        stats.pack(fill="x")
        for i in range(4):
            stats.columnconfigure(i, weight=1)
        self.info_card(stats, "Overall Performance", "76%", "Demo value", 0)
        self.info_card(stats, "Attendance", "84%", "Demo value", 1)
        self.info_card(stats, "Study Hours", "18.5h", "This week • demo", 2)
        self.info_card(stats, "Current Rank", "#4", "Demo ranking", 3)

        selection = tk.Frame(self.content_area, bg=PANEL, padx=18, pady=16)
        selection.pack(fill="x", pady=(18, 12))
        self.label(selection, "Current Learning Selection", 14, True, ACCENT, PANEL).pack(anchor="w")
        self.label(selection, f"Course: {self.selected_course or 'Not selected'}", 10, fg=TEXT, bg=PANEL).pack(anchor="w", pady=(8, 2))
        self.label(selection, f"Subject: {self.selected_subject or 'Not selected'}", 10, fg=TEXT, bg=PANEL).pack(anchor="w", pady=2)
        self.label(selection, f"Unit: {self.selected_unit or 'Not selected'}", 10, fg=TEXT, bg=PANEL).pack(anchor="w", pady=2)
        self.create_button(selection, "Change Course / Subject / Unit", self.show_course_selection,
                           secondary=True).pack(anchor="w", pady=(10, 0))

        plan = tk.Frame(self.content_area, bg=PANEL, padx=18, pady=16)
        plan.pack(fill="both", expand=True, pady=(4, 0))
        self.label(plan, "Today's Recommended Study Plan", 15, True, TEXT, PANEL).pack(anchor="w", pady=(0, 10))
        tasks = [
            ("Revise selected unit", "30 min", "HIGH"),
            ("Practice topic questions", "25 min", "HIGH"),
            ("Review previous mistakes", "15 min", "MEDIUM"),
        ]
        for topic, duration, priority in tasks:
            row = tk.Frame(plan, bg=CARD, padx=12, pady=10)
            row.pack(fill="x", pady=4)
            self.label(row, topic, 10, True, TEXT, CARD).pack(side="left")
            self.label(row, duration, 10, fg=MUTED, bg=CARD).pack(side="right", padx=12)
            self.label(row, priority, 9, True, ACCENT, CARD).pack(side="right")

    def student_profile(self):
        self.clear_content()
        self.page_title("My Profile", "Profile and academic selection (demo data)")
        box = tk.Frame(self.content_area, bg=PANEL, padx=24, pady=20)
        box.pack(fill="x", pady=12)
        details = [
            ("Student ID", self.current_user),
            ("Name", "Student Name (sample)"),
            ("Course", self.selected_course or "Not selected"),
            ("Subject", self.selected_subject or "Not selected"),
            ("Unit", self.selected_unit or "Not selected"),
            ("Section", "A3 (sample)"),
            ("Attendance", "84% (sample)"),
            ("Overall Marks", "76% (sample)"),
        ]
        for label, value in details:
            row = tk.Frame(box, bg=PANEL)
            row.pack(fill="x", pady=6)
            self.label(row, label, 10, fg=MUTED, bg=PANEL, width=20, anchor="w").pack(side="left")
            self.label(row, value, 10, True, TEXT, PANEL).pack(side="left")

    def student_subjects(self):
        if not self.selected_course:
            self.show_course_selection()
            return
        self.clear_content()
        self.page_title("Subjects & Units", f"Course: {self.selected_course}")
        for subject, units in CURRICULUM[self.selected_course].items():
            box = tk.Frame(self.content_area, bg=PANEL, padx=14, pady=12)
            box.pack(fill="x", pady=5)
            self.label(box, subject, 12, True, TEXT, PANEL).pack(side="left")
            self.create_button(box, "View Units", lambda s=subject: self.select_subject(s), width=14).pack(side="right")

    def student_notes(self):
        if not self.ensure_selection():
            return
        self.clear_content()
        self.page_title("Notes & Notepad", f"{self.selected_course} → {self.selected_subject} → {self.selected_unit}")
        container = tk.Frame(self.content_area, bg=BG)
        container.pack(fill="both", expand=True)
        pdf = tk.Frame(container, bg=PANEL, padx=16, pady=16)
        pdf.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.label(pdf, "Teacher's PDF Notes", 15, True, TEXT, PANEL).pack(anchor="w")
        self.label(pdf, "\nNo PDF viewer is connected yet.\nUse Open PDF to choose a study file.\nThe selected file path will be shown below.",
                   10, fg=MUTED, bg=PANEL, justify="left").pack(anchor="w", pady=12)
        pdf_path = tk.StringVar(value="No PDF selected")
        self.label(pdf, "Selected file:", 10, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(10, 2))
        tk.Label(pdf, textvariable=pdf_path, bg=PANEL, fg=TEXT, wraplength=300,
                 justify="left").pack(anchor="w")
        def choose_pdf():
            path = filedialog.askopenfilename(title="Select PDF notes", filetypes=[("PDF files", "*.pdf")])
            if path:
                pdf_path.set(path)
                messagebox.showinfo("PDF selected", "File selected. An embedded PDF reader will be added in a later stage.")
        self.create_button(pdf, "Open PDF", choose_pdf, width=14).pack(anchor="w", pady=10)

        notes = tk.Frame(container, bg=PANEL, padx=16, pady=16)
        notes.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.label(notes, "My Notepad", 15, True, TEXT, PANEL).pack(anchor="w")
        key = (self.current_user, self.selected_course, self.selected_subject, self.selected_unit)
        text = tk.Text(notes, bg=CARD, fg=TEXT, insertbackground=TEXT, font=("Arial", 10),
                       relief="flat", wrap="word")
        text.pack(fill="both", expand=True, pady=12)
        text.insert("1.0", self.personal_notes.get(key, "Write your notes for this unit here..."))
        def save_notes():
            self.personal_notes[key] = text.get("1.0", "end-1c")
            messagebox.showinfo("Saved", "Notes saved in this running session. Persistent database saving comes later.")
        def improve_notes():
            raw = text.get("1.0", "end-1c").strip()
            if not raw:
                messagebox.showwarning("No notes", "Write some notes first.")
                return
            messagebox.showinfo("AI Notes", "AI integration is not connected yet. Notes have not been sent to an AI service.")
        actions = tk.Frame(notes, bg=PANEL)
        actions.pack(fill="x")
        self.create_button(actions, "Save Notes", save_notes, width=14).pack(side="left")
        self.create_button(actions, "Improve with AI", improve_notes, width=16, secondary=True).pack(side="right")

    def student_tests(self):
        if not self.ensure_selection():
            return
        self.clear_content()
        self.page_title("Tests", f"Selected unit: {self.selected_unit}")
        for title, desc in [
            ("Topic-wise Test", "Practice one topic at a time."),
            ("Unit-wise Test", "Assess your understanding of this unit."),
            ("Overall Course Test", "Test the complete selected course syllabus."),
        ]:
            row = tk.Frame(self.content_area, bg=PANEL, padx=18, pady=15)
            row.pack(fill="x", pady=6)
            inner = tk.Frame(row, bg=PANEL)
            inner.pack(side="left", fill="x", expand=True)
            self.label(inner, title, 13, True, TEXT, PANEL).pack(anchor="w")
            self.label(inner, desc, 9, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(4, 0))
            self.create_button(row, "Start Test", lambda t=title: self.start_demo_test(t), width=13).pack(side="right")

    def start_demo_test(self, title):
        messagebox.showinfo("Test module", f"{title}\n\nQuestion bank, score calculation and result history will be connected to the backend in the next stage.")

    def student_schedule(self):
        self.clear_content()
        self.page_title("My Schedule", "Sample schedule; adaptive scheduling logic will be connected later.")
        schedule = [
            ("06:00 PM", "Revise selected unit", "30 min", "HIGH"),
            ("06:30 PM", "Practice topic questions", "25 min", "HIGH"),
            ("06:55 PM", "Break", "10 min", ""),
            ("07:05 PM", "Review mistakes", "15 min", "MEDIUM"),
            ("07:20 PM", "Quick revision quiz", "15 min", "TEST"),
        ]
        for start, topic, duration, priority in schedule:
            row = tk.Frame(self.content_area, bg=PANEL, padx=16, pady=11)
            row.pack(fill="x", pady=4)
            self.label(row, start, 10, True, ACCENT, PANEL, width=12, anchor="w").pack(side="left")
            self.label(row, topic, 10, fg=TEXT, bg=PANEL, width=30, anchor="w").pack(side="left")
            self.label(row, duration, 10, fg=MUTED, bg=PANEL, width=12, anchor="w").pack(side="left")
            self.label(row, priority, 9, True, ACCENT, PANEL).pack(side="right")

    def student_ranking(self):
        self.clear_content()
        self.page_title("Student Ranking", "Sample ranking only; live rankings need stored test results.")
        ranking = [("1", "Ayush Kumar", "94%"), ("2", "Aarij Tyagi", "89%"),
                   ("3", "Student A", "86%"), ("4", self.current_user, "84%"),
                   ("5", "Student B", "81%")]
        for rank, name, score in ranking:
            row = tk.Frame(self.content_area, bg=PANEL, padx=18, pady=11)
            row.pack(fill="x", pady=4)
            self.label(row, f"#{rank}", 12, True, ACCENT, PANEL, width=8).pack(side="left")
            self.label(row, name, 10, fg=TEXT, bg=PANEL, width=28, anchor="w").pack(side="left")
            self.label(row, score, 10, True, TEXT, PANEL).pack(side="right")

    def student_reports(self):
        self.clear_content()
        self.page_title("Learning Reports", "Sample values; report generation will be connected to actual data.")
        report = tk.Frame(self.content_area, bg=PANEL, padx=20, pady=20)
        report.pack(fill="x")
        self.label(report, "Daily Learning Report", 16, True, TEXT, PANEL).pack(anchor="w", pady=(0, 12))
        data = [
            ("Study time", "2h 40m (sample)"),
            ("Tests attempted", "2 (sample)"),
            ("Average score", "76% (sample)"),
            ("Improvement", "+8% (sample)"),
            ("Strong topics", "Arrays, Queue (sample)"),
            ("Weak topics", "Graph, Recursion (sample)"),
        ]
        for title, value in data:
            row = tk.Frame(report, bg=CARD, padx=12, pady=9)
            row.pack(fill="x", pady=3)
            self.label(row, title, 10, fg=MUTED, bg=CARD).pack(side="left")
            self.label(row, value, 10, True, TEXT, CARD).pack(side="right")
        self.label(report, "\nRecommended next steps", 13, True, ACCENT, PANEL).pack(anchor="w", pady=(12, 4))
        self.label(report, "• Revise weak topics.\n• Attempt another unit test.\n• Compare results after revision.",
                   10, fg=TEXT, bg=PANEL, justify="left").pack(anchor="w")

    # --------------------- teacher pages ---------------------
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
        self.create_dashboard("Teacher / Host Dashboard", menu)
        self.teacher_home()

    def teacher_home(self):
        self.clear_content()
        self.page_title("Class Overview", "Demo analytics; values will come from the database later.")
        stats = tk.Frame(self.content_area, bg=BG)
        stats.pack(fill="x")
        for i in range(4):
            stats.columnconfigure(i, weight=1)
        self.info_card(stats, "Students", "45", "Sample", 0)
        self.info_card(stats, "Average Marks", "74%", "Sample", 1)
        self.info_card(stats, "Attendance", "82%", "Sample", 2)
        self.info_card(stats, "Average Test Score", "76%", "Sample", 3)
        box = tk.Frame(self.content_area, bg=PANEL, padx=20, pady=20)
        box.pack(fill="both", expand=True, pady=18)
        self.label(box, "Class Performance Overview", 16, True, TEXT, PANEL).pack(anchor="w")
        for label, value in [
            ("Strongest topic", "Arrays — 88% (sample)"),
            ("Weakest topic", "Graphs — 57% (sample)"),
            ("Most improved student", "Student A — +21% (sample)"),
            ("Average study time", "2.8 hours/day (sample)"),
        ]:
            row = tk.Frame(box, bg=CARD, padx=12, pady=10)
            row.pack(fill="x", pady=4)
            self.label(row, label, 10, fg=MUTED, bg=CARD).pack(side="left")
            self.label(row, value, 10, True, TEXT, CARD).pack(side="right")

    def teacher_students(self):
        self.clear_content()
        self.page_title("Student Management", "Sample records; add/edit/delete actions need database integration.")
        for sid, name, marks, attendance in [
            ("STU001", "Ayush Kumar", "94%", "88%"),
            ("STU002", "Aarij Tyagi", "89%", "91%"),
            ("STU003", "Prateek Negi", "84%", "84%"),
            ("STU004", "Student A", "81%", "79%"),
        ]:
            row = tk.Frame(self.content_area, bg=PANEL, padx=12, pady=12)
            row.pack(fill="x", pady=4)
            self.label(row, sid, 9, True, ACCENT, PANEL, width=10).pack(side="left")
            self.label(row, name, 10, fg=TEXT, bg=PANEL, width=22, anchor="w").pack(side="left")
            self.label(row, f"Marks: {marks}", 9, fg=MUTED, bg=PANEL).pack(side="left", padx=10)
            self.label(row, f"Attendance: {attendance}", 9, fg=MUTED, bg=PANEL).pack(side="left", padx=10)

    def teacher_add_student(self):
        self.clear_content()
        self.page_title("Add Student", "Demo form; it does not save to a database yet.")
        form = tk.Frame(self.content_area, bg=PANEL, padx=22, pady=22)
        form.pack(anchor="nw", fill="x")
        entries = {}
        for field in ["Student ID", "Full Name", "Course", "Section"]:
            self.label(form, field, 10, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(8, 3))
            if field == "Course":
                var = tk.StringVar(value="BCA")
                widget = ttk.Combobox(form, textvariable=var, values=list(CURRICULUM), state="readonly")
                widget.pack(fill="x", pady=(0, 6))
                entries[field] = var
            else:
                widget = tk.Entry(form, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
                widget.pack(fill="x", ipady=7, pady=(0, 6))
                entries[field] = widget
        def submit():
            messagebox.showinfo("Demo form", "Form layout is ready. Student records will be saved after SQLite integration.")
        self.create_button(form, "Save Student", submit).pack(anchor="w", pady=14)

    def teacher_marks(self):
        self.simple_teacher_page("Marks Management", "Teacher marks editing and saved mark records will be connected to SQLite.")

    def teacher_attendance(self):
        self.simple_teacher_page("Attendance Management", "Attendance editing and attendance summaries will be connected to SQLite.")

    def teacher_syllabus(self):
        self.clear_content()
        self.page_title("Syllabus Management", "Current demo curriculum")
        for course, subjects in CURRICULUM.items():
            box = tk.Frame(self.content_area, bg=PANEL, padx=12, pady=10)
            box.pack(fill="x", pady=4)
            self.label(box, f"{course}: {len(subjects)} subjects, {sum(len(u) for u in subjects.values())} units",
                       10, True, TEXT, PANEL).pack(anchor="w")
        self.label(self.content_area, "The subject and unit names are placeholders and can be replaced with official syllabi.",
                   9, fg=MUTED, wraplength=750, justify="left").pack(anchor="w", pady=10)

    def teacher_notes(self):
        self.simple_teacher_page("Study Notes", "Teacher PDF upload and course/subject/unit assignment will be connected next.")

    def teacher_tests(self):
        self.simple_teacher_page("Test Management", "Teacher test creation, questions, answer keys and results will be connected next.")

    def teacher_rankings(self):
        self.simple_teacher_page("Student Rankings", "Live rankings will be calculated from actual stored test results.")

    def teacher_reports(self):
        self.simple_teacher_page("Student Reports", "Individual and class performance reports will be generated from stored data.")

    def simple_teacher_page(self, title, description):
        self.clear_content()
        self.page_title(title, description)
        box = tk.Frame(self.content_area, bg=PANEL, padx=24, pady=24)
        box.pack(fill="x", pady=15)
        self.label(box, description, 11, fg=TEXT, bg=PANEL, wraplength=750, justify="left").pack(anchor="w")

if __name__ == "__main__":
    app = AdaptiveApp()
    app.mainloop()
