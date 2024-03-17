import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from keras.layers import LSTM, Dropout, Dense
from keras.models import Sequential
from joblib import dump, load

# Загрузка и предварительная обработка данных
def load_and_preprocess_data():
    symbols_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/symbols/symbols.csv'
    price_data_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/price_data/price_data.csv'
    sources_file = 'C:/ProgramData/MySQL/MySQL Server 8.3/Uploads/sources/sources.csv'

    symbols = pd.read_csv(symbols_file, names=['symbol_id', 'name', 'ticker', 'enabled'], header=None)
    price_data = pd.read_csv(price_data_file, names=['id', 'symbol_id', 'source_id', 'timestamp', 'price', 'volume_24_token', 'session_timestamp', 'exported'], header=None)
    sources = pd.read_csv(sources_file, names=['source_id', 'name', 'api_url', 'api_key', 'enabled'], header=None)

    price_data = price_data.merge(symbols, on='symbol_id').merge(sources, on='source_id')
    price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])

    # Нормализация данных
    scaler = MinMaxScaler(feature_range=(0, 1))
    price_data[['price', 'volume_24_token']] = scaler.fit_transform(price_data[['price', 'volume_24_token']])

    return price_data, scaler

# Создание последовательностей
def create_sequences(data, sequence_length=10):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        sequence = data[['price', 'volume_24_token']].iloc[i:i + sequence_length].values
        X.append(sequence)
        y.append(data['price'].iloc[i + sequence_length])
    return np.array(X), np.array(y)

# Обучение модели
def train_model(X_train, y_train):
    input_shape = (X_train.shape[1], X_train.shape[2])

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    
    return model

if __name__ == "__main__":
    price_data, scaler = load_and_preprocess_data()
    
    # Подготовка данных для обучения
    sequence_length = 10
    X, y = create_sequences(price_data, sequence_length)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Обучение и оценка модели
    model = train_model(X_train, y_train)
    model.evaluate(X_test, y_test)

    # Сохранение модели и scaler'а
    model.save('C:/Users/SergVoid/Projects/Projects/AI Crypto/predict_model.keras')
    # Сохраните scaler с использованием joblib или pickle для последующего использования в predict.py
    scaler_file_path = 'C:/Users/SergVoid/Projects/Projects/AI Crypto/scaler.joblib'
    dump(scaler, scaler_file_path)