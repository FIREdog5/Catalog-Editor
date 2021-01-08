import tkinter as tk

def confirm_dialogue(dialogue, function, *args):
      confirm_window = tk.Toplevel()
      screen_width = confirm_window.winfo_screenwidth()
      screen_height = confirm_window.winfo_screenheight()
      confirm_window.geometry("+{0}+{1}".format(screen_width//2, screen_height//2))
      confirm_window.grab_set()
      greeting = tk.Label(master=confirm_window, text=dialogue)
      greeting.pack()
      frame = tk.Frame(master=confirm_window, borderwidth=5)
      frame.pack()
      def yes_call():
          confirm_window.grab_release()
          confirm_window.destroy()
          function(*args)
      button1 = tk.Button(master=frame, command=yes_call, text="Yes", bg="green")
      button1.pack(side=tk.LEFT)
      def no_call():
          confirm_window.grab_release()
          confirm_window.destroy()
      button2 = tk.Button(master=frame, command=no_call, text="No", bg="red")
      button2.pack(side=tk.LEFT)
