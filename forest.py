from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
import tensorflow as tf
from tensorflow.keras.initializers import RandomNormal
import numpy as np

data = pd.read_csv("NewerMLdata.csv",dtype={'wear_name': str}) #18 col

trainData=data.drop(columns=['Listing id', 'Lowest calculated price','Sale price','Item name', 'Icon url']) #15 col
trainData.replace({"False":0,"True":1},inplace=True)

encoder = OneHotEncoder(sparse_output=False,handle_unknown="ignore").set_output(transform='pandas')
encoded_data = encoder.fit_transform(trainData[['wear_name']])
finished_encoded_data = pd.concat([trainData,encoded_data],axis=1).drop(columns="wear_name")
minority = finished_encoded_data[finished_encoded_data["target"]==1]
#print("total rows where target=1:",minority.shape[0])
oversampled_data = pd.concat([finished_encoded_data]+[minority]*4,ignore_index=True)



y = oversampled_data["target"]
#print("Target value count: ",y.value_counts())
X = oversampled_data.drop(columns="target") #14 col
#print(X.columns)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=30, random_state=42,max_depth=5)
model.fit(X_train, y_train)

print(model.score(X_test,y_test))

# save
joblib.dump(model, "./random_forest.joblib")



