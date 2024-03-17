import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Загрузка данных
symbols = pd.read_csv('C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/symbols/symbols.csv', names=['symbol_id', 'name', 'ticker', 'enabled'])
price_data = pd.read_csv('C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/price_data/price_data.csv', names=['id', 'symbol_id', 'source_id', 'timestamp', 'price', 'volume_24_token', 'session_timestamp', 'exported'])

# Объединение данных о ценах с информацией о символах
price_data = price_data.merge(symbols, on='symbol_id')

# Преобразование столбца timestamp в datetime
price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

# Нормализация данных
scaler_price = MinMaxScaler()
scaler_volume = MinMaxScaler()

price_data['price'] = scaler_price.fit_transform(price_data[['price']])
price_data['volume_24_token'] = scaler_volume.fit_transform(price_data[['volume_24_token']])

# Функция для создания последовательностей
def create_sequences(data, N):
    X, y = [], []
    for i in range(len(data) - N):
        X.append(data.iloc[i:(i + N)].drop(['timestamp', 'symbol_id', 'name', 'ticker', 'enabled', 'source_id', 'session_timestamp', 'exported', 'id'], axis=1).values)
        y.append(data.iloc[i + N]['price'])
    return np.array(X), np.array(y)

# Создание последовательностей для каждой криптовалюты
sequences = {}
for ticker in symbols['ticker'].unique():
    ticker_data = price_data[price_data['ticker'] == ticker]
    sequences[ticker] = create_sequences(ticker_data, N=10)  # N - количество шагов в последовательности

# Выбор одной криптовалюты для примера
X_btc, y_btc = sequences['BTC']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_btc, y_btc, test_size=0.2, random_state=42)

# Функция для создания модели
def create_rnn_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(units=64, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(units=32),
        tf.keras.layers.Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Создание модели
input_shape = (X_train.shape[1], X_train.shape[2])
model = create_rnn_model(input_shape)

# Обучение модели
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

# Оценка модели
model.evaluate(X_test, y_test)
