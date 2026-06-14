import os
import glob
import shutil
import requests
import random
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Прямая ссылка без склеек и переменных
RAW_URL = "https://githubusercontent.com"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def get_roblox_cursor_path():
    user_profile = os.environ.get("USERPROFILE")
    base_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "Versions", "version-*", "content", "textures", "Cursors", "KeyboardMouse")
    found_paths = glob.glob(base_path)
    return found_paths if found_paths else None

def load_cursors_from_github():
    url = f"{RAW_URL}/list.txt?nocache={random.randint(1, 10000)}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            lines = [line.strip() for line in response.text.split("\n") if line.strip()]
            return lines
        else:
            messagebox.showerror("Ошибка сервера", f"GitHub вернул код: {response.status_code}\nСсылка: {url}")
    except Exception as e:
        messagebox.showerror("Ошибка соединения", f"Текущая ссылка: {url}\n\nОшибка:\n{e}")
    return []

def apply_selected_cursor():
    selected_name = cursor_combobox.get()
    if not selected_name or selected_name in ["Загрузка...", "Ошибка чтения"]:
        messagebox.showwarning("Внимание", "Сначала выберите курсор из списка!")
        return

    roblox_dir = get_roblox_cursor_path()
    if not roblox_dir:
        messagebox.showerror("Ошибка", "Папка Roblox не найдена!")
        return

    try:
        cache_buster = f"?nocache={random.randint(1, 10000)}"
        img_url = f"{RAW_URL}/{selected_name}{cache_buster}"
        img_response = requests.get(img_url, timeout=5)
        if img_response.status_code == 200:
            target_files = ["ArrowCursor.png", "ArrowFarCursor.png"]
            for filename in target_files:
                destination = os.path.join(roblox_dir, filename)
                with open(destination, "wb") as f:
                    f.write(img_response.content)
            
            messagebox.showinfo("Успех!", f"Курсор успешно установлен!")
        else:
            messagebox.showerror("Ошибка", f"Файл {selected_name} не найден на GitHub.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def refresh_list():
    cursor_combobox.configure(values=["Загрузка..."])
    cursor_combobox.set("Загрузка...")
    app.update()
    
    cursors = load_cursors_from_github()
    if cursors:
        cursor_combobox.configure(values=cursors)
        cursor_combobox.set(cursors[0])  # Выбираем первый курсор из списка
    else:
        cursor_combobox.configure(values=["Ошибка чтения"])
        cursor_combobox.set("Ошибка чтения")

app = ctk.CTk()
app.title("Roblox Cloud Cursor v3.0")
app.geometry("400x240")
app.resizable(False, False)

title_label = ctk.CTkLabel(app, text="Облачный Сменщик Курсоров", font=ctk.CTkFont(family="Arial", size=18, weight="bold"))
title_label.pack(pady=(20, 5))

desc_label = ctk.CTkLabel(app, text="Выбирайте курсоры, обновляемые через GitHub", font=ctk.CTkFont(family="Arial", size=12), text_color="gray")
desc_label.pack(pady=(0, 20))

cursor_combobox = ctk.CTkComboBox(app, width=250, values=["Загрузка..."])
cursor_combobox.set("Загрузка...")
cursor_combobox.pack(pady=10)

btn_apply = ctk.CTkButton(app, text="Установить этот курсор", width=250, height=40, corner_radius=8, font=ctk.CTkFont(weight="bold"), command=apply_selected_cursor)
btn_apply.pack(pady=5)

btn_refresh = ctk.CTkButton(app, text="🔄 Обновить список", width=120, height=30, fg_color="transparent", border_width=1, text_color="white", command=refresh_list)
btn_refresh.pack(pady=(10, 0))

app.after(100, refresh_list)
app.mainloop()
