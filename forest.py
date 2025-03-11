from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split


data = pd.read_csv("MLdata.csv") #18 col
trainData=data.drop(columns=['Listing id', 'Item name', 'Icon url']) #15 col
trainData.replace({"False":0,"True":1},inplace=True)
    

X = trainData.drop(columns="target") #14 col
y = trainData["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=11, random_state=42)
model.fit(X_train, y_train)

# save
joblib.dump(model, "./random_forest.joblib")


