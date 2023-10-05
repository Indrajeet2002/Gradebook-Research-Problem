import tkinter as tk
from tkinter import Button, Entry, Label, Toplevel, filedialog, messagebox
import csv
from tkinter import font

# Define sid_entry and labels as global variables
sid_entry = None
sid_label_result = None
first_name_label = None
last_name_label = None
email_label = None
hw_label = None
quiz_label = None
midterm_label = None
final_label = None
final_letter_score_label = None
task_entry = None
task_label_result = None
max_score_label = None
min_score_label = None
avg_score_label = None
file_path = None
listbox = None
update_scores_window = None
data = None

def read_csv_file(file_path):
    # Read the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data

def write_csv_file(file_path, data):
    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)

def get_scores_by_task(data, task_name):
    # Find the column index for the given task name
    header_row = data[0]
    try:
        task_index = header_row.index(task_name)
    except ValueError:
        return None  # Task name not found

    # Extract the scores for the task from the data
    scores = [int(row[task_index]) for row in data[1:] if row[task_index].isdigit()]

    return scores

def calculate_statistics(scores):
    if not scores:
        return None, None, None

    max_score = max(scores)
    min_score = min(scores)
    avg_score = sum(scores) / len(scores)

    return max_score, min_score, avg_score

def display_task_statistics():
    task_name = task_entry.get()

    scores = get_scores_by_task(data, task_name)

    if scores is not None:
        max_score, min_score, avg_score = calculate_statistics(scores)
        task_label_result.config(text=f"Task Name: {task_name}")
        max_score_label.config(text=f"Maximum Score: {max_score}")
        min_score_label.config(text=f"Minimum Score: {min_score}")
        avg_score_label.config(text=f"Average Score: {avg_score:.2f}")
    else:
        clear_task_labels()

def clear_task_labels():
    task_label_result.config(text="")
    max_score_label.config(text="")
    min_score_label.config(text="")
    avg_score_label.config(text="")

def get_student_data_by_sid(data, sid):
    for row in data[1:]:
        if row[0] == sid:
            return row
    return None

def calculate_final_letter_score(final_score):
    # Compute the final letter score based on the given criteria
    if final_score >= 90:
        return 'A'
    elif final_score >= 80:
        return 'B'
    elif final_score >= 70:
        return 'C'
    elif final_score >= 60:
        return 'D'
    else:
        return 'F'

def compute_final_score(student_data):
    # Calculate the weighted final score based on the given criteria
    if len(student_data) >= 13:
        hw_score = (int(student_data[4]) + int(student_data[5]) + int(student_data[6])) / 3
        quiz_score = (int(student_data[7]) + int(student_data[8]) + int(student_data[9]) + int(student_data[10])) / 4
        midterm_score = int(student_data[11])
        final_score = int(student_data[12])

        # Calculate the weighted final score
        weighted_final_score = (hw_score * 0.2) + (quiz_score * 0.2) + (midterm_score * 0.3) + (final_score * 0.3)

        return weighted_final_score
    else:
        return None

def display_student_data():
    sid = sid_entry.get()

    student_data = get_student_data_by_sid(data, sid)

    if student_data:
        sid_label_result.config(text=f"SID: {student_data[0]}")
        first_name_label.config(text=f"First Name: {student_data[1]}")
        last_name_label.config(text=f"Last Name: {student_data[2]}")
        email_label.config(text=f"Email: {student_data[3]}")
        
        # Check if student_data contains enough elements before accessing specific columns
        if len(student_data) >= 5:
            hw_label.config(text=f"HW: {student_data[4]}, {student_data[5]}, {student_data[6]}")
        else:
            hw_label.config(text="HW: N/A")
        
        # Check if student_data contains enough elements before accessing specific columns
        if len(student_data) >= 8:
            quiz_label.config(text=f"Quizzes: {student_data[7]}, {student_data[8]}, {student_data[9]}, {student_data[10]}")
        else:
            quiz_label.config(text="Quizzes: N/A")

        # Check if student_data contains enough elements before accessing specific columns
        if len(student_data) >= 12:
            midterm_label.config(text=f"Midterm: {student_data[11]}")
            final_label.config(text=f"Final: {student_data[12]}")
            
            final_score = compute_final_score(student_data)
            if final_score is not None:
                final_letter = calculate_final_letter_score(final_score)
                final_letter_score_label.config(text=f"Final Letter Score: {final_letter}")
            else:
                final_letter_score_label.config(text="Final Letter Score: N/A")
        else:
            midterm_label.config(text="Midterm: N/A")
            final_label.config(text="Final: N/A")
            final_letter_score_label.config(text="Final Letter Score: N/A")
    else:
        clear_labels()

