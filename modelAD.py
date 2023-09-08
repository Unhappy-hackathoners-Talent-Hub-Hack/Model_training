#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from keras import layers
from keras import models
from sklearn.preprocessing import MinMaxScaler


scaler = MinMaxScaler()

table = pd.read_excel('combinations2.xlsx')

table.drop(table.columns[14:], axis=1, inplace=True)
data_left = table.drop(table.columns[10:], axis=1)
data_right = table.drop(table.columns[:11], axis=1)

test_data_left = data_left.iloc[::10]
test_data_right = data_right.iloc[::10]
data_left = data_left.drop(data_left.index[::10])
data_right = data_right.drop(data_right.index[::10])

input_size = len(data_left.columns)
output_size = len(data_right.columns)

data_left = data_left.to_numpy()
data_right = data_right.to_numpy()
test_data_left = test_data_left.to_numpy()
test_data_right = test_data_right.to_numpy()

data_left = scaler.fit_transform(data_left)
test_data_left = scaler.fit_transform(test_data_left)

model = models.Sequential()
model.add(layers.Dense(64, 
                       input_dim=input_size,
                       activation='relu'))
model.add(layers.Dense(32,
                       activation='relu'))
model.add(layers.Dense(output_size))

model.compile(loss='mean_squared_error',
              optimizer='adam')

num_epochs = 10
batch_size = 16

history = model.fit(data_left,
                    data_right,
                    epochs=num_epochs,
                    batch_size=batch_size,
                    verbose=1)

model.save('popitkaAD3.h5')

test_loss = model.evaluate(test_data_left, test_data_right)
print(f'Test Loss: {test_loss}')

predictions = model.predict(test_data_left)

test0 = []
test1 = []
test2 = []
pred0 = []
pred1 = []
pred2 = []

for i in range(len(test_data_left)):
    test0.append(test_data_right[i][0])
    test1.append(test_data_right[i][1])
    test2.append(test_data_right[i][2])    
    pred0.append(predictions[i][0])
    pred1.append(predictions[i][1])
    pred2.append(predictions[i][2])
        
plt.figure(figsize=(10, 5))
plt.scatter(test_data_right, predictions, c='blue', marker='o', label='Predictions')  # Маркеры для предсказаний
plt.plot(test_data_right, test_data_right, c='red', linestyle='-', label='True Values')  # Прямая для истинных значений
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.legend()
plt.show()
