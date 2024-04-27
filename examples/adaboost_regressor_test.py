"https://www.kaggle.com/code/vbmokin/used-cars-price-prediction-by-15-models/input"
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
)

from predikit import Regressor

root = os.path.dirname(os.path.relpath("../predikit"))
sys.path.append(root)

train0 = pd.read_csv("./sample_data/craigslistVehicles.csv")
train0.head(5)

drop_columns = [
    "url",
    "city",
    "city_url",
    "make",
    "title_status",
    "VIN",
    "size",
    "image_url",
    "desc",
    "lat",
    "long",
]
train0 = train0.drop(columns=drop_columns)

train0.info()

train0 = train0.dropna()
train0.head(5)

numerics = ["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
categorical_columns = []
features = train0.columns.values.tolist()
for col in features:
    if train0[col].dtype in numerics:
        continue
    categorical_columns.append(col)
# Encoding categorical features
for col in categorical_columns:
    if col in train0.columns:
        le = LabelEncoder()
        le.fit(list(train0[col].astype(str).values))
        train0[col] = le.transform(list(train0[col].astype(str).values))

train0["year"] = (train0["year"] - 1900).astype(int)
train0["odometer"] = train0["odometer"].astype(int)

train0.head(10)

train0.info()

train0["price"].value_counts()

train0 = train0[train0["price"] > 1000]
train0 = train0[train0["price"] < 40000]
# Rounded ['odometer'] to 5000
train0["odometer"] = train0["odometer"] // 5000
train0 = train0[train0["year"] > 110]
train0.info()

target_name = "price"
train_target0 = train0[target_name]
train0 = train0.drop([target_name], axis=1)
# Synthesis test0 from train0
train0, test0, train_target0, test_target0 = train_test_split(
    train0, train_target0, test_size=0.2, random_state=0
)
# For boosting model
train0b = train0
train_target0b = train_target0
# Synthesis valid as test for selection models
trainb, testb, targetb, target_testb = train_test_split(
    train0b, train_target0b, test_size=valid_part, random_state=0
)
# For models from Sklearn
scaler = StandardScaler()
train0 = pd.DataFrame(scaler.fit_transform(train0), columns=train0.columns)

# Synthesis valid as test for selection models
train, test, target, target_test = train_test_split(
    train0, train_target0, test_size=valid_part, random_state=0
)

train.info()

test.info()

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

# Define the lists to store accuracy values
acc_train_r2 = []
acc_test_r2 = []
acc_train_d = []
acc_test_d = []
acc_train_rmse = []
acc_test_rmse = []


def acc_d(y_meas, y_pred):
    # Relative error between predicted y_pred and measured y_meas values
    return mean_absolute_error(y_meas, y_pred) * len(y_meas) / sum(abs(y_meas))


def acc_rmse(y_meas, y_pred):
    # RMSE between predicted y_pred and measured y_meas values
    return (mean_squared_error(y_meas, y_pred)) ** 0.5


def acc_boosting_model(num, model, train, test, num_iteration=0):
    # Calculation of accuracy of boosting model by different metrics

    global acc_train_r2, acc_test_r2, acc_train_d, acc_test_d, acc_train_rmse, acc_test_rmse

    if num_iteration > 0:
        ytrain = model.predict(train, num_iteration=num_iteration)
        ytest = model.predict(test, num_iteration=num_iteration)
    else:
        ytrain = model.predict(train)
        ytest = model.predict(test)

    print("target = ", targetb[:5].values)
    print("ytrain = ", ytrain[:5])

    acc_train_r2_num = round(r2_score(targetb, ytrain) * 100, 2)
    print("acc(r2_score) for train =", acc_train_r2_num)
    acc_train_r2.insert(num, acc_train_r2_num)

    acc_train_d_num = round(acc_d(targetb, ytrain) * 100, 2)
    print("acc(relative error) for train =", acc_train_d_num)
    acc_train_d.insert(num, acc_train_d_num)

    acc_train_rmse_num = round(acc_rmse(targetb, ytrain) * 100, 2)
    print("acc(rmse) for train =", acc_train_rmse_num)
    acc_train_rmse.insert(num, acc_train_rmse_num)

    print("target_test =", target_testb[:5].values)
    print("ytest =", ytest[:5])

    acc_test_r2_num = round(r2_score(target_testb, ytest) * 100, 2)
    print("acc(r2_score) for test =", acc_test_r2_num)
    acc_test_r2.insert(num, acc_test_r2_num)

    acc_test_d_num = round(acc_d(target_testb, ytest) * 100, 2)
    print("acc(relative error) for test =", acc_test_d_num)
    acc_test_d.insert(num, acc_test_d_num)

    acc_test_rmse_num = round(acc_rmse(target_testb, ytest) * 100, 2)
    print("acc(rmse) for test =", acc_test_rmse_num)
    acc_test_rmse.insert(num, acc_test_rmse_num)


def acc_model(num, model, train, test):
    # Calculation of accuracy of model акщь Sklearn by different metrics

    global acc_train_r2, acc_test_r2, acc_train_d, acc_test_d, acc_train_rmse, acc_test_rmse

    ytrain = model.predict(train)
    ytest = model.predict(test)

    print("target = ", target[:5].values)
    print("ytrain = ", ytrain[:5])

    acc_train_r2_num = round(r2_score(target, ytrain) * 100, 2)
    print("acc(r2_score) for train =", acc_train_r2_num)
    acc_train_r2.insert(num, acc_train_r2_num)

    acc_train_d_num = round(acc_d(target, ytrain) * 100, 2)
    print("acc(relative error) for train =", acc_train_d_num)
    acc_train_d.insert(num, acc_train_d_num)

    acc_train_rmse_num = round(acc_rmse(target, ytrain) * 100, 2)
    print("acc(rmse) for train =", acc_train_rmse_num)
    acc_train_rmse.insert(num, acc_train_rmse_num)

    print("target_test =", target_test[:5].values)
    print("ytest =", ytest[:5])

    acc_test_r2_num = round(r2_score(target_test, ytest) * 100, 2)
    print("acc(r2_score) for test =", acc_test_r2_num)
    acc_test_r2.insert(num, acc_test_r2_num)

    acc_test_d_num = round(acc_d(target_test, ytest) * 100, 2)
    print("acc(relative error) for test =", acc_test_d_num)
    acc_test_d.insert(num, acc_test_d_num)

    acc_test_rmse_num = round(acc_rmse(target_test, ytest) * 100, 2)
    print("acc(rmse) for test =", acc_test_rmse_num)
    acc_test_rmse.insert(num, acc_test_rmse_num)


Ada_Boost = Regressor(strategy="AdaBoostRegressor")
Ada_Boost.fit(train, target)
acc_model(13, Ada_Boost, train, test)