def refresh_listbox():
    listbox.delete(0, tk.END)
    headers = data[0]
    listbox.insert(tk.END, ', '.join(headers))
    for row in data[1:]:
        listbox.insert(tk.END, ', '.join(row))

def clear_labels():
    sid_label_result.config(text="")
    first_name_label.config(text="")
    last_name_label.config(text="")
    email_label.config(text="")
    hw_label.config(text="")
    quiz_label.config(text="")
    midterm_label.config(text="")
    final_label.config(text="")
    final_letter_score_label.config(text="")

def export_csv_data():
    # Open a file dialog to select the export destination CSV file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if file_path:
        # Write the current data to the selected export file
        write_csv_file(file_path, data)

def open_add_user_window():
    # Create a new Tkinter window for adding a student
    add_user_window = Toplevel()
    add_user_window.title("Add Student")

    # Create entry fields for adding a new user
    entry_label = tk.Label(add_user_window, text="Add Student (SID,FirstName,LastName,Email,HW1,HW2,HW3,Quiz1,Quiz2,Quiz3,Quiz4,MidtermExam,FinalExam)")
    entry_label.pack()
    entry_label_2 = tk.Label(add_user_window, text="To delete a student profile, first click on the student in the other window and then the button below.")
    entry_label_2.pack()
    entry = tk.Entry(add_user_window)
    entry.pack()

    def add_user():
        # Add a new user to the data
        new_user = entry.get().split(',')
        data.append(new_user)
        write_csv_file(file_path, data)
        refresh_listbox()

    def delete_user():
        selected_index = listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            if selected_index < len(data):  # Check if the selected index is within the range
                del data[selected_index]
                write_csv_file(file_path, data)
                refresh_listbox()

    add_button = tk.Button(add_user_window, text="Add User", command=add_user)
    add_button.pack()

    # Create a button to delete the selected user
    delete_button = tk.Button(add_user_window, text="Delete User", command=delete_user)
    delete_button.pack()


def open_search_window():
    # Create a new Tkinter window for searching student data
    search_window = Toplevel()
    search_window.title("Search Student Data")

    # Create entry field for searching by SID
    sid_label = tk.Label(search_window, text="Enter SID:")
    sid_label.pack()
    global sid_entry
    sid_entry = tk.Entry(search_window)
    sid_entry.pack()

    # Create a button to search for student data
    search_button = tk.Button(search_window, text="Search Student Data", command=display_student_data)
    search_button.pack()

    # Labels to display student data
    global sid_label_result
    sid_label_result = tk.Label(search_window, text="")
    sid_label_result.pack()
    global first_name_label
    first_name_label = tk.Label(search_window, text="")
    first_name_label.pack()
    global last_name_label
    last_name_label = tk.Label(search_window, text="")
    last_name_label.pack()
    global email_label
    email_label = tk.Label(search_window, text="")
    email_label.pack()
    global hw_label
    hw_label = tk.Label(search_window, text="")
    hw_label.pack()
    global quiz_label
    quiz_label = tk.Label(search_window, text="")
    quiz_label.pack()
    global midterm_label
    midterm_label = tk.Label(search_window, text="")
    midterm_label.pack()
    global final_label
    final_label = tk.Label(search_window, text="")
    final_label.pack()
    global final_letter_score_label
    final_letter_score_label = tk.Label(search_window, text="")
    final_letter_score_label.pack()

def open_stats_window():
    # Create a new Tkinter window for task statistics
    stats_window = Toplevel()
    stats_window.title("Task Statistics")

    # Create entry field for searching by task name
    task_label = tk.Label(stats_window, text="Enter Task Name:")
    task_label.pack()
    global task_entry
    task_entry = tk.Entry(stats_window)
    task_entry.pack()

    # Create a button to search for task statistics
    search_task_button = tk.Button(stats_window, text="Search Task Stats", command=display_task_statistics)
    search_task_button.pack()

    # Labels to display task statistics
    global task_label_result
    task_label_result = tk.Label(stats_window, text="")
    task_label_result.pack()
    global max_score_label
    max_score_label = tk.Label(stats_window, text="")
    max_score_label.pack()
    global min_score_label
    min_score_label = tk.Label(stats_window, text="")
    min_score_label.pack()
    global avg_score_label
    avg_score_label = tk.Label(stats_window, text="")
    avg_score_label.pack()

