import datetime
import random
import json
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np


def timeseries_prediction():
    df = []
    ts = []
    values = []
    for i2 in range(100):  # genera dati per 100 rilevazioni
        if i2 == 0:
            value = random.randint(1, 25)  # mm
        elif random.randint(0, 100) > 33:
            value = df[i2-1][1] + random.randint(0, 40)/10
        else:
            value = df[i2-1][1]

        value = round(value, 3)
        date = datetime.datetime.isoformat(datetime.datetime.today())
        df.append([datetime.datetime.fromisoformat(date).timestamp(), value])
        ts.append(i2)
        values.append(value)

    test_values = []
    test_ts = []
    for i2 in range(100):  # genera dati per 100 rilevazioni
        if i2 == 0:
            value = random.randint(1, 25)  # mm
        elif random.randint(0, 100) > 33:
            value = df[i2-1][1] + random.randint(0, 40)/10
        else:
            value = df[i2-1][1]

        value = round(value, 3)
        date = datetime.datetime.isoformat(datetime.datetime.today())
        test_ts.append(i2)
        test_values.append(value)

    def create_sequences(_x, _y, seq_length):
        X, y = [], []
        for i in range(len(_x) - seq_length):
            X.append(_y[i:i + seq_length])
            y.append(_y[i + seq_length])
        return np.array(X), np.array(y)

    seq_length = 12  # Number of time steps to look back
    x_train, y_train = create_sequences(ts, values, seq_length)
    x_test, y_test = create_sequences(test_ts, test_values, seq_length)
    print(y_train)
    print(x_train)

    model = Sequential([
        LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=1)

    # Make predictions
    train_predictions = model.predict(x_train)
    test_predictions = model.predict(x_test)

    # Plot predictions
    plt.figure(figsize=(10, 6))

    # Plot actual data
    plt.plot(values, label='Actual', color='blue')
    plt.plot(test_values, label='Actual Test', color='red')

    # Plot training predictions
    plt.plot(train_predictions, label='Train Predictions',
             color='green')

    # Plot testing predictions
    test_pred_index = range(seq_length + len(train_predictions),
                            seq_length + len(train_predictions) + len(test_predictions))
    plt.plot(test_predictions, label='Test Predictions', color='orange')

    plt.xlabel('ts')
    plt.ylabel('rstd')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    timeseries_prediction()