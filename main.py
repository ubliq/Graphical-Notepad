import tkinter as tk


class NotepadApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Graphical Notepad")
        self.root.geometry("900x600")
        self.root.minsize(600, 400)

        self._build_menu()
        self._build_editor()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новый")
        file_menu.add_command(label="Открыть...")
        file_menu.add_command(label="Сохранить")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()