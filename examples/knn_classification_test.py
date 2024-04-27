"https://www.kaggle.com/code/mbalvi75/08-knn-diabetes-dataset"
import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


root = os.path.dirname(os.path.relpath("../predikit"))
sys.path.append(root)

from predikit import Classifier

df = pd.read_csv("../predikit/examples/sample_data/diabetes.csv")
print(df.head(3))


knn = Classifier(
    params={"n_neighbors": 5, "p": 2, "metric": "euclidean"},
    strategy="KNeighborsClassifier",
)


w = 5
df.hist(
    bins=10, figsize=(20, 15), color="green", alpha=0.6, hatch="X", rwidth=w
)

X = df.iloc[:, 0:8]
y = df.iloc[:, 8]

xtr, xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=4)

sc = StandardScaler()

xtr = sc.fit_transform(xtr)
xte = sc.fit_transform(xte)

knn.fit(xtr, ytr)
pred = knn.predict(xte)
print("prediction: ", pred)
print("-----------------------------------------------------")
pred_probability = knn.predict_proba(xte)
print("prediction probability: ", pred_probability)
print("-----------------------------------------------------")
pred_log_probability = knn.predict_log_proba(xte)
print("prediction log probability: ", pred_log_probability)
print("-----------------------------------------------------")
score = knn.score(xte, yte)
print("Accuracy:", score)
print("-----------------------------------------------------")
print(accuracy_score(pred, yte))
print("-----------------------------------------------------")
print(confusion_matrix(pred, yte))
