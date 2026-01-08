import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
df = None
class loginSystem:
    def _init_(self):
        self.username = ""
        self.password = ""

    def signup(self):
        print("======================")
        print("||      SIGNUP      ||")
        print("======================")
        self.username = input("For signin first please Enter username: ")
        while True:
            self.password = input("Enter password(must contain alphabet.digit and underscore): ")
            length = len(self.password) >= 6
            letter = any(c.isalpha() for c in self.password)
            digit = any(c.isdigit() for c in self.password)
            underscore = "_" in self.password

            if length and letter and digit and underscore:
                print("Signup successful!\n")
                break
            else:
                print("Your password or username is incorrect!")
                print("\nPassword must contain:")
                print("- at least 6 characters")
                print("- at least one letter")
                print("- at least one number")
                print("- underscore (_)")
                print("Try again...\n")

    def login(self):
        print("======================")
        print("||      login      ||")
        print("======================")

        while True:
            user = input("Enter username: ")
            pwd = input("Enter password: ")

            if user == self.username and pwd == self.password:
                print("\nLogin successful! Welcome!")
                break
            else:
                print("Incorrect username or password. Try again...\n")

def loadData():
    global df
    try:
        df = pd.read_csv("shoaib.csv")
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.title()
        print("Columns in CSV:", df.columns.tolist())
        print(df.head())
        print("Data Loaded Successfully")
        return df
    except Exception as e:
        print("Error loading shoaib.csv:", e)
        return None
def mainMenu():
    print("================================================================")
    print("||             WELCOME TO STUDENT ANALYST SYSTEM               ||")
    print("================================================================")
    print("===================================")
    print("||           MAIN MENU           ||")
    print("===================================")
    print("1. Basic Details")
    print("2. Subject Details")
    print("3. Student Details")
    print("4. Pass / Fail")
    print("5. Marks Frequency")
    print("6. Subject Report")
    print("7. Heat Map")
    print("8. Student Academic Report")
    print("9. Student Attendance Report")
    print("10. Co-Curricular Report")
    print("0. EXIT")
    print("===========================================\n")


def stBasicDet():
   
    print("\n========== BASIC STUDENT DETAILS ==========")
    if df is None:
        print("Data not loaded.")
        return
    print(df.describe())
    print("===========================================\n")

def subjDetail():
    print("\n========== STUDENT SUBJECT DETAILS ==========")
    if df is None:
        print("Data not loaded.")
        return
    if "Subject" not in df.columns or "Marks" not in df.columns:
        print("ERROR: 'Subject' and/or 'Marks' column missing.")
        return

    print("======== MAXIMUM MARKS BY SUBJECT ========")
    print(df.groupby("Subject")["Marks"].max())
    print("===============================")

    print("======== MINIMUM MARKS BY SUBJECT ========")
    print(df.groupby("Subject")["Marks"].min())
    print("===============================")

    print("======== AVERAGE MARKS BY SUBJECT ========")
    print(df.groupby("Subject")["Marks"].mean())
    print("===============================")

    print("======== VARIANCE BY SUBJECT ========")
    print(df.groupby("Subject")["Marks"].var())
    print("===============================")

    print("======== STANDARD DEVIATION BY SUBJECT ========")
    print(df.groupby("Subject")["Marks"].std())
    print("===============================\n")


def StudentDet():
    print("==== Student Complete Detail ====")
    if df is None:
        print("Data not loaded.")
        return
    if "Name" not in df.columns or "Marks" not in df.columns:
        print("ERROR: 'Name' and/or 'Marks' column missing.")
        return
    group_cols = ["Name"]
    if "Class" in df.columns:
        group_cols.append("Class")
    summary = df.groupby(group_cols)["Marks"].agg(['count','mean','max','min','var','std'])
    print(summary)
    print("===============================\n")

def PassFail():
    print("==== Student Pass/Fail Detail ====")
    if df is None:
        print("Data not loaded.")
        return
    if "Marks" not in df.columns:
        print("ERROR: 'Marks' column missing.")
        return
    threshold = 50  
    row_pass = (df["Marks"] >= threshold).sum()
    row_total = len(df)
    row_fail = row_total - row_pass
    print(f"Per-entry (subject) - Passed entries: {row_pass}, Failed entries: {row_fail}, Pass% = {row_pass*100/row_total:.2f}%")

    if "Name" in df.columns:
        student_avg = df.groupby("Name")["Marks"].mean()
        student_pass = (student_avg >= threshold).sum()
        student_total = student_avg.shape[0]
        student_fail = student_total - student_pass
        print(f"Per-student (avg) - Passed students: {student_pass}, Failed students: {student_fail}, Pass% = {student_pass*100/student_total:.2f}%")
    else:
        print("Note: No 'Name' column, skipping per-student pass/fail.")

def Frequency():
    print("========== MARKS FREQUENCY ===========")
    if df is None:
        print("Data not loaded.")
        return
    if "Marks" not in df.columns:
        print("ERROR: 'Marks' column missing.")
        return

    plt.figure(figsize=(8,5))
    sns.histplot(df["Marks"].dropna(), kde=True)
    plt.title("Histogram of Marks")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


