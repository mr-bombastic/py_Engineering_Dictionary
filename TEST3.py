import tkinter as tk
from tkinter import messagebox

def answer():
    messagebox.showerror("Answer", "Sorry, no answer available")

def callback():
    if messagebox.askyesno('Verify', 'Really quit?'):
        messagebox.showwarning('Yes', 'Not yet implemented')
    else:
        messagebox.showinfo('No', 'Quit has been cancelled')

tk.Button(text='Quit', command=callback).pack(fill=tk.X)
tk.Button(text='Answer', command=answer).pack(fill=tk.X)
tk.mainloop()