import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
from PIL import Image, ImageTk

class RaTempEdit:
    def __init__(self, root):
        self.root = root
        self.root.title("RaTempEdit")
        self.root.geometry("600x600")
        self.root.minsize(450, 500)
        
        # Настройка сетки для главного окна
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        self.current_file_path = None
        
        # Словарь красивых описаний для отображения в интерфейсе и Windows
        self.ext_descriptions = {
            ".rtmp-text": "RaTemp Standard",
            ".we-can": "Weed Canfing Document",
            ".of-tka": "Offing Tkanat Document",
            ".source": "Office RTMP Document",
            ".of-main": "Office Main Document"
        }
        
        self.extensions = list(self.ext_descriptions.keys())
        
        # Перехват кнопки закрытия окна (крестика) для проверки на сохранение
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # --- ВЕРХНЯЯ ПАНЕЛЬ С КНОПКОЙ ОТКРЫТИЯ ---
        self.top_frame = tk.Frame(root)
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.btn_open = tk.Button(
            self.top_frame, 
            text="[ Открыть файл ]", 
            font=("Arial", 10, "bold"), 
            bg="#2196F3", 
            fg="white", 
            command=self.open_file_dialog
        )
        self.btn_open.pack(side="left", fill="x", expand=True)

        # --- БЛОК 1: CODE EDIT (ВВЕРХУ) ---
        self.label_code = tk.Label(root, text="CodeEdit:", font=("Arial", 11, "bold"))
        self.label_code.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nw")
        
        self.text_frame = tk.Frame(root)
        self.text_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(25, 10), sticky="nsew")
        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)
        
        self.text_code = tk.Text(self.text_frame, font=("Consolas", 11), undo=True, wrap="word")
        self.text_code.grid(row=0, column=0, sticky="nsew")
        
        # Привязка горячих клавиш Ctrl+S для сохранения
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_file())
        
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_code.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_code.config(yscrollcommand=self.scrollbar.set)
        
        # --- НИЖНЯЯ ПАНЕЛЬ ДЛЯ НАСТРОЕК И ИМЕНИ ---
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.bottom_frame.columnconfigure(1, weight=1)
        
        # --- БЛОК 2: ИМЯ (ВНИЗУ) ---
        self.label_name = tk.Label(self.bottom_frame, text="Имя файла:", font=("Arial", 10, "bold"))
        self.label_name.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.entry_name = tk.Entry(self.bottom_frame, font=("Arial", 10))
        self.entry_name.grid(row=0, column=1, pady=5, sticky="ew")
        self.entry_name.insert(0, "temp")
        
        # --- БЛОК 3: РАСШИРЕНИЕ (ВНИЗУ) ---
        self.label_ext = tk.Label(self.bottom_frame, text="Расширение:", font=("Arial", 10, "bold"))
        self.label_ext.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.combo_ext = ttk.Combobox(self.bottom_frame, values=self.extensions, font=("Arial", 10), state="readonly")
        self.combo_ext.grid(row=1, column=1, pady=5, sticky="ew")
        self.combo_ext.current(0)
        self.combo_ext.bind("<<ComboboxSelected>>", self.update_preview_icon)
        
        # Метка для отображения иконки превью
        self.label_icon_preview = tk.Label(self.bottom_frame)
        self.label_icon_preview.grid(row=2, column=1, pady=5, sticky="w")
        
        # --- БЛОК 4: КНОПКА СОХРАНЕНИЯ (В САМОМ НИЗУ) ---
        self.btn_save = tk.Button(
            root, 
            text="{ Сохранить изменения }", 
            font=("Arial", 11, "bold"), 
            bg="#4CAF50", 
            fg="white", 
            command=self.save_file
        )
        self.btn_save.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="ew")

        # Первая инициализация превью иконки
        self.update_preview_icon()
        
        # Автооткрытие при двойном клике в Windows
        if len(sys.argv) > 1:
            file_to_load = sys.argv[1]
            if os.path.exists(file_to_load):
                self.load_file_content(file_to_load)

    def update_preview_icon(self, event=None):
        selected_ext = self.combo_ext.get()
        img_name = f"{selected_ext.replace('.', '')}.png"
        
        # Динамически определяем путь (для корректной работы внутри собранного .exe)
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
            
        img_path = os.path.join(base_path, "icons_files", img_name)
        description = self.ext_descriptions.get(selected_ext, selected_ext)
        
        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path).convert("RGBA")
                pil_img = pil_img.resize((35, 35)) 
                self.current_tk_img = ImageTk.PhotoImage(pil_img)
                
                self.label_icon_preview.config(
                    image=self.current_tk_img, 
                    text=f" Тип: {description}", 
                    compound="left", 
                    font=("Arial", 10, "italic"), 
                    fg="#333333"
                )
            except Exception as e:
                self.label_icon_preview.config(image="", text=f"[ Ошибка: {str(e)[:20]} ]", fg="red")
        else:
            self.label_icon_preview.config(image="", text=f" Тип: {description} (Превью нет)", font=("Arial", 10, "italic"), fg="gray")

    def load_file_content(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            self.text_code.delete("1.0", tk.END)
            self.text_code.insert("1.0", content)
            self.current_file_path = file_path
            
            base_name = os.path.basename(file_path)
            matched_ext = ""
            for ext in self.extensions:
                if base_name.endswith(ext):
                    matched_ext = ext
                    base_name = base_name[:-len(ext)]
                    break
            
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, base_name)
            
            if matched_ext in self.extensions:
                self.combo_ext.set(matched_ext)
                self.update_preview_icon()
                
            self.root.title(f"RaTempEdit - {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{str(e)}")

    def open_file_dialog(self):
        file_types = [("Все форматы RaTempEdit", " ".join([f"*{ext}" for ext in self.extensions]))]
        for ext, desc in self.ext_descriptions.items():
            file_types.append((f"{desc} (*{ext})", f"*{ext}"))
        file_types.append(("Все файлы", "*.*"))
        
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.load_file_content(file_path)

    def save_file(self):
        filename = self.entry_name.get().strip()
        if not filename:
            messagebox.showerror("Ошибка", "Пожалуйста, укажите имя файла!")
            return
            
        selected_ext = self.combo_ext.get()
        
        for ext in self.extensions:
            if filename.endswith(ext):
                filename = filename[:-len(ext)]
                break
        filename += selected_ext
            
        code_content = self.text_code.get("1.0", tk.END)
        initial_dir = os.path.dirname(self.current_file_path) if self.current_file_path else None
        
        desc = self.ext_descriptions.get(selected_ext)
        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile=filename,
            defaultextension=selected_ext,
            filetypes=[(desc, f"*{selected_ext}"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(code_content)
                self.current_file_path = file_path
                self.root.title(f"RaTempEdit - {os.path.basename(file_path)}")
                messagebox.showinfo("Успех", f"Изменения сохранены:\n{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось записать изменения:\n{str(e)}")

    def on_closing(self):
        """Проверка на наличие не сохраненного текста перед выходом"""
        # Если в поле больше 1 символа (стандартный невидимый перенос строки tk.END всегда возвращает 1 символ)
        if len(self.text_code.get("1.0", "end-1c").strip()) > 0:
            if messagebox.askyesno("Выход", "В поле CodeEdit есть текст. Вы уверены, что хотите закрыть программу? Несохраненные изменения будут потеряны."):
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RaTempEdit(root)
    root.mainloop()
