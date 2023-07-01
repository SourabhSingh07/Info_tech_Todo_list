from tkinter import *
from tkinter import messagebox, filedialog
from datetime import date
from tkcalendar import DateEntry

today_date = date.today()
# class named task with title, discription , status, date
class Task:
    def __init__(self, title, description, status, date):
        self.title = title
        self.description = description
        self.status = status
        self.date = date

    def __str__(self):
        return f"Remainder: {self.date}\nTitle: {self.title}\nDescription: {self.description}\nStatus: {self.status}"

#  class with method add_task, delete_task,view_task,save_task,load_task and user_date
class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task):
        self.tasks.remove(task)

    def view_tasks(self):
        if not self.tasks:
            return "No tasks found."
        else:
            return str(self.tasks)

    def save_tasks(self, filename):
        try:
            with open(filename, "w") as file:
                for task in self.tasks:
                    file.write(f"{task.date},{task.title},{task.description},{task.status}\n")
            return "Tasks saved successfully."
        except Exception as e:
            return f"Error saving tasks: {str(e)}"

    def load_tasks(self, filename):
        self.tasks = []
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    values = line.strip().split(",")
                    task = Task(values[1], values[2], values[3], values[0])
                    self.tasks.append(task)
            return "Tasks loaded successfully."
        except Exception as e:
            return f"Error loading tasks: {str(e)}"

    def users_date(self):
        for task in self.tasks:
            date = task.date.split('/')
            if today_date.month == int(date[0]) and today_date.day == int(date[1]) and today_date.year == int(
                    str(20) + date[2]):
                messagebox.showinfo("Remainder", f"Remainder task: {task.title}")


class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.todo_list = ToDoList()
        self.create_widgets()

    def create_widgets(self):
        self.to_do_text = Canvas(root, width=400, height=50, background='#3399FF', highlightthickness=0)
        self.to_do_text.create_text(200, 30, text='To-Do List', font='Algerian 40 italic', fill='#FF0000')
        self.to_do_text.pack()

        self.task_frame = Frame(root, bg='#3399FF')
        self.task_frame.pack(pady=20)

        self.task_label = Label(self.task_frame, font='Kokila 15 bold', text='Task:', bg='#3399FF')
        self.task_label.grid(row=0, column=0)

        self.description_label = Label(self.task_frame, font='Kokila 15 bold', text='Description:', bg='#3399FF')
        self.description_label.grid(row=1, column=0)

        self.status_label = Label(self.task_frame, font='Kokila 15 bold', text='Status:', bg='#3399FF')
        self.status_label.grid(row=2, column=0)

        self.date_label = Label(self.task_frame, font='Kokila 15 bold', text='Date:', bg='#3399FF')
        self.date_label.grid(row=3, column=0)

        self.enter_task = Entry(self.task_frame, width=50)
        self.enter_task.grid(row=0, column=1)

        self.enter_description = Entry(self.task_frame, width=50)
        self.enter_description.grid(row=1, column=1)

        self.enter_status = Entry(self.task_frame, width=50)
        self.enter_status.grid(row=2, column=1)

        self.Enter_date = DateEntry(self.task_frame)
        self.Enter_date.grid(row=3, column=1)
        self.Enter_date.delete(0,END)

        self.task_listbox = Listbox(root, font="Kokila 15 bold")
        self.task_listbox.pack(fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.task_listbox)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.status_frame = Frame(root, bg='#CCE5FF')
        self.status_frame.pack(fill=X)

        self.add_button = Button(self.status_frame, fg='black', font='Kokila 18', text='Add', borderwidth=0,bg='#CCE5FF', command=self.add_task)
        self.add_button.pack(side=LEFT, padx=5)

        self.save = PhotoImage(file='save.png')
        self.save_button = Button(self.status_frame, image=self.save, borderwidth=0, bg='#CCE5FF',command=self.save_tasks)
        self.save_button.pack(side=LEFT, padx=30, pady=2)

        self.view_button = Button(self.status_frame, fg='black', font='Kokila 18', text='View', borderwidth=0,bg='#CCE5FF', command=self.view_tasks)
        self.view_button.pack(side=LEFT, padx=5)

        self.open_image = PhotoImage(file='open.png')
        self.load_button = Button(self.status_frame, image=self.open_image, borderwidth=0, bg='#CCE5FF',command=self.load_tasks)
        self.load_button.pack(side=LEFT, padx=30, pady=2)

        self.delete = PhotoImage(file='delete.png')
        self.delete_button = Button(self.status_frame, image=self.delete, borderwidth=0, bg='#CCE5FF',command=self.delete_task)
        self.delete_button.pack(side=LEFT, padx=25, pady=2)

        self.delete_all_button = Button(self.status_frame, fg='black', font='Kokila 18', text='Delete all',borderwidth=0, bg='#CCE5FF', command=self.delete_all)
        self.delete_all_button.pack(side=LEFT, padx=5)

    def add_task(self):
        title = self.enter_task.get()
        description = self.enter_description.get()
        status = self.enter_status.get()
        date = self.Enter_date.get()
        if title and description and status and date:
            task = Task(title, description, status, date)
            self.todo_list.add_task(task)
            self.todo_list.users_date()
            self.update_task_list()
            self.clear_input_fields()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.todo_list.tasks[selected_index[0]]
            self.todo_list.delete_task(task)

            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def view_tasks(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.todo_list.tasks[selected_index[0]]
            messagebox.showinfo("Task Details", task)
        else:
            messagebox.showwarning("Warning", "Please select a task to view.")

    def save_tasks(self):
        filename = filedialog.asksaveasfilename(title="Save Tasks", defaultextension=".txt",filetypes=(("Text files", "*.txt"),))
        if filename:
            result = self.todo_list.save_tasks(filename)
            messagebox.showinfo("Save Tasks", result)

    def load_tasks(self):
        filename = filedialog.askopenfilename(title="Load Tasks", filetypes=(("Text files", "*.txt"),))
        if filename:
            result = self.todo_list.load_tasks(filename)
            messagebox.showinfo("Load Tasks", result)
            self.todo_list.users_date()
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to load.")

    def delete_all(self):
        self.clear_input_fields()
        self.todo_list.tasks = []
        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, END)
        for task in self.todo_list.tasks:
            self.task_listbox.insert(END, task.title)

    def clear_input_fields(self):
        self.enter_task.delete(0, END)
        self.enter_description.delete(0, END)
        self.enter_status.delete(0, END)

    def remainder(self):
        self.todo_list.users_date()
        root.after(60000, self.remainder)


root = Tk()
root.geometry("500x500")
root.title("To-Do List")
root.configure(bg='#3399FF')
root.minsize(width=425,height=335)
todolist_app = ToDoListApp(root)
todolist_app.remainder()
root.mainloop()
