import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Input, LSTMV1, Dense
from tensorflow.python.keras.models import Sequential, save_model

# Загрузка данных
symbols_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/symbols/symbols.csv'
price_data_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/price_data/price_data.csv'

symbols = pd.read_csv(symbols_file, names=['symbol_id', 'name', 'ticker', 'enabled'])
price_data = pd.read_csv(price_data_file, names=['id', 'symbol_id', 'source_id', 'timestamp', 'price', 'volume_24_token', 'session_timestamp', 'exported'])

# Объединение данных о ценах с информацией о символах
price_data = price_data.merge(symbols, on='symbol_id')
price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

# Нормализация данных
scaler = MinMaxScaler(feature_range=(0, 1))
price_data[['price', 'volume_24_token']] = scaler.fit_transform(price_data[['price', 'volume_24_token']])

# Функция для создания последовательностей
def create_sequences(df, sequence_length):
    X, y = [], []
    for i in range(len(df) - sequence_length):
        X.append(df[['price', 'volume_24_token']].iloc[i:i + sequence_length].values)
        y.append(df['price'].iloc[i + sequence_length])
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



early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Функция для создания модели с дополнительными слоями и Dropout
def create_rnn_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.LSTM(units=64, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.LSTM(units=32),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(units=1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Создание модели
input_shape = (X_train.shape[1], X_train.shape[2])
model = create_rnn_model(input_shape)

# Обучение модели с EarlyStopping
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, callbacks=[early_stopping])

# Оценка модели
model.evaluate(X_test, y_test)

model.save('C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/predict.keras')