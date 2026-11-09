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
        self._build_statusbar()
        self._bind_shortcuts()


    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новый       Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Открыть...  Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Сохранить   Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Сохранить как... Ctrl+Shift+S", command=self.save_as_file)
        menubar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Отменить    Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Повторить   Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать    Ctrl+X",
                              command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Копировать  Ctrl+C",
                              command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставить    Ctrl+V",
                              command=lambda: self.text.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Правка", menu=edit_menu)

        self.root.config(menu=menubar)

    def _build_editor(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(frame, wrap="word", undo=True, font=("Consolas", 12))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(frame, command=self.text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scroll.set)
        self.text.bind("<KeyRelease>", lambda e: self._update_status())
        self.text.bind("<ButtonRelease-1>", lambda e: self._update_status())

    #вызов окна при создании нового файла
    def new_file(self):
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.root.title("Graphical Notepad")
        self._update_status()

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
        self._update_status()

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

    def _bind_shortcuts(self):
        self.root.bind_all("<Control-n>", lambda e: self.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file())
        self.root.bind_all("<Control-S>", lambda e: self.save_as_file())
        self.root.bind_all("<Control-z>", lambda e: self.undo())
        self.root.bind_all("<Control-y>", lambda e: self.redo())

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    def _build_statusbar(self):
        self.status = tk.Label(self.root, text="Строка 1, Столбец 1 | Символов: 0",
                               anchor="w", padx=8, pady=4)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def _update_status(self):
        idx = self.text.index(tk.INSERT)
        line, col = idx.split(".")
        chars = len(self.text.get("1.0", "end-1c"))
        self.status.config(text=f"Строка {line}, Столбец {int(col)+1} | Символов: {chars}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()