def open_update_scores_window():
    global update_scores_window
    update_scores_window = Toplevel()
    update_scores_window.title("Update Student Scores")

    sid_label = Label(update_scores_window, text="Enter SID:")
    sid_label.pack()
    global sid_entry
    sid_entry = Entry(update_scores_window)
    sid_entry.pack()

    hw_label = Label(update_scores_window, text="Enter HW Scores (comma-separated, leave blank for no change):")
    hw_label.pack()
    global hw_entry
    hw_entry = Entry(update_scores_window)
    hw_entry.pack()

    quiz_label = Label(update_scores_window, text="Enter Quiz Scores (comma-separated, leave blank for no change):")
    quiz_label.pack()
    global quiz_entry
    quiz_entry = Entry(update_scores_window)
    quiz_entry.pack()

    midterm_label = Label(update_scores_window, text="Enter Midterm Score (leave blank for no change):")
    midterm_label.pack()
    global midterm_entry
    midterm_entry = Entry(update_scores_window)
    midterm_entry.pack()

    final_label = Label(update_scores_window, text="Enter Final Score (leave blank for no change):")
    final_label.pack()
    global final_entry
    final_entry = Entry(update_scores_window)
    final_entry.pack()

    update_button = Button(update_scores_window, text="Update Scores", command=update_student_scores)
    update_button.pack()

def update_student_scores():
    sid = sid_entry.get()
    hw_scores = hw_entry.get()
    quiz_scores = quiz_entry.get()
    midterm_score = midterm_entry.get()
    final_score = final_entry.get()

    student_data = get_student_data_by_sid(data, sid)

    if student_data:
        # Update the scores if values are provided, preserving the existing scores
        if hw_scores:
            student_data[4:7] = hw_scores.split(',')
        if quiz_scores:
            student_data[7:11] = quiz_scores.split(',')
        if midterm_score:
            student_data[11] = midterm_score
        if final_score:
            student_data[12] = final_score

        write_csv_file(file_path, data)
        messagebox.showinfo("Success", "Student scores updated successfully.")
        refresh_listbox()
        update_scores_window.destroy()
    else:
        messagebox.showerror("Error", "Student not found.")



def display_csv_data():
    # Open a file dialog to select the CSV file
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if file_path:
        global data
        data = read_csv_file(file_path)

        # Create a new Tkinter window
        window = tk.Tk()
        window.title("CSV Data Display")

        global listbox
        # Create a Tkinter Listbox to display the CSV data
        listbox = tk.Listbox(window, width=70, height=20)
        listbox.pack()

        def refresh_listbox():
            listbox.delete(0, tk.END)
            headers = data[0]
            listbox.insert(tk.END, ', '.join(headers))
            for row in data[1:]:
                listbox.insert(tk.END, ', '.join(row))

        refresh_listbox()

        # Create a "Add or Delete Student" button
        add_button = tk.Button(window, text="Add or Delete Student", command=open_add_user_window)
        add_button.pack()

        # Create a "Search Student Data" button
        search_button = tk.Button(window, text="Search Student Data", command=open_search_window)
        search_button.pack()

        # Create an "Update Scores" button
        update_scores_button = tk.Button(window, text="Update Scores", command=open_update_scores_window)
        update_scores_button.pack()

        # Create a "Search Task Statistics" button
        stats_button = tk.Button(window, text="Search Task", command=open_stats_window)
        stats_button.pack()

        # Create a "Export CSV" button
        export_button = tk.Button(window, text="Export CSV", command=export_csv_data)
        export_button.pack()

        # Start the Tkinter main loop
        window.mainloop()

# Create the main Tkinter window
root = tk.Tk()
root.title("CSV Data Editor")
root.config(width=500, height=500,padx=20,pady=50)
label = Label(
    root, text='WELCOME TO GRADEBOOK. IMPORT FILE BELOW:\n',font=font.Font(size=16))
label.pack()

# Create an "Import" button
import_button = tk.Button(root, text="Import CSV", command=display_csv_data)
import_button.pack()

# Start the Tkinter main loop
root.mainloop()
