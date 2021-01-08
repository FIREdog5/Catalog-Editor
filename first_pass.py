import tkinter as tk
import data_manager as dm
import html_compiler as hc
import confirm_dialogue as cd
import info_dialogue as id
import os
from PIL import Image, ImageTk

def main(old_window=None, return_function=lambda *_: None):
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

    name_frame = tk.Frame(master=frame, borderwidth=5)
    name_frame.pack(side=tk.LEFT)
    name_label = tk.Label(master=name_frame, text="Name:")
    name_entry = tk.Entry(master=name_frame, width=50)
    name_label.pack()
    name_entry.pack()

    number_frame = tk.Frame(master=frame, borderwidth=5)
    number_frame.pack(side=tk.LEFT)
    number_label = tk.Label(master=number_frame, text="Number:")
    number_entry = tk.Entry(master=number_frame, width=20)
    number_label.pack()
    number_entry.pack()

    picture_frame = tk.Frame(master=frame, borderwidth=5)
    picture_frame.pack(side=tk.LEFT)
    try:
        img = os.path.join("pictures", data_manager.get_next_picture())
    except EOFError:
        id.info_dialogue("No images remain, redirecting to catalog creator", hc.main, window=window, return_function=return_function)
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
        data_manager.collect_data(data)
        data_manager.save_data()
        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
        description_entry.delete("1.0", tk.END)
        try:
            new_img = os.path.join("pictures", data_manager.get_next_picture())
        except EOFError:
            id.info_dialogue("No images remain, redirecting to catalog creator", hc.main, window=window, return_function=return_function)
        load = Image.open(new_img)
        load = load.resize((250, 250), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        picture_label.configure(image=render)
        picture_label.image = render
        picture_label_text.configure(text=new_img)
        picture_label_text.text = new_img
        img = new_img

    def check_errors(data):
        if not data["name"]:
            return "Please provide a name for the picture."
        if not data["number"] or not data["number"].isnumeric() or int(data["number"]) < 1:
            return "Please provide a valid number for the picture."
        dataset_numbers = [entry["number"] for entry in data_manager.database]
        if data["number"] in dataset_numbers:
            return "A picture in the dataset already uses this number."
        if not data["description"] or data["description"] == "\n":
            return "Please provide a description for the picture."
        if not data["picture"]:
            return "Something went wrong with the picture. Please restart the program."
        return ""

    button = tk.Button(master=window, command=submit_call, text="Save and load next picture")
    button.pack()

    def main_menu_call():
        nonlocal window
        cd.confirm_dialogue("Return to main menu and discard unsaved changes?", return_function, window)

    main_menu_frame = tk.Frame(master=window, borderwidth=50)
    main_menu_frame.pack()
    main_menu_button = tk.Button(master=main_menu_frame, command=main_menu_call, text="Main menu")
    main_menu_button.pack()

    window.mainloop()
