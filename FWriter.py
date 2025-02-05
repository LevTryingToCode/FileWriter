import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os
from playsound3 import playsound
import threading
import sys


class File_Itself:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.all_files = [f.name for f in Path(self.base_dir).iterdir() if f.is_file() and f.name != "FWriter.py"]

    def FileRead(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        return lines, 10, 10

    def FileWrite(self, filename, content):
        file_path = os.path.join(self.base_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)


class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.file_manager = File_Itself()
        self.root.title("FILE EDITOR")
        self.root.geometry("500x300")

        self.browse_button = tk.Button(root, text="Tallózás", command=self.browse_file)
        self.browse_button.pack(pady=20)

        self.selected_file_label = tk.Label(root, text="Nincs kiválasztva", fg="blue")
        self.selected_file_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Válassz egy fájlt")
        if file_path:
            self.selected_file_label.config(text=f"Kiválasztott fájl: {os.path.basename(file_path)}")
            self.open_file_editor(file_path)

    def open_file_editor(self, file_path):
        file_content, fwidth, fheight = self.file_manager.FileRead(file_path)

        new_window = tk.Toplevel(self.root)
        new_window.title(f"Szerkesztés: {os.path.basename(file_path)}")
        new_window.geometry("600x400")

        text_box = tk.Text(new_window, wrap="word", height=fheight, width=fwidth)
        text_box.pack(pady=10, padx=10, expand=True, fill="both")
        text_box.insert(tk.END, ''.join(file_content))

        # Javított gombnyomás-ellenőrzés
        save_button = tk.Button(new_window, text="Mentés",
                                command=lambda: self.on_save(file_path, text_box, new_window))
        save_button.pack(pady=10)

    def on_save(self, file_path, text_box, window):
        content = text_box.get(1.0, tk.END)
        self.file_manager.FileWrite(file_path, content)
        print(f"{file_path} mentve.")
        threading.Thread(target=lambda: playsound("Soundeffects/tada.mp3"), daemon=True).start()
        window.destroy()

        self.selected_file_label = tk.Label(root, text=f"{file_path} mentve ( ha nem akkor sory :-( )", fg="blue")
        self.selected_file_label.pack()


# Fő program
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()


    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Válassz egy fájlt")
        if file_path:
            self.selected_file_label.config(text=f"Kiválasztott fájl: {os.path.basename(file_path)}")
            self.open_file_editor(file_path)

    def open_file_editor(self, file_path):
        file_content, fwidth, fheight = self.file_manager.FileRead(file_path)

        new_window = tk.Toplevel(self.root)
        new_window.title(f"Szerkesztés: {os.path.basename(file_path)}")
        new_window.geometry("600x400")

        text_box = tk.Text(new_window, wrap="word", height=fheight, width=fwidth)
        text_box.pack(pady=10, padx=10, expand=True, fill="both")
        text_box.insert(tk.END, ''.join(file_content))

        save_button = tk.Button(new_window, text="Mentés",
                                command=lambda: self.on_save(file_path, text_box, new_window))
        save_button.pack(pady=10)

        def on_save(self, file_path, text_box, new_window):
            content = text_box.get("1.0", tk.END)
            self.file_manager.FileWrite(file_path, content)
            print(f"{file_path} mentve")
            new_window.destroy()
            threading.Thread(target=lambda: playsound("Soundeffects/tada.mp3"), daemon=True).start()



    def save_selected(self, file_path, text_box):
        content = text_box.get(1.0, tk.END)
        self.file_manager.FileWrite(file_path, content)
        print(f"{file_path} mentve.")



# Fő program
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()
