import tkinter as tk
from gui_app import ParticipantApp
from config import APP_SIZE

if __name__ == "__main__":
    root = tk.Tk()
    
    app_gui = ParticipantApp(root)

    window_width = APP_SIZE[0]
    window_height = APP_SIZE[1]
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()