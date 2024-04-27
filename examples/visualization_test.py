"https://www.kaggle.com/code/mbalvi75/08-knn-diabetes-dataset"
import os
import sys
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

root = os.path.dirname(os.path.relpath("../predikit"))
sys.path.append(root)

# pycharm
#from ..predikit.visualization.visualization import Visualization
#vscode
from predikit.visualization import Visualization

diabetes_data = pd.read_csv("../predikit/examples/sample_data/diabetes.csv")
print(diabetes_data.head(3))

diabetes_data.info(verbose=True)

diabetes_data_copy = diabetes_data.copy(deep=True)
diabetes_data_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = diabetes_data_copy[
    ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']].replace(0, np.NaN)

## showing the count of Nans
print(diabetes_data_copy.isnull().sum())

diabetes_data_copy['Glucose'].fillna(diabetes_data_copy['Glucose'].mean(), inplace=True)
diabetes_data_copy['BloodPressure'].fillna(diabetes_data_copy['BloodPressure'].mean(), inplace=True)
diabetes_data_copy['SkinThickness'].fillna(diabetes_data_copy['SkinThickness'].median(), inplace=True)
diabetes_data_copy['Insulin'].fillna(diabetes_data_copy['Insulin'].median(), inplace=True)
diabetes_data_copy['BMI'].fillna(diabetes_data_copy['BMI'].median(), inplace=True)

count_plot = Visualization(
    params={"data": diabetes_data, 'y': diabetes_data.dtypes,
            }, strategy="countplot")

plot = count_plot.plot()

diabetes_data.plot(kind="")
