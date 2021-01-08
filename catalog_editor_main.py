import tkinter as tk
import first_pass as fp
import html_compiler as hc
import data_manager as dm
import pre_edit_pass as pep

def main(old_window=None, return_function=lambda *_: None):
    if old_window:
        old_window.destroy()
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry("{0}x{1}+{2}+{3}".format(screen_width//2, screen_height//2, screen_width//2 - screen_width//4, screen_height//2 - screen_height//4))
    greeting = tk.Label(master=window, text="Select what you want the program to do:")
    greeting.pack()
    frame = tk.Frame(master=window, borderwidth=50)
    frame.pack()
    def first_pass_call():
        fp.main(old_window=window, return_function=main)
    button1 = tk.Button(master=frame, command=first_pass_call, text="First pass")
    button1.pack(side=tk.LEFT)
    def edit_pass_call():
        pep.main(old_window=window, return_function=main)
    button2 = tk.Button(master=frame, command=edit_pass_call, text="Edit pass")
    button2.pack(side=tk.LEFT)
    def html_call():
        hc.main(old_window=window, return_function=main)
    button2 = tk.Button(master=window, command=html_call, text="Create catalog.html")
    button2.pack()
    window.mainloop()

dm.load_pictures()
main()
