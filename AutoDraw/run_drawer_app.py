import tkinter as tk
from tkinter import messagebox
import time
import pyautogui

try:
    from image_handler import Image_handler
    from mouse_automate_black import Mouseomate as Mouseomate_black
except ImportError:
    print("ERROR: Make sure 'image_handler.py' and 'mouse_automate_black.py' are in the same folder.")
    exit()

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Area Selector")
        
        self.image_path = None
        self.image_array = None
        self.draw_area_geo = None
        self.handler = None
        
        self.root.geometry("400x400+100+100")
        self.root.attributes('-alpha', 0.6)
        self.root.wm_attributes("-topmost", 1)
        
        label_text = "1. Select Image & set Output Width.\n"\
                     "2. Click 'Preview' -> This box will resize.\n"\
                     "3. Move the resized box to your target area."
        
        self.label = tk.Label(root, 
                         text=label_text,
                         bg="white", font=("Arial", 10, "bold"))
        self.label.pack(pady=20, padx=20)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        config_frame = tk.Frame(control_frame)
        config_frame.pack(side=tk.LEFT, padx=10)
        
        self.btn_select_image = tk.Button(config_frame, text="1. Select Image", command=self.select_image)
        self.btn_select_image.pack(fill='x', pady=5)
        
        tk.Label(config_frame, text="Output Width (in pixels):").pack()
        self.output_width_var = tk.StringVar(value="300")
        tk.Entry(config_frame, textvariable=self.output_width_var, width=10).pack()

        tk.Label(config_frame, text="Step/Offset (For 5px brush, use 4):").pack()
        self.offset_var = tk.StringVar(value="1")
        tk.Entry(config_frame, textvariable=self.offset_var, width=10).pack()

        action_frame = tk.Frame(control_frame)
        action_frame.pack(side=tk.LEFT, padx=10)

        self.btn_preview = tk.Button(action_frame, text="2. Preview & Resize Box", command=self.preview_image, state=tk.DISABLED)
        self.btn_preview.pack(fill='x', pady=5)

        self.btn_draw = tk.Button(action_frame, text="3. START DRAWING", command=self.start_drawing, 
                                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.btn_draw.pack(fill='x', pady=5)
        
        speed_frame = tk.Frame(control_frame, relief=tk.GROOVE, borderwidth=1)
        speed_frame.pack(side=tk.LEFT, padx=10, fill='y')
        
        tk.Label(speed_frame, text="Speed (seconds)").pack()

        tk.Label(speed_frame, text="Line Duration (lsleep):").pack()
        self.lsleep_var = tk.StringVar(value="0.05")
        tk.Entry(speed_frame, textvariable=self.lsleep_var, width=10).pack()
        
        tk.Label(speed_frame, text="Row Pause (rsleep):").pack()
        self.rsleep_var = tk.StringVar(value="0.01")
        tk.Entry(speed_frame, textvariable=self.rsleep_var, width=10).pack()
        
        self.status_label = tk.Label(root, text="Status: Waiting for image...", bg="white")
        self.status_label.pack(pady=10, fill='x', side=tk.BOTTOM)

    def select_image(self):
        """Uses the static method from your Image_handler to get a path."""
        self.image_path = Image_handler.get_image()
        if not self.image_path:
            return
        
        self.status_label.config(text=f"Image: {self.image_path.split('/')[-1]}")
        self.btn_preview.config(state=tk.NORMAL)
        self.btn_draw.config(state=tk.NORMAL)

    def process_image(self):
        """
        Processes the image based on the GUI window's current size
        and the offset value.
        """
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return False
        
        try:
            self.offset = int(self.offset_var.get())
            if self.offset < 1: self.offset = 1
        except ValueError:
            messagebox.showerror("Error", "Offset must be a positive number.")
            return False
        
        self.root.update_idletasks()
        geo = self.root.geometry()
        size, x, y = geo.split('+')
        
        self.draw_area_geo = {
            "x": int(x),
            "y": int(y),
        }

        self.handler = Image_handler(self.image_path)
        
        try:
            user_defined_width = int(self.output_width_var.get())
            if user_defined_width < 10: user_defined_width = 10
        except ValueError:
            messagebox.showerror("Error", "Output Width must be a number.")
            return False
        
        resize_value_for_handler = user_defined_width / self.offset
        
        self.handler.convert_bandw("black") 
        self.handler.resize(int(resize_value_for_handler))
        
        self.image_array = self.handler.update_array()
        return True

    def preview_image(self):
        """Shows the processed image preview AND resizes the box."""
        if self.process_image():
            
            try:
                final_h, final_w = self.image_array.shape
                screen_w = final_w * self.offset
                screen_h = final_h * self.offset
                current_x = self.draw_area_geo['x']
                current_y = self.draw_area_geo['y']
                
                self.root.geometry(f"{screen_w}x{screen_h}+{current_x}+{current_y}")
                self.status_label.config(text=f"Box resized to {screen_w}x{screen_h}. Close preview.")
            except Exception as e:
                print(f"Error resizing window: {e}")
                self.status_label.config(text="Preview ready. Error resizing box.")
                
            self.handler.im.show()
            self.status_label.config(text="Preview closed. Move box to final position.")

    def start_drawing(self):
        """Hides the window and starts the drawing process."""
        if not self.process_image():
            return

        self.status_label.config(text="Drawing starts in 3 seconds... Move mouse to corner to abort.")
        
        self.root.iconify()
        time.sleep(3)
        
        start_pos = (self.draw_area_geo['x'], self.draw_area_geo['y'])
        
        try:
            lsleep = float(self.lsleep_var.get())
            rsleep = float(self.rsleep_var.get())
        except ValueError:
            messagebox.showerror("Error", "Speeds must be numbers (e.g., 0.05)")
            self.root.deiconify()
            return
        
        try:
            self.status_label.config(text="Drawing... (Outlining & Filling)")
            Mouseomate_black.draw_outline_and_fill(
                self.image_array,
                self.offset,
                rsleep,
                lsleep,
                start_pos
            )
                
            self.status_label.config(text="Drawing complete!")
        except pyautogui.FailSafeException:
            self.status_label.config(text="Drawing aborted by user (FailSafe).")
        
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
