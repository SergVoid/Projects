import tkinter as tk
from tkinter import messagebox, ttk 
import datetime

# Путь к файлу
file_path = "//store-02-71-by/ISD/VPNUsers.txt"

# Словарь для сопоставления логинов с датами
user_dates = {}

# Глобальная переменная для хранения текущего пользователя
current_user = ""

# Функция для чтения всех пользователей из файла
def read_users_from_file():
    with open(file_path, "r") as file:
        return file.readlines()

# Функция для записи всех пользователей обратно в файл
def write_users_to_file(users):
    with open(file_path, "w") as file:
        file.writelines(users)

# Функция для поиска пользователя и возврата списка логинов
def find_user_expire_date(username):
    matches = []  # Список для хранения совпадений (только логины)
    global user_dates
    user_dates.clear()  # Очищаем предыдущие результаты
    users = read_users_from_file()
    for line in users[1:]:  # Пропускаем заголовок
        parts = line.strip().replace('"', '').split(",")
        if username.lower() in parts[0].lower():
            matches.append(parts[0])  # Добавляем логин
            user_dates[parts[0]] = parts[1]  # Сохраняем дату для логина
            if len(matches) == 3:  # Ограничиваем список тремя совпадениями
                break
    return matches

# Функция вызываемая при выборе логина в Combobox или при поиске
def on_user_select(event=None):
    global current_user
    username = combo_username.get()
    if username in user_dates:
        current_user = username  # Обновляем текущего пользователя
        date = user_dates[username]
        label_date.config(text=f"Дата истечения: {date}")
    else:
        label_date.config(text="Дата истечения: не найдена")

# Функция для прибавления 6 месяцев к дате
def add_six_months(date_str):
    expire_date = datetime.datetime.strptime(date_str, "%Y%m%d")
    new_expire_date = expire_date + datetime.timedelta(days=182)  # Примерно 6 месяцев
    return new_expire_date.strftime("%Y%m%d")

# Функция вызываемая при нажатии на кнопку добавления 6 месяцев
def on_add_six_months():
    global current_user
    if current_user:
        users = read_users_from_file()
        for i, line in enumerate(users):
            parts = line.strip().replace('"', '').split(",")
            if current_user.lower() == parts[0].lower():
                new_expire_date = add_six_months(parts[1])
                users[i] = f'"{parts[0]}","{new_expire_date}"\n'  # Обновляем строку
                write_users_to_file(users)  # Перезаписываем файл
                label_result.config(text=f"Новая дата истечения для {current_user}: {new_expire_date}")
                combo_username.set('')
                current_user = ""
                label_date.config(text="Дата истечения: ")
                return
        messagebox.showinfo("Ошибка", "Пользователь не найден для обновления.")
    else:
        messagebox.showinfo("Результат", "Сначала найдите пользователя.")

# Функция вызываемая при нажатии на кнопку поиска
def on_search(event=None):  # Добавляем event=None для обработки событий
    username = combo_username.get()
    matches = find_user_expire_date(username)
    if matches:
        combo_username['values'] = matches  # Обновляем значения в Combobox
        combo_username.set(matches[0])  # Устанавливаем первое совпадение
    else:
        messagebox.showinfo("Результат", "Совпадения не найдены.")

# Создание графического интерфейса
root = tk.Tk()
root.title("VPN Expire Date Manager")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Логин пользователя:").grid(row=0, column=0, padx=5, pady=5)

combo_username = ttk.Combobox(frame)
combo_username.grid(row=0, column=1, padx=5, pady=5)
combo_username.bind('<Return>', on_search)  # Поиск при нажатии Enter
combo_username.bind('<<ComboboxSelected>>', on_user_select)  # Обработка выбора из списка

search_button = tk.Button(frame, text="Найти", command=on_search)
search_button.grid(row=0, column=2, padx=5, pady=5)

label_date = tk.Label(root, text="Дата истечения: ", justify=tk.LEFT)
label_date.pack(padx=10, pady=5)

# Исправляем вызов функции на on_add_six_months для кнопки "Добавить 6 месяцев"
tk.Button(root, text="Добавить 6 месяцев", command=on_add_six_months).pack()

label_result = tk.Label(root, text="", justify=tk.LEFT)
label_result.pack()

root.mainloop()