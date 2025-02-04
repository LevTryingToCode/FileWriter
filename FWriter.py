import tkinter as tk
from pathlib import Path
from playsound3 import playsound
import threading

class File_Itself:
    def __init__(self):
        self.all_files = [f.name for f in Path('.').iterdir() if f.is_file() and f.name != "FWriter.py"]
        self.file_containments = []
        self.fwidth = 0
        self.fheight = 0

    def FileList(self):
        return self.all_files

    def FileRead(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            self.file_containments = lines
            self.fwidth = max(len(line.rstrip("\n")) for line in lines)
            self.fheight = len(lines)

    def FileWrite(self, filename, content):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)


class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.file_manager = File_Itself()
        self.root.title("FILE EDITOR")
        self.root.geometry("500x500")

        # Frame a lista és a scrollbar számára
        frame = tk.Frame(root)
        frame.pack(pady=20)

        self.listbox = tk.Listbox(frame, width=50, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        for file in self.file_manager.FileList():
            self.listbox.insert(tk.END, file)

        self.button = tk.Button(root, text="Kiválasztás", command=self.show_selected)
        self.button.pack(pady=10)

        self.selected_file_label = tk.Label(root, text="Nincs kiválasztva", fg="blue")
        self.selected_file_label.pack()

    def show_selected(self):
        """A kiválasztott fájl megnyitása egy új ablakban."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_file = self.listbox.get(selected_index)
            self.selected_file_label.config(text=f"Kiválasztott fájl: {selected_file}")

            # Fájl beolvasása
            self.file_manager.FileRead(selected_file)

            # Új ablak létrehozása
            new_window = tk.Toplevel(self.root)
            new_window.title(f"Szerkesztés: {selected_file}")
            new_window.geometry("600x400")

            # Textbox létrehozása az új ablakban
            text_box = tk.Text(new_window, wrap="word", height=self.file_manager.fheight,
                               width=self.file_manager.fwidth)
            text_box.pack(pady=10, padx=10, expand=True, fill="both")

            # Betöltjük a fájl tartalmát a Text boxba
            text_box.insert(tk.END, ''.join(self.file_manager.file_containments))

            # Mentés gomb az új ablakban
            save_button = tk.Button(new_window, text="Mentés",
                                    command=lambda: self.save_selected(selected_file, text_box))
            save_button.pack(pady=10)

        else:
            self.selected_file_label.config(text="Nincs fájl kiválasztva")

    def save_selected(self, filename, text_box):
        """A TextBox tartalmának mentése a kiválasztott fájlba."""
        content = text_box.get(1.0, tk.END)  # Tartalom lekérése
        self.file_manager.FileWrite(filename, content)  # Mentés fájlba
        print(f"{filename} mentve.")  # Konzol visszajelzés

        # **Playsound külön szálon való indítása, hogy a GUI ne fagyjon be**
        threading.Thread(target=lambda: playsound("Soundeffects/tada.mp3"), daemon=True).start()


# Fő program
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()
