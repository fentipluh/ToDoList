import tkinter as tk
from tkinter import ttk
import sqlite3

def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        save_task(task)
        entry.delete(0, tk.END)

def edit_task():
    try:
        selected_task = listbox.curselection()
        task_to_edit = listbox.get(selected_task)
        entry.delete(0, tk.END)
        entry.insert(tk.END, task_to_edit)
        delete_task_from_db(task_to_edit)
        listbox.delete(selected_task)
    except:
        pass

def delete_task():
    try:
        selected_task = listbox.curselection()
        deleted_task = listbox.get(selected_task)
        delete_task_from_db(deleted_task)
        listbox.delete(selected_task)
    except:
        pass

def save_task(task):
    conn = sqlite3.connect('task_scheduler.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def delete_task_from_db(task):
    conn = sqlite3.connect('task_scheduler.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE task_name=?", (task,))
    conn.commit()
    conn.close()

def update_task(task, new_task):
    conn = sqlite3.connect('task_scheduler.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET task_name=? WHERE task_name=?", (new_task, task))
    conn.commit()
    conn.close()

root = tk.Tk()
root.title("Daily tasks")

style = ttk.Style()

style.configure("TButton", padding=10, relief="flat", foreground="black", background="#3498db")

frame = ttk.Frame(root)
frame.pack(padx=50, pady=50)

label = ttk.Label(frame, text="Список задач:")
label.pack()

listbox = tk.Listbox(frame, height=10, font=("Helvetica", 12))
listbox.pack(pady=10)

entry = ttk.Entry(frame, font=("Helvetica", 12))
entry.pack()

add_button = ttk.Button(frame, text="Добавить задачу", command=add_task)
add_button.pack(pady=10)

edit_button = ttk.Button(frame, text="Изменить задачу", command=edit_task)
edit_button.pack(pady=5)

delete_button = ttk.Button(frame, text="Удалить задачу", command=delete_task)
delete_button.pack(pady=5)


conn = sqlite3.connect('task_scheduler.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tasks (task_name TEXT)")
conn.commit()
conn.close()

root.mainloop()
