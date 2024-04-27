"https://www.kaggle.com/code/akshat0007/applying-knn-for-regression-on-zomato-dataset/notebook"
from cmath import sqrt
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    mean_squared_error,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

root = os.path.dirname(os.path.relpath("../predikit"))
sys.path.append(root)

from predikit import Regressor

df = pd.read_csv(
    "../predikit/examples/sample_data/zomato.csv", encoding="ISO-8859-1"
)
country = pd.read_excel("../predikit/examples/sample_data/Country-Code.xlsx")
df = pd.merge(df, country, on="Country Code")
df.head()
df1 = df.groupby(["Cuisines"])
df1.mean()
df2 = df.groupby(["City"])
df2.mean()
df3 = df["City"].value_counts()

data_country = df.groupby(["Country"], as_index=False).count()[
    ["Country", "Restaurant ID"]
]
data_country.head()
data_country.columns = ["Country", "No of Restaurant"]
plt.figure(figsize=(20, 30))
plt.bar(
    data_country["Country"], data_country["No of Restaurant"], color="brown"
)
plt.xlabel("Country")
plt.ylabel("No of Restaurant")
plt.title("No of Restaurant")
plt.xticks(rotation=60)

sns.barplot(x="Cuisines", y="Number of Resturants", data=Top10)
plt.xlabel("Cuisines", fontsize=20)
plt.ylabel("Number of Resturants", fontsize=20)
plt.title("Top 10 Cuisines on Zomato", fontsize=30)
plt.show()

dummy_cuisines = pd.get_dummies(df["Has Online delivery"])
df4 = dummy_cuisines.sum()
DataFrame(df4)
x = ["Yes", "No"]
plt.bar(x, df4, color="red")
plt.xlabel("Wether the restaurant has an Online delivery")
plt.ylabel("Count of restaurants")

df.corr()
corrmat = df.corr()

f, ax = plt.subplots(figsize=(9, 8))
sns.heatmap(corrmat, ax=ax, cmap="YlGnBu", linewidths=0.1)

x = df[["Currency"]]
y = df["Average Cost for two"]
x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, random_state=42
)
dummies = pd.get_dummies(x_train)
dummies
dummies2 = pd.get_dummies(x_test)
dummies2.head()
k = []
accu = []
model = Regressor(params={"n_neighbors": 5}, strategy="KNeighborsRegressor")
model.fit(dummies, y_train)  # fit the model

k = []
accu = []
for i in range(1, 50):
    model = Regressor(
        params={"n_neighbors": i}, strategy="KNeighborsRegressor"
    )
    model.fit(dummies, y_train)  # fit the model
    pred = model.predict(dummies2)  # make prediction on test set
    a = dummies2.shape
    accuracy = r2_score(y_test, pred)
    print("For k=", i)
    print("Accuracy is -", accuracy * 100, "%")
    k.append(i)
    accu.append(accuracy)

plt.plot(k, accu)
plt.xlabel("Value of K")
plt.ylabel("R2_score")

model = Regressor(params={"n_neighbors": 13}, strategy="KNeighborsRegressor")
model.fit(dummies, y_train)  # fit the model
pred = model.predict(dummies2)  # make prediction on test set
a = dummies2.shape
accuracy = r2_score(y_test, pred)
for i in range(a[0]):
    print("For ", x_test.iloc[i, :])
    print("average cost for two=")
    print(pred[i])

accuracy = r2_score(y_test, pred)
print("For K=", 2)
print("Accuracy is a-", accuracy * 100, "%")

# Linear Regression
x = df[["Currency", "Rating text"]]
y = df["Average Cost for two"]
x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, random_state=42
)
dummies = pd.get_dummies(x_train)
dummies
dummies2 = pd.get_dummies(x_test)
dummies2.head()
linear_model = Regressor(strategy="LinearRegression")
linear_model.fit(dummies, y_train)

prediction = linear_model.predict(dummies2)
r2_score(prediction, y_test)

error = sqrt(mean_squared_error(y_test, prediction))
error
