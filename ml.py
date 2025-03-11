import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.initializers import RandomNormal

#Should have alot more data before using this

data = pd.read_csv("MLdata.csv") #18 col
trainData=data.drop(columns=['Listing id', 'Item name', 'Icon url']) #15 col
trainData.replace({"False":0,"True":1},inplace=True)
    

X = trainData.drop(columns="target") #14 col
y = trainData["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

X_val = X_test[:31]
X_test = X_test[31:]
y_val = y_test[:31]
y_test = y_test[31:]

tf.random.set_seed(42)
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(shape=(14,)),  
    tf.keras.layers.Dense(16, activation='relu', kernel_initializer=RandomNormal(seed=42),name='layer_1'),
    tf.keras.layers.Dense(32, activation='relu', kernel_initializer=RandomNormal(seed=42),name='layer_2'),
    tf.keras.layers.Dense(16, activation='relu', kernel_initializer=RandomNormal(seed=42),name='layer_3'),
    tf.keras.layers.Dense(8, activation='relu', kernel_initializer=RandomNormal(seed=42),name='layer_4'),
    tf.keras.layers.Dense(1, activation='sigmoid', kernel_initializer=RandomNormal(seed=42),name='output_layer')
])

model.compile(loss='binary_crossentropy', optimizer="AdamW", metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, validation_data=(X_val, y_val))


def accuracy(y,y_pred):
    return np.mean(y==y_pred)


prediction = model.predict(X_test)
binary_prediction = ((prediction>=0.5).astype(int)).reshape(-1)
print(binary_prediction.shape)
print(y_test.shape)
print(accuracy(y_test,binary_prediction))

results = model.evaluate(X_test,y_test)
print("Test loss model1:" ,results[0])


