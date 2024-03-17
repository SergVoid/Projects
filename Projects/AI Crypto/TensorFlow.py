import tensorflow as tf

# Функция для создания модели
def create_rnn_model(input_shape):
    model = tf.keras.Sequential([
        # Добавление слоев LSTM
        tf.keras.layers.LSTM(units=64, return_sequences=True, input_shape=input_shape),
        # Добавление выходного слоя с одним нейроном (для предсказания цены)
        tf.keras.layers.Dense(units=1)
    ])
    # Компиляция модели
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Создание экземпляра модели
input_shape = (None, num_features)  # num_features - количество признаков во входных данных
model = create_rnn_model(input_shape)
