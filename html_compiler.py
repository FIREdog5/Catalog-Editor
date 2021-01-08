import tkinter as tk
import data_manager as dm
import confirm_dialogue as cd
import os

def main(old_window=None, return_function=lambda *_: None):
    if old_window:
        old_window.destroy()
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry("{0}x{1}+{2}+{3}".format(screen_width//2, screen_height//2, screen_width//2 - screen_width//4, screen_height//2 - screen_height//4))
    greeting = tk.Label(master=window, text="HTML catalog compiler settings")
    greeting.pack()

    frame = tk.Frame(master=window, borderwidth=50)
    frame.pack()

    width_frame = tk.Frame(master=frame, borderwidth=5)
    width_frame.pack(side=tk.LEFT)
    width_label = tk.Label(master=width_frame, text="Image width:")
    width_entry = tk.Entry(master=width_frame, width=20)
    width_label.pack()
    width_entry.pack()
    width_entry.insert(0, "200")

    height_frame = tk.Frame(master=frame, borderwidth=5)
    height_frame.pack(side=tk.LEFT)
    height_label = tk.Label(master=height_frame, text="Image height:")
    height_entry = tk.Entry(master=height_frame, width=20)
    height_label.pack()
    height_entry.pack()
    height_entry.insert(0, "200")

    def compile_html_call():
        error_label.configure(text="")
        error_label.text = ""
        try:
            compile_html(int(width_entry.get()), int(height_entry.get()))
        except:
            error = "Compilation failed, something went wrong. Make sure your image sizes are numbers."
            error_label.configure(text=error)
            error_label.text = error

    button1 = tk.Button(master=frame, command=compile_html_call, text="Compile HTML")
    button1.pack(side=tk.LEFT)

    error_label = tk.Label(master=window, text="", fg="red")
    error_label.pack()

    def verify_database_call():
        data_manager = dm.Data_manager()
        try:
            data_manager.load_data()
        except:
            pass
        missing_count = 0
        extra_count = 0
        duplicate_picture_count = 0
        duplicate_number_count = 0
        duplicate_name_count = 0
        dataset_pictures = [entry["picture"].split("\\")[1] for entry in data_manager.database]
        file_system_pictures = os.listdir("pictures")
        should_add_skips = data_manager.index >= len(data_manager.database)
        for file in file_system_pictures:
            if not file in dataset_pictures:
                missing_count += 1
                if should_add_skips:
                    data_manager.got_skipped.append(file)

        for file in dataset_pictures:
            if not file in file_system_pictures:
                extra_count += 1
            if dataset_pictures.count(file) > 1:
                duplicate_picture_count += 1

        dataset_numbers = [entry["number"] for entry in data_manager.database]
        for number in dataset_numbers:
            if dataset_numbers.count(number) > 1:
                duplicate_number_count += 1

        dataset_names = [entry["name"] for entry in data_manager.database]
        for name in dataset_names:
            if dataset_names.count(name) > 1:
                duplicate_name_count += 1

        missing_count_label.configure(text="")
        missing_count_label.text = ""
        extra_count_label.configure(text="")
        extra_count_label.text = ""
        duplicate_picture_count_label.configure(text="")
        duplicate_picture_count_label.text = ""
        duplicate_number_count_label.configure(text="")
        duplicate_number_count_label.text = ""
        duplicate_name_count_label.configure(text="")
        duplicate_name_count_label.text = ""

        if missing_count:
            missing_count_label.configure(text="There are {0} missing pictures from your dataset. Use first pass to correct this".format(missing_count))
            missing_count_label.text = "There are {0} missing pictures from your dataset. Use first pass to correct this".format(missing_count)
        if extra_count:
            extra_count_label.configure(text="There are {0} pictures in your dataset that are no longer in the pictures folder.".format(extra_count))
            extra_count_label.text = "There are {0} pictures in your dataset that are no longer in the pictures folder.".format(extra_count)
        if duplicate_picture_count:
            duplicate_picture_count_label.configure(text="There are {0} duplicate pictures in your dataset.".format(duplicate_picture_count//2))
            duplicate_picture_count_label.text = "There are {0} duplicate pictures in your dataset.".format(duplicate_picture_count//2)
        if duplicate_number_count:
            duplicate_number_count_label.configure(text="There are {0} duplicate numbers in your dataset. Honestly this souldn't be possible without modifying savestate.json, please report this as a bug".format(duplicate_number_count//2))
            duplicate_number_count_label.text = "There are {0} duplicate numbers in your dataset. Honestly this souldn't be possible without modifying savestate.json, please report this as a bug".format(duplicate_number_count//2)
        if duplicate_name_count:
            duplicate_name_count_label.configure(text="There are {0} duplicate names in your dataset.".format(duplicate_name_count//2))
            duplicate_name_count_label.text = "There are {0} duplicate names in your dataset.".format(duplicate_name_count//2)

    button2 = tk.Button(master=window, command=verify_database_call, text="Verify Database")
    button2.pack()

    missing_count_label = tk.Label(master=window, text="", fg="red")
    missing_count_label.pack()
    extra_count_label = tk.Label(master=window, text="", fg="red")
    extra_count_label.pack()
    duplicate_picture_count_label = tk.Label(master=window, text="", fg="red")
    duplicate_picture_count_label.pack()
    duplicate_number_count_label = tk.Label(master=window, text="", fg="red")
    duplicate_number_count_label.pack()
    duplicate_name_count_label = tk.Label(master=window, text="", fg="red")
    duplicate_name_count_label.pack()

    def main_menu_call():
        nonlocal window
        cd.confirm_dialogue("Return to main menu?", return_function, window)

    main_menu_button = tk.Button(master=window, command=main_menu_call, text="Main menu")
    main_menu_button.pack()

    window.mainloop()

HTML_HEADER = '<html>\n<head>\n<style>\ntable, th, td {\n  border: 1px solid black;\n}\nth, td {\n  padding: 10px;\n}\n</style>\n</head>\n<body>\n<table>\n  <tr>\n    <th>Number</th>\n    <th>Name</th>\n    <th>Image</th>\n    <th>Description</th>\n  </tr>\n\n'
HTML_IMAGE = '  <tr>\n    <td>{0}</td>\n    <td>{1}</td>\n    <td><img src="{2}" style="width:{3}px;height:{4}px;"></td>\n    <td>{5}</td>\n  </tr>\n'
HTML_FOOTER = '\n</table>\n</body>\n</html>\n'

def compile_html(width, height):
    data_manager = dm.Data_manager()
    try:
        data_manager.load_data()
    except:
        pass
    html_data = HTML_HEADER
    data_manager.database.sort(key=lambda x:int(x["number"]))
    for entry in data_manager.database:
        html_data += HTML_IMAGE.format(entry["number"], entry["name"], entry["picture"], width, height, entry["description"].replace("\n", "<br>"))
    html_data += HTML_FOOTER
    f = open("catalog.html", "w")
    f.write(html_data)
    f.close()
