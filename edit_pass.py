import tkinter as tk
import data_manager as dm
import confirm_dialogue as cd
import os
from PIL import Image, ImageTk

def main(old_window=None, return_function=lambda *_: None, continue_function=lambda *_: None, number=None):
    if not number:
        return
    if old_window:
        old_window.destroy()
    window = tk.Tk()
    window.state('zoomed')
    greeting = tk.Label(master=window, text="Fill in the information for the following picture:")
    greeting.pack()
    frame = tk.Frame(master=window, borderwidth=5)
    frame.pack()

    data_manager = dm.Data_manager()
    try:
        data_manager.load_data()
    except:
        pass

    entry = data_manager.get_entry(number)

    name_frame = tk.Frame(master=frame, borderwidth=5)
    name_frame.pack(side=tk.LEFT)
    name_label = tk.Label(master=name_frame, text="Name:")
    name_entry = tk.Entry(master=name_frame, width=50)
    name_label.pack()
    name_entry.pack()
    name_entry.insert(0, entry["name"])

    number_frame = tk.Frame(master=frame, borderwidth=5)
    number_frame.pack(side=tk.LEFT)
    number_label = tk.Label(master=number_frame, text="Number:")
    number_entry = tk.Entry(master=number_frame, width=20)
    number_label.pack()
    number_entry.pack()
    number_entry.insert(0, number)

    picture_frame = tk.Frame(master=frame, borderwidth=5)
    picture_frame.pack(side=tk.LEFT)
    img = entry["picture"]
    load = Image.open(img)
    load = load.resize((250, 250), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    picture_label_text = tk.Label(master=picture_frame, text=img)
    picture_label = tk.Label(master=picture_frame, image=render)
    picture_label_text.pack()
    picture_label.pack()

    description_frame = tk.Frame(master=frame, borderwidth=5)
    description_frame.pack(side=tk.LEFT)
    description_label = tk.Label(master=description_frame, text="Description:")
    description_entry = tk.Text(master=description_frame, width=100)
    description_label.pack()
    description_entry.pack()
    counter = 1
    for line in entry["description"].split("\n"):
        description_entry.insert("{0}.0".format(counter), line + ("\n" if counter < len(entry["description"].split("\n")) - 1 else ""))
        counter += 1

    error_label = tk.Label(master=window, text="", fg="red")
    error_label.pack()

    def submit_call():
        nonlocal img
        data = {}
        data["name"] = name_entry.get()
        data["number"] = number_entry.get()
        data["description"] = description_entry.get("1.0", tk.END)
        data["picture"] = img
        errors = check_errors(data)
        error_label.configure(text=errors)
        error_label.text = errors
        if errors:
            return
        data_manager.modify_data(number, data)
        data_manager.save_data()
        continue_function(old_window=window, return_function=return_function)

    def check_errors(data):
        if not data["name"]:
            return "Please provide a name for the picture."
        if not data["number"] or not data["number"].isnumeric() or int(data["number"]) < 1:
            return "Please provide a valid number for the picture."
        dataset_numbers = [entry["number"] for entry in data_manager.database]
        if data["number"] != number and data["number"] in dataset_numbers:
            return "A picture in the dataset already uses this number."
        if not data["description"] or data["description"] == "\n":
            return "Please provide a description for the picture."
        if not data["picture"]:
            return "Something went wrong with the picture. Please restart the program."
        return ""

    button = tk.Button(master=window, command=submit_call, text="Save changes and edit something else")
    button.pack()

    def delete_function():
        data_manager.remove_entry(number)
        data_manager.save_data()

    def delete_call():
        cd.confirm_dialogue("Are you sure you want to delete this entry?", delete_function)

    delete_frame = tk.Frame(master=window, borderwidth=50)
    delete_frame.pack()
    delete_button = tk.Button(master=delete_frame, command=delete_call, text="Delete this entry", bg="red")
    delete_button.pack()

    def main_menu_call():
        nonlocal window
        cd.confirm_dialogue("Return to main menu and discard unsaved changes?", return_function, window)

    main_menu_frame = tk.Frame(master=window, borderwidth=5)
    main_menu_frame.pack()
    main_menu_button = tk.Button(master=main_menu_frame, command=main_menu_call, text="Main menu")
    main_menu_button.pack()

    window.mainloop()
