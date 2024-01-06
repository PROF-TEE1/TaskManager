# Using a GUI library like Tkinter to create a Task Management coupled with an alarm

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import winaudio

class TaskManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        # Create variables
        self.task_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.tasks = []

        # Create widgets
        tk.Label(master, text="Task:").pack()
        self.task_entry = tk.Entry(master, textvariable=self.task_var, width=30)
        self.task_entry.pack()

        tk.Label(master, text="Due Date (YYYY-MM-DD HH:MM):").pack()
        self.due_date_entry = tk.Entry(master, textvariable=self.due_date_var, width=30)
        self.due_date_entry.pack()

        tk.Button(master, text="Add Task", command=self.add_task).pack()

        tk.Label(master, text="Task List:").pack()
        self.task_listbox = tk.Listbox(master, selectmode=tk.SINGLE, width=40, height=10)
        self.task_listbox.pack()

        tk.Button(master, text="Set Alarm", command=self.set_alarm).pack()

    def add_task(self):
        task_text = self.task_var.get().strip()
        due_date_text = self.due_date_var.get().strip()

        if task_text and due_date_text:
            try:
                due_date = datetime.strptime(due_date_text, "%Y-%m-%d %H:%M")
                task = {"text": task_text, "due_date": due_date}
                self.tasks.append(task)
                self.task_listbox.insert(tk.END, f"{task_text} (Due: {due_date_text})")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Invalid date format. Please use YYYY-MM-DD HH:MM.")
        else:
            messagebox.showwarning("Incomplete Input", "Please enter both task and due date.")

    def set_alarm(self):
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            selected_task = self.tasks[selected_task_index[0]]
            due_date = selected_task["due_date"]
            current_time = datetime.now()

            if current_time < due_date:
                time_difference = due_date - current_time
                seconds_difference = time_difference.total_seconds()
                self.master.after(int(seconds_difference * 1000), self.show_alarm, selected_task["text"])
            else:
                messagebox.showinfo("Task Expired", "The selected task's due date has already passed.")
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to set an alarm.")

    def show_alarm(self, task_text):
        # play sound
        winaudio.play_wave_sound("sample.wav", winaudio.SND_SYNC)
        messagebox.showinfo("Task Reminder", f"It's time for: {task_text}")
        
        

def main():
    root = tk.Tk()
    task_manager = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
