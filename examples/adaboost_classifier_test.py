'https://www.kaggle.com/code/prashant111/adaboost-classifier-tutorial'
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score

root = os.path.dirname(os.path.relpath("../predikit"))
sys.path.append(root)

from predikit import Classifier

iris=pd.read_csv("../predikit/examples/sample_data/Iris.csv")
iris.head()
iris.info()

X = iris[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]

X.head()

y = iris['Species']

y.head()

from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()

y=le.fit_transform(y)

# Import train_test_split function
from sklearn.model_selection import train_test_split

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Import the AdaBoost classifier
from predikit import Classifier


# Create adaboost classifer object
abc = Classifier(params={'n_estimators': 50, 'learning_rate' : 1, 'random_state' : 0}, strategy='AdaBoostClassifier')

# Train Adaboost Classifer
model1 = abc.fit(X_train, y_train)


#Predict the response for test dataset
y_pred = model1.predict(X_test)


print("AdaBoost Classifier Model Accuracy:", accuracy_score(y_test, y_pred))

# load required classifer
from predikit import Classifier

# import Support Vector Classifier
from sklearn.svm import SVC

# create SVC object
svc = SVC(probability=True, kernel='linear')

# create adaboost classifer object with SVC as the base estimator
abc = Classifier(params={'n_estimators': 50, 'learning_rate' : 1, 'random_state' : 0, 'estimator' : svc}, strategy='AdaBoostClassifier')

# train adaboost classifer
model2 = abc.fit(X_train, y_train)

# predict the response for test dataset
y_pred = model2.predict(X_test)

# calculate and print model accuracy
print("Model Accuracy with SVC Base Estimator:", accuracy_score(y_test, y_pred))
