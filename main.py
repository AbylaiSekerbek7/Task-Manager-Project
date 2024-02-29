# Sekerbek Abylaikhan SE2329

# imports
import tkinter as tk # library for GUI
import json # library for save and load data in json file
import pygame # library for sounds
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime # library for current date and time

class TaskManagerApp(tk.Tk):
    def __init__(self):
        # At first we need to initialize
        super().__init__()
        pygame.init()

        # Window configurations
        self.title("Task Manager App") # Just title of the window
        self.geometry("700x700") # The size of window, you can change as you want
        self.configure(bg="#DCF2F1") # Background of window
        self.dark_mode = False # Flag to change the background on Darker, Lighter

        # Loading sounds
        # I have already uploaded mp3 sounds, in sounds directory
        self.add_sound_delete = pygame.mixer.Sound('./sounds/light-switch-156813.mp3')
        self.done_sound = pygame.mixer.Sound('./sounds/ping-82822.mp3')

        # Style configurations
        style = ttk.Style()
        style.configure('Blue.TButton', background='blue')    # Blue color
        style.configure('Green.TButton', background='green')  # Green color
        style.configure('Red.TButton', background='red')      # Red color

        # Button for switching background of screen
        self.btnColor = tk.Button(self, text="Darker", command=self.toggle_color, fg="black", bg="#4158D0", )
        self.btnColor.place(relx=0.1, rely=0.1, anchor="center")

        # Label for displaying current system date and time
        self.current_datetime_label = ttk.Label(self, text="", font=("TkDefaultFont", 12))
        self.current_datetime_label.pack(side=tk.TOP, pady=5)

        # Task input
        self.task_input = ttk.Entry(self, font=("TkDefaultFont", 16), width=30, style="Custom.TEntry")
        self.task_input.pack(pady=10)
        self.task_input.insert(0, "Enter your todo here...")

        # Label to display selected date
        self.date_label = tk.Label(self, text="Selected deadline: ")
        self.date_label.pack(pady=5)

        # Date input
        self.date_input = DateEntry(self, width=38, background='darkblue', foreground='white', borderwidth=2)
        self.date_input.pack(pady=5)

        # Task List
        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons to Add Task, Done Task, Delete Task, View Stats
        ttk.Button(self, text="Add", command=self.add_task, style="Blue.TButton").pack(pady=5)
        ttk.Button(self, text="Done", command=self.mark_done, style="Green.TButton").pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", command=self.delete_task, style="Red.TButton").pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(self, text="View Stats", command=self.view_stats, style="Blue.TButton").pack(side=tk.BOTTOM, pady=10)

        self.update_current_datetime() # This is for updating every 1 second current date and time
        self.load_tasks() # And in logical we must at first load tasks from 'tasks.json' (our tasks data)

    # All Functions

    # def for switching the background of screen
    def toggle_color(self):
            if self.dark_mode:
                self.configure(bg="#DCF2F1")
                self.btnColor.configure(text="Darker")
                self.dark_mode = False
            else:
                self.configure(bg="#0F1035")
                self.btnColor.configure(text="Lighter")
                self.dark_mode = True

    # def to update date and time, every 1 second
    def update_current_datetime(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_datetime_label.config(text=f"Current Date and Time: {current_datetime}")
        self.after(1000, self.update_current_datetime)

    # def to add task in list
    def add_task(self):
        task = self.task_input.get() # Getting user task input
        deadline = self.date_input.get() # Getting user selected deadline
        if task.strip() == "": # Just in case that we can't add empty task
            messagebox.showerror("Invalid task", "Please enter a none empty task.")
            return
        try:
            if self.date_input.get_date() < datetime.now().date(): # Simple if to check the deadline
                task_color = "red"
            else:
                task_color = "orange"
            # Adding task to list
            task_with_deadline = f"{task} {deadline}"
            self.task_list.insert(tk.END, task_with_deadline)
            self.task_list.itemconfig(tk.END, fg=task_color)
            self.task_input.delete(0, tk.END)
            self.date_input.delete(0, tk.END)
            self.date_label.config(text=f"Selected deadline: {deadline}")
        except ValueError:
            # If user entered not correct value, we show messagebox error
            messagebox.showerror("Invalid Deadline", "Please enter deadline in DD/MM/YYYY format.")

        self.save_tasks() # Saving the task in json
        self.add_sound_delete.play() # And playing sound

    # def to mark done selected task
    def mark_done(self):
        selected_task_index = self.task_list.curselection() # Getting the selected task from list
        if selected_task_index: # If we have the index
            self.task_list.itemconfig(selected_task_index, fg="green") # We change the color on 'green'
            self.save_tasks() # Saving new changes in json
            self.done_sound.play() # And playing sound

    # def to delete selected task from list
    def delete_task(self):
        selected_task_index = self.task_list.curselection() # Getting the selected task from list
        if selected_task_index: # If we have the index
            self.task_list.delete(selected_task_index) # Just with using function delete() deleting task by index
            self.save_tasks() # Saving new changes in json
            self.add_sound_delete.play() # And playing sound

    # def to view stats of list
    def view_stats(self):
        total_tasks = self.task_list.size() # Getting the size of list
        completed_tasks = sum(1 for i in range(total_tasks) if "green" in self.task_list.itemcget(i, "fg")) # And in for, we chose only completed tasks, and getting the sum - count
        inprocess_tasks = sum(1 for i in range(total_tasks) if "orange" in self.task_list.itemcget(i, "fg")) # And in for, we chose only in process tasks, and getting the sum - count
        overdue_tasks = sum(1 for i in range(total_tasks) if "red" in self.task_list.itemcget(i, "fg")) # And in for, we chose only overdue tasks, and getting the sum - count
        messagebox.showinfo("Task Statistics", f"Total Tasks: {total_tasks}\nCompleted Tasks: {completed_tasks}\nIn Process Tasks: {inprocess_tasks}\nOverdue Tasks: {overdue_tasks}") # Showing the stat in messagebox

    # def to Load Tasks from json
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f: # Opening the file as f
                data = json.load(f) # with using function load() we loading the file
                for task in data:
                    task_text = f"{task['text']} {task['deadline']}"
                    self.task_list.insert(tk.END, task_text)
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError as e:
            # If we not found the file, we print the error
            print("Exception on loading tasks - ", e)

    # def to Save Tasks in json
    def save_tasks(self):
        data = [] # At first we need to create a empty array
        for i in range(self.task_list.size()): # Taking every task in task_list
            task_with_deadline = self.task_list.get(i)
            text, deadline = task_with_deadline.rsplit(' ', 1)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color, "deadline": deadline}) # And appending the text, color, deadline
        with open("tasks.json", "w") as f:
            json.dump(data, f) # dump function to format the data array in Json object

    # def to check deadline of task
    def check_deadline_tasks(self):
        current_datetime = datetime.now() # getting the current datetime
        for i in range(self.task_list.size()):
            task_with_deadline = self.task_list.get(i)
            task_text, deadline_str = task_with_deadline.rsplit(' ', 1) # rsplit to split a string into a list of substring, so we getting deadline_str
            deadline = datetime.strptime(deadline_str, "%m/%d""/%y") # formating the deadline
            task_color = self.task_list.itemcget(i, "fg") # and getting the current color

            if task_color == "orange": # The rule that we check only the tasks that in process
                if deadline < current_datetime: # So if the deadline passed
                    self.task_list.itemconfig(i, fg="red") # We changing the color on red
                else:
                    self.task_list.itemconfig(i, fg="orange") # Else we just don't touching it

        self.after(1000, self.check_deadline_tasks) # To check every 1 second

if __name__ == '__main__':
    app = TaskManagerApp() # Creating app
    app.check_deadline_tasks() # Running the ckecker
    app.mainloop() # And running the mainloop