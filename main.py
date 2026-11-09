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
        edit_menu.add_separator()
        edit_menu.add_command(label="Найти и заменить... Ctrl+F", command=self.open_find_window)
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
        self.root.bind_all("<Control-f>", lambda e: self.open_find_window())

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

    def open_find_window(self):
        win = tk.Toplevel(self.root)
        win.title("Поиск и замена")
        win.geometry("380x160")
        win.transient(self.root)

        tk.Label(win, text="Найти:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        find_entry = tk.Entry(win, width=30)
        find_entry.grid(row=0, column=1, padx=6, pady=6)
        find_entry.focus()

        tk.Label(win, text="Заменить на:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        repl_entry = tk.Entry(win, width=30)
        repl_entry.grid(row=1, column=1, padx=6, pady=6)

        def find_next():
            self.text.tag_remove("match", "1.0", tk.END)
            query = find_entry.get()
            if not query:
                return
            start = self.text.index(tk.INSERT)
            idx = self.text.search(query, start, stopindex=tk.END, nocase=True)
            if not idx:
                idx = self.text.search(query, "1.0", stopindex=tk.END, nocase=True)
            if idx:
                end = f"{idx}+{len(query)}c"
                self.text.tag_add("match", idx, end)
                self.text.tag_config("match", background="#ffcc00", foreground="#000000")
                self.text.mark_set(tk.INSERT, end)
                self.text.see(idx)
            else:
                messagebox.showinfo("Поиск", "Совпадений не найдено.")

        def replace_one():
            query = find_entry.get()
            if not query:
                return
            try:
                sel_start = self.text.index("sel.first")
                sel_end = self.text.index("sel.last")
            except tk.TclError:
                find_next()
                return
            if self.text.get(sel_start, sel_end).lower() == query.lower():
                self.text.delete(sel_start, sel_end)
                self.text.insert(sel_start, repl_entry.get())
            find_next()

        def replace_all():
            query = find_entry.get()
            if not query:
                return
            content = self.text.get("1.0", tk.END)
            count = content.lower().count(query.lower())
            if count == 0:
                messagebox.showinfo("Поиск", "Совпадений не найдено.")
                return
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", content.replace(query, repl_entry.get()))
            messagebox.showinfo("Поиск", f"Заменено вхождений: {count}")

        btn_frame = tk.Frame(win)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Найти далее", command=find_next).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Заменить", command=replace_one).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Заменить всё", command=replace_all).pack(side=tk.LEFT, padx=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()