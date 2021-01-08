import tkinter as tk

def info_dialogue(dialogue, function, *args, **kwargs):
      confirm_window = tk.Toplevel()
      screen_width = confirm_window.winfo_screenwidth()
      screen_height = confirm_window.winfo_screenheight()
      confirm_window.geometry("+{0}+{1}".format(screen_width//2, screen_height//2))
      confirm_window.grab_set()
      greeting = tk.Label(master=confirm_window, text=dialogue)
      greeting.pack()
      frame = tk.Frame(master=confirm_window, borderwidth=5)
      frame.pack()
      def ok_call():
          confirm_window.grab_release()
          confirm_window.destroy()
          function(*args, **kwargs)
      button1 = tk.Button(master=frame, command=ok_call, text="Ok")
      button1.pack()
