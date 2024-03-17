import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import load_model
from joblib import load
# Пути к файлам данных и модели
symbols_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/symbols/symbols.csv'
price_data_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/price_data/price_data.csv'
model_file = 'C:/Users/SergVoid/Projects/Projects/AI Crypto/predict_model.keras'  # Укажите путь к сохраненной модели
scaler_file_path = 'C:/Users/SergVoid/Projects/Projects/AI Crypto/scaler.joblib'
scaler = load(scaler_file_path)
# Загрузка данных
symbols = pd.read_csv(symbols_file, names=['symbol_id', 'name', 'ticker', 'enabled'])
price_data = pd.read_csv(price_data_file, names=['id', 'symbol_id', 'source_id', 'timestamp', 'price', 'volume_24_token', 'session_timestamp', 'exported'])

# Объединение данных и нормализация
price_data = price_data.merge(symbols, on='symbol_id')
price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

# Нормализация данных (Необходимо использовать те же параметры scaler'ов, что и при обучении)
scaler_price = MinMaxScaler()
scaler_volume = MinMaxScaler()
price_data['price'] = scaler_price.fit_transform(price_data[['price']])
price_data['volume_24_token'] = scaler_volume.fit_transform(price_data[['volume_24_token']])

# Функция для создания последовательностей (подобно тому, как было сделано при обучении)
def create_sequences(data, N):
    X = []
    for i in range(len(data) - N):
        X.append(data.iloc[i:(i + N)].drop(['timestamp', 'symbol_id', 'name', 'ticker', 'enabled', 'source_id', 'session_timestamp', 'exported', 'id'], axis=1).values)
    return np.array(X)

# Подготовка последних N записей для каждой криптовалюты
N = 10  # Количество шагов в последовательности, использованных при обучении
ticker_data = price_data[price_data['ticker'] == 'BTC']  # Пример для BTC
last_sequence = create_sequences(ticker_data, N)[-1].reshape((1, N, 2))  # Измените 2 на ваше количество признаков

# Получаем временную метку последней записи в последовательности
last_timestamp = ticker_data.iloc[-1]['timestamp']

# Загрузка модели
model = tf.keras.models.load_model(model_file)

# Выполнение предсказания
predicted_price = model.predict(last_sequence)

# Обратное масштабирование предсказанной цены
predicted_price = scaler_price.inverse_transform(predicted_price)

# Вывод предсказанной цены и времени, к которому она относится
print(f"Предсказанная цена для BTC на момент времени {last_timestamp + pd.Timedelta(minutes=1)}: {predicted_price[0][0]}")
