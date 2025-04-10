# region_selector.py

import tkinter as tk
import os
from screeninfo import get_monitors

class ScreenRegionSelector:
    def __init__(self):
        monitors = get_monitors()
        print("Monitors detected:", monitors)

        # Use second monitor if available
        if len(monitors) > 1:
            screen = monitors[1]
        else:
            screen = monitors[0]

        self.root = tk.Tk()
        self.root.title("Select screen region")
        self.root.geometry(f"{screen.width}x{screen.height}+{screen.x}+{screen.y}")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.3)
        self.root.config(bg='black')

        self.start_x = self.start_y = self.rect = None

        self.canvas = tk.Canvas(self.root, cursor="cross", bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.root, text="Click and drag to select the screen region. Press ESC to cancel.",
                              bg="black", fg="white", font=("Arial", 16))
        self.label.place(relx=0.5, rely=0.01, anchor='n')

        self.canvas.bind("<ButtonPress-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.root.mainloop()

    def on_start(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                 outline='red', width=2)

    def on_drag(self, event):
        curr_x, curr_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curr_x, curr_y)

    def on_release(self, event):
        end_x, end_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        left = int(min(self.start_x, end_x))
        top = int(min(self.start_y, end_y))
        width = int(abs(end_x - self.start_x))
        height = int(abs(end_y - self.start_y))

        print(f"Selected Region: (left={left}, top={top}, width={width}, height={height})")
        self.root.destroy()

        # Write directly to config.py
        with open("config.py", "r") as f:
            lines = f.readlines()

        with open("config.py", "w") as f:
            for line in lines:
                if "CAPTURE_REGION" in line:
                    f.write(f"CAPTURE_REGION = ({left}, {top}, {width}, {height})\n")
                else:
                    f.write(line)

if __name__ == "__main__":
    ScreenRegionSelector()
