import os
from datetime import datetime
from database_manager import create_connection  # Импорт функции создания соединения

tables = ['symbols', 'sources', 'price_data']  # Список таблиц для экспорта
output_folder = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/'  # Путь к папке для сохранения файлов

def export_table_to_csv(table_name, output_folder, only_new=False):
    """
    Экспортирует данные из указанной таблицы в CSV файл.
    """
    if table_name in ['symbols', 'sources']:
        file_name = f"{table_name}.csv"  # Файлы для symbols и sources без временной метки
        file_path = os.path.join(output_folder, table_name, file_name).replace('\\', '/')
    elif table_name == 'price_data' and only_new:
        file_name = f"{table_name}.csv"  # Файл для price_data с новыми записями
        file_path = os.path.join(output_folder, table_name, file_name).replace('\\', '/')
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Для других случаев используем временную метку
        file_name = f"{table_name}_{timestamp}.csv"
        file_path = os.path.join(output_folder, table_name, file_name).replace('\\', '/')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создаем папку, если она не существует

    # Удаляем существующий файл, чтобы избежать ошибки "File already exists"
    if os.path.exists(file_path):
        os.remove(file_path)

    # SQL запрос для экспорта данных
    query = f"""
    SELECT * INTO OUTFILE '{file_path}'
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
    FROM {table_name};
    """

    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            print(f"Таблица '{table_name}' успешно экспортирована в файл: {file_path}")
    except Exception as error:
        print(f"Ошибка при экспорте таблицы '{table_name}': {error}")
    finally:
        if connection.is_connected():
            connection.close()

for table in tables:
    only_new = table == 'price_data'  # Используем параметр only_new=True только для price_data
    export_table_to_csv(table, output_folder, only_new=only_new)