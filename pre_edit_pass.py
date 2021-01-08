import tkinter as tk
import data_manager as dm
import confirm_dialogue as cd
import edit_pass as ep
import os

def main(old_window=None, return_function=lambda *_: None):
    if old_window:
        old_window.destroy()
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry("{0}x{1}+{2}+{3}".format(screen_width//2, screen_height//2, screen_width//2 - screen_width//4, screen_height//2 - screen_height//4))

    data_manager = dm.Data_manager()
    try:
        data_manager.load_data()
    except:
        pass

    greeting = tk.Label(master=window, text="Edit an entry:")
    greeting.pack()

    frame = tk.Frame(master=window, borderwidth=50)
    frame.pack()

    number_frame = tk.Frame(master=frame, borderwidth=5)
    number_frame.pack(side=tk.LEFT)
    number_label = tk.Label(master=number_frame, text="Number of the entry to be edited:")
    number_entry = tk.Entry(master=number_frame, width=20)
    number_label.pack()
    number_entry.pack()

    error_label = tk.Label(master=window, text="", fg="red")
    error_label.pack()

    def edit_call():
        number = number_entry.get()
        errors = check_errors(number)
        error_label.configure(text=errors)
        error_label.text = errors
        if errors:
            return
        ep.main(old_window=window, return_function=return_function, continue_function=main, number=number)
        pass

    def check_errors(data):
        if not data or int(data) < 1:
            return "Please provide a valid number to fetch."
        dataset_numbers = [entry["number"] for entry in data_manager.database]
        if not data in dataset_numbers:
            return "That entry does not exist."
        return ""

    button1 = tk.Button(master=frame, command=edit_call, text="edit")
    button1.pack(side=tk.LEFT)

    error_label = tk.Label(master=window, text="", fg="red")
    error_label.pack()

    def main_menu_call():
        nonlocal window
        cd.confirm_dialogue("Return to main menu?", return_function, window)

    main_menu_button = tk.Button(master=window, command=main_menu_call, text="Main menu")
    main_menu_button.pack()

    window.mainloop()
