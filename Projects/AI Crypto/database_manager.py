import mysql.connector

# Функции создания соединения, добавления символов и источников остаются без изменений

def set_symbol_status(symbol, status):
    """Обновляет статус активности для символа."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE symbols SET enabled = %s WHERE ticker = %s"
    cursor.execute(query, (status, symbol,))
    connection.commit()
    cursor.close()
    connection.close()

def set_source_status(name, status):
    """Обновляет статус активности для источника."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE sources SET enabled = %s WHERE name = %s"
    cursor.execute(query, (status, name,))
    connection.commit()
    cursor.close()
    connection.close()

def get_active_symbols():
    """Возвращает список активных символов."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT ticker FROM symbols WHERE enabled = TRUE"
    cursor.execute(query)
    symbols = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return symbols

def get_active_sources():
    """Возвращает список активных источников."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT name FROM sources WHERE enabled = TRUE"
    cursor.execute(query)
    sources = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return sources

import mysql.connector
from DB import host, user, passwd, database

def create_connection():
    """Создает соединение с базой данных."""
    return mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )



def add_symbol(symbol, name):
    """Добавляет новую криптовалюту в таблицу symbols с проверкой на дубликаты."""
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM symbols WHERE ticker = %s", (symbol,))
            if cursor.fetchone()[0] > 0:
                print(f"Символ {symbol} уже существует.")
                return
            cursor.execute("INSERT INTO symbols (ticker, name) VALUES (%s, %s)", (symbol, name))
            connection.commit()
            print(f"Криптовалюта {name} добавлена.")
    except mysql.connector.Error as error:
        print(f"Ошибка при добавлении символа {symbol}: {error}")
    finally:
        connection.close()


def add_source(name, api_url=None, api_key=None, enabled=True):
    """Добавляет новый источник данных в таблицу sources или обновляет существующий."""
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Проверяем, существует ли уже источник с таким именем
            cursor.execute("SELECT COUNT(*) FROM sources WHERE name = %s", (name,))
            if cursor.fetchone()[0] > 0:
                # Если источник существует, обновляем его данные
                update_query = """
                    UPDATE sources
                    SET api_url = %s, api_key = %s, enabled = %s
                    WHERE name = %s
                """
                cursor.execute(update_query, (api_url, api_key, enabled, name))
                print(f"Информация для источника {name} обновлена.")
            else:
                # Если источник не существует, добавляем его как новую запись
                insert_query = """
                    INSERT INTO sources (name, api_url, api_key, enabled)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, api_url, api_key, enabled))
                print(f"Источник данных {name} добавлен.")
            connection.commit()
    except mysql.connector.Error as error:
        print(f"Ошибка при работе с источником {name}: {error}")
    finally:
        connection.close()

def view_symbols():
    """Отображает список всех криптовалют."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM symbols"
    cursor.execute(query)
    symbols = cursor.fetchall()
    for symbol in symbols:
        print(symbol)
    cursor.close()
    connection.close()

def view_sources():
    """Отображает список всех источников данных."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM sources"
    cursor.execute(query)
    sources = cursor.fetchall()
    for source in sources:
        print(source)
    cursor.close()
    connection.close()

def add_price_data(symbol_id, source_id, price, volume=None):
    """Добавляет данные о цене в таблицу price_data."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO price_data (symbol_id, source_id, price, volume) VALUES (%s, %s, %s, %s)"
    values = (symbol_id, source_id, price, volume)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    print("Цена успешно добавлена в базу данных.")
def get_symbol_id(ticker):
    """Возвращает идентификатор символа по его тикеру."""
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT symbol_id FROM symbols WHERE ticker = %s"
    cursor.execute(query, (ticker,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    else:
        return None
    
def get_source_id(source_name):
    connection = create_connection()
    try:
        with connection.cursor(buffered=True) as cursor:
            query = "SELECT source_id FROM sources WHERE name = %s"
            cursor.execute(query, (source_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
    finally:
        connection.close()
    return None

def get_price_data():
    """Извлекает данные о ценах для последнего запроса."""
    connection = create_connection()
    cursor = connection.cursor()
    query = """
    SELECT symbols.ticker, sources.name, price_data.price, price_data.volume, price_data.timestamp
    FROM price_data
    JOIN symbols ON price_data.symbol_id = symbols.symbol_id
    JOIN sources ON price_data.source_id = sources.source_id
    WHERE price_data.timestamp = (SELECT MAX(timestamp) FROM price_data)
    ORDER BY sources.name, symbols.ticker
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def get_api_key(source_name):
    """Возвращает ключ API для указанного источника."""
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT api_key FROM sources WHERE name = %s"
            cursor.execute(query, (source_name,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Возвращает первый элемент кортежа, который должен быть api_key
    except mysql.connector.Error as error:
        print(f"Ошибка при получении API ключа для {source_name}: {error}")
    finally:
        if connection.is_connected():
            connection.close()
    return None