def subjReport():
    print("==== Student Subject Report ====")
    if df is None:
        print("Data not loaded.")
        return
    if "Subject" not in df.columns or "Marks" not in df.columns:
        print("ERROR: 'Subject' and/or 'Marks' missing.")
        return
    plt.figure(figsize=(8,5))
    try:
        sns.barplot(data=df, x='Subject', y='Marks', estimator=np.mean, errorbar=None)
    except TypeError:
        sns.barplot(data=df, x='Subject', y='Marks', estimator=np.mean, ci=None)
    plt.title("Average Marks per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.show()

def studentHeatMap():
    print("==== Student Heat Map ====")
    if df is None:
        print("Data not loaded.")
        return
    if not {"Name","Subject","Marks"}.issubset(df.columns):
        print("ERROR: 'Name', 'Subject', 'Marks' are required for heatmap.")
        return
    pivot = df.pivot_table(index='Name', columns='Subject', values='Marks', aggfunc='mean')
    plt.figure(figsize=(12, max(6, len(pivot)*0.15)))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="coolwarm", cbar_kws={'label': 'Marks'})
    plt.title("Student vs Subject Marks Heatmap")
    plt.ylabel("Student")
    plt.xlabel("Subject")
    plt.tight_layout()
    plt.show()
def StdAcadRep():
    print("==== Student Academic Report ====")

    # Check if data is loaded
    if df is None:
        print("Data not loaded.")
        return

    # Required columns check
    required = {"Name", "Subject", "Marks"}
    if not required.issubset(df.columns):
        print("ERROR: 'Name', 'Subject', 'Marks' required for academic report.")
        return

    # Display subject-wise marks
    print("==== Subject-wise marks (sample rows) ==========")
    if "Class" in df.columns:
        print(df[["Name", "Class", "Subject", "Marks"]].head(20))
    else:
        print(df[["Name", "Subject", "Marks"]].head(20))

    # Average marks per student per subject
    print("\n==== Average marks per student-subject ==========")
    print(df.groupby(["Name", "Subject"])["Marks"].mean().head(20))

    # Average marks per student
    print("\n==== Average marks per student ==========")
    print(df.groupby("Name")["Marks"].mean().sort_values(ascending=False).head(20))
    print("==========================")

    # Maximum marks per student
    print("\n==== Maximum marks per student ==========")
    print(df.groupby("Name")["Marks"].max().head(20))
    print("============================")

    # Minimum marks per student
    print("\n==== Minimum marks per student ==========")
    print(df.groupby("Name")["Marks"].min().head(20))
    print("=============================")

    # Academic performance (if column exists)
    if "Academic" in df.columns:
        print("\n==== Academic performance ====")
        print(df.groupby("Academic")["Marks"].mean())
        print("===============================")
    else:
        print("\nNote: No 'Academic' column found; skipping that section.")


def stdAttendReport():
    print("===== Student Attendance Report =====")

    if df is None:
        print("Data not loaded.")
        return
    if "Classes_Attend" in df.columns:

        try:
            total_days = int(input("Enter total working days: "))
        except ValueError:
            print("Invalid total days entered.")
            return

        df_att = df.copy()
        df_att["Attendance_%"] = (df_att["Classes_Attend"] / total_days) * 100

        # Group by student name
        if "Name" in df_att.columns:
            per_stud = df_att.groupby("Name")["Attendance_%"].mean()
        else:
            print(df_att.head())
            return
        remarks_list = []
        for p in per_stud:
            if p >= 90:
                remarks_list.append("Excellent")
            elif p >= 75:
                remarks_list.append("Good")
            elif p >= 60:
                remarks_list.append("Needs Improvement")
            else:
                remarks_list.append("Poor")
        result = per_stud.reset_index()
        result["Remarks"] = remarks_list

        print("\n----- Attendance Report -----")
        print(result.to_string(index=False))

    else:
        print("No attendance column found ('Classes_Attend').")

def stdCoCurclReport():
    print("==== Student Co-Curricular Report ====")

    if df is None:
        print("Data not loaded.")
        return
    df.columns = df.columns.str.strip().str.lower()

    if "cocurricular" not in df.columns:
        print("No 'CoCurricular' column found in CSV.")
        print("Available columns:", df.columns.tolist())
        return

    print("\n===== Participation Count (Activity-wise) =====")
    print(df["cocurricular"].value_counts())

    print("\n===== Co-Curricular Activities for Each Student =====")
    student_activities = df.groupby("name")["cocurricular"].apply(list)

    for name, activities in student_activities.head(20).items():
        print(f"{name} : {activities}")



def matchChoice(choice):
    match choice:
        case 1:
            stBasicDet()
        case 2:
            subjDetail()
        case 3:
            StudentDet()
        case 4:
            PassFail()
        case 5:
            Frequency()
        case 6:
            subjReport()
        case 7:
            studentHeatMap()
        case 8:
            StdAcadRep()
        case 9:
            stdAttendReport()
        case 10:
            stdCoCurclReport()
        case 0:
            print("Exiting Program...")
            exit()
            print("Invalid choice! Please enter a number between 0 and 10.")
def main():
    l1=loginSystem()
    l1.signup()
    l1.login()
    loadData()
    print("=============================")
    if df is None:
        print("File could not be loaded!")
        return
    while True:
        mainMenu()
        try:
            choice = int(input("Enter number between (0–10): "))
            matchChoice(choice)
        except ValueError:
            print("Invalid Input! Please enter a number.")

if __name__ == "__main__":
    main()