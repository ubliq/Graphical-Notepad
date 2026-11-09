import tkinter as tk
from tkinter import filedialog, messagebox
import os


class NotepadApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Graphical Notepad")
        self.root.geometry("900x600")
        self.root.minsize(600, 400)

        self.current_file: str | None = None

        self._build_menu()
        self._build_editor()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        #добавляем кнопки
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть...", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как...", command=self.save_as_file)
        menubar.add_cascade(label="Файл", menu=file_menu)

        self.root.config(menu=menubar)

    def _build_editor(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(frame, wrap="word", undo=True, font=("Consolas", 12))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(frame, command=self.text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scroll.set)

    #вызов окна при создании нового файла
    def new_file(self):
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.root.title("Graphical Notepad")

    #программируем кнопку открытия нового файла
    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")
            return

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.current_file = path
        self.root.title(f"{os.path.basename(path)} — Graphical Notepad")

    # программируем кнопки сохранения файла
    def save_file(self):
        if self.current_file is None:
            return self.save_as_file()
        return self._write_to_file(self.current_file)


    def save_as_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not path:
            return False
        return self._write_to_file(path)

    # создаём окно ошибки
    def _write_to_file(self, path: str) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END).rstrip("\n"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
            return False
        self.current_file = path
        self.root.title(f"{os.path.basename(path)} — Graphical Notepad")
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()