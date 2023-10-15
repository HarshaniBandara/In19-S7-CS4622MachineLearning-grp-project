# -*- coding: utf-8 -*-
"""layer-8-label-4-190088H.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F13B2rjjwkWJbG8oahIMbrFy2nE7lKrV
"""

!python3 -m pip install -U matplotlib
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sklearn as sk
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, KFold

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

def train_and_evaluate_models(X_train, y_train, X_val, y_val,test_x):
    """
    Train and evaluate multiple classification models on the given data.

    Parameters:
    - X_train: Training features
    - y_train: Training labels
    - X_val: Validation features
    - y_val: Validation labels

    Returns:
    - A dictionary containing model names as keys and their accuracies on the validation data as values.
    """

    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='linear', C=1.0, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB(),
        'Decision Tree': DecisionTreeClassifier(random_state=42)
    }

    accuracies = {}
    pred={}

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        y_pred_test=model.predict(test_x)
        accuracy = accuracy_score(y_val, y_pred)
        accuracies[model_name] = accuracy
        pred[model_name]=y_pred_test
    print(accuracies)
    return accuracies,pred

def cross_validation(x_train,y_train,x_valid,y_valid):
    classifiers = [
    ("Random Forest", RandomForestClassifier()),
    ('Logistic Regression',LogisticRegression(max_iter=1000, random_state=42)),
    ("K-Nearest Neighbors", KNeighborsClassifier(n_neighbors=5)),
    ("SVM", SVC(kernel="linear"))]



    for model_name, model in classifiers:
        cross_val_scores = cross_val_score(model, x_train, y_train, cv=5)
        print(f"{model_name} Cross-validation scores:", cross_val_scores)
        print(f"{model_name} Mean accuracy:", cross_val_scores.mean())
        print(f"{model_name} Standard deviation:", cross_val_scores.std())
        print("\n")

#function for knn model using and check accuarcy

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
def knn(train_x,train_y,valid_x,valid_y):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(train_x, train_y)
    y_pred = model.predict(valid_x)
    accuracy = accuracy_score(valid_y, y_pred)
    print(f'Accuracy using knn: {accuracy:.2f}')

#function for data preprocessing
from sklearn.preprocessing import StandardScaler
def preprocessing(label):
    train=pd.read_csv("train.csv")
    test=pd.read_csv("test.csv")
    valid=pd.read_csv("valid.csv")
    train_x_label_1=train.iloc[:, :-4]
    train_y_label_1=train.iloc[:,-5+label]

    valid_x_label_1=train.iloc[:, :-4]
    train_y_label_1=train.iloc[:,-5+label]

    test_x_label_1=train.iloc[:, 1:]

    ss = StandardScaler()
    scaled_train_x_label = ss.fit_transform(train_x_label_1)
    scaled_train_x_label
    scaled_test_x_label=ss.fit_transform(test_x_label_1)
    scaled_valid_x_label=ss.fit_transform(valid_x_label_1)
    return scaled_train_x_label,scaled_valid_x_label

# scaling function
from sklearn.preprocessing import StandardScaler
def scale(train_x,valid_x,test_x):
    ss = StandardScaler()
    scaled_train_x_label = ss.fit_transform(train_x)
    scaled_train_x_label
    scaled_test_x_label=ss.fit_transform(test_x)
    scaled_valid_x_label=ss.fit_transform(valid_x)
    return scaled_train_x_label,scaled_valid_x_label

# pca approch
from sklearn.decomposition import PCA
def pca(train_x,train_y,valid_x,valid_y,test_x):
    pca=PCA(.95, svd_solver='full')
    pca=pca.fit(train_x)
    train_features_pca=pca.transform(train_x)
    valid_features_pca=pca.transform(valid_x)
    test_features_pca=pca.transform(test_x)
    print("accuarcy after pca")
    #     knn(train_features_pca,train_y,valid_features_pca,valid_y)
    return train_features_pca,valid_features_pca,test_features_pca

# Write predicted values to a CSV file.
import pandas as pd

def write_predictions_to_csv(predictions, output_file):


    # Create a DataFrame with a column for predictions
    df = pd.DataFrame({'Predicted_Label': predictions})

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)  # Set index=False to exclude row numbers

train=pd.read_csv("/kaggle/input/grp-project-ml/train.csv")
test=pd.read_csv("/kaggle/input/grp-project-ml/test.csv")
valid=pd.read_csv("/kaggle/input/grp-project-ml/valid.csv")

train.head()

test.head()

valid.head()

train.info()

train.dtypes

#Check is there any NaN values

train.isnull().sum()

#check is there any duplicates in the data set
train.drop_duplicates()


#only label_2 has NaN values

#cheack is there any string values, if there any string values we can encode the values.
contains_strings=train.applymap(lambda x: isinstance(x, str))
if contains_strings.any().any():
    print("There are string values in the DataFrame columns.")
else:
    print("There are no string values in the DataFrame columns.")

"""label 1"""

train_x_label_1=train.iloc[:, :-4]
train_y_label_1=train.iloc[:,-1:]
valid_x_label_1=valid.iloc[:, :-4]
valid_y_label_1=valid.iloc[:,-1:]
test_x_label_1=test.iloc[:, 1:]
train_x_label_1
print(valid_y_label_1,train_y_label_1)

# knn(train_x_label_1,train_y_label_1,valid_x_label_1,valid_y_label_1)
# Accuracy using knn: 0.77

# train_and_evaluate_models(train_x_label_1,train_y_label_1,valid_x_label_1,valid_y_label_1)
# {'Random Forest': 0.7733333333333333, 'SVM': 0.9426666666666667, 'Logistic Regression': 0.9226666666666666, 'K-Nearest Neighbors': 0.9413333333333334, 'Naive Bayes': 0.39066666666666666, 'Decision Tree': 0.664}
# {'Random Forest': 0.7733333333333333,
#  'SVM': 0.9426666666666667,
#  'Logistic Regression': 0.9226666666666666,
#  'K-Nearest Neighbors': 0.9413333333333334,
#  'Naive Bayes': 0.39066666666666666,
#  'Decision Tree': 0.664}

#check duplicates
train_features_T = train_x_label_1.T
train_features_T.shape
print(train_features_T.duplicated().sum())

train_y_label_1

print(train_y_label_1['label_4'])

import matplotlib.pyplot as plt
plt.hist(train_y_label_1['label_4'], bins=10, edgecolor='k')  # Adjust the number of bins as needed
plt.xlabel('label 4 values')
plt.ylabel('Frequency')
plt.title('Frequency Distribution of Target Values')
plt.grid(True)

# Show the plot
plt.show()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report


from imblearn.over_sampling import RandomOverSampler
# # Apply SMOTE to oversample the minority classes
# smote = SMOTE(sampling_strategy='auto', random_state=42)
# x_train_resampled, y_train_resampled = smote.fit_resample(x_train, y_train)


over_sampler = RandomOverSampler(sampling_strategy='auto')
train_x_label_1, train_y_label_1= over_sampler.fit_resample(train_x_label_1,train_y_label_1)
cross_validation(train_x_label_1, train_y_label_1,valid_x_label_1,validation_y_label_1)
# train_and_evaluate_models(train_x_label_1,train_y_label_1,valid_x_label_1,valid_y_label_1)


# {'Random Forest': 0.7946666666666666,
#  'SVM': 0.9106666666666666,
#  'Logistic Regression': 0.8773333333333333,
#  'K-Nearest Neighbors': 0.9253333333333333,
#  'Naive Bayes': 0.336,
#  'Decision Tree': 0.6893333333333334}

# after sampling
# Calculate label correlations
column_to_visualize = 'label_4'

# Create a histogram
plt.hist(train_y_label_1[column_to_visualize], bins=20, edgecolor='k')
plt.xlabel(column_to_visualize)
plt.ylabel('Frequency')
plt.title(f'Distribution of {column_to_visualize}')
plt.show()
frequency_counts = train_y_label_1['label_4'].value_counts()

from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
scaled_train_x_label_1 = ss.fit_transform(train_x_label_1)
scaled_train_x_label_1
scaled_test_x_label_1=ss.fit_transform(test_x_label_1)
scaled_valid_x_label_1=ss.fit_transform(valid_x_label_1)

from sklearn.preprocessing import RobustScaler
ss = RobustScaler()
scaled_train_x_label_1 = ss.fit_transform(train_x_label_1)
scaled_train_x_label_1
scaled_test_x_label_1=ss.transform(test_x_label_1)
scaled_valid_x_label_1=ss.transform(valid_x_label_1)
acc,pred=train_and_evaluate_models(scaled_train_x_label_1,train_y_label_1,scaled_valid_x_label_1,valid_y_label_1,scaled_test_x_label_1)
print("accuracy using RobustScaler.")

scaled_train_x_label_1_df = pd.DataFrame(scaled_train_x_label_1,columns = train_x_label_1.columns)
scaled_train_x_label_1_df.describe()
scaled_test_x_label_1_df=pd.DataFrame(scaled_test_x_label_1,columns=test_x_label_1.columns)
scaled_valid_x_label_1_df=pd.DataFrame(scaled_valid_x_label_1,columns=valid_x_label_1.columns)

print("after scaling")
train_and_evaluate_models(scaled_train_x_label_1_df,train_y_label_1,scaled_valid_x_label_1,valid_y_label_1,scaled_test_x_label_1)

scaled_train_x_label_1_df.describe()

print(train_y_label_1)

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
classifier = LogisticRegression(solver='lbfgs')

# Train the classifier on the training data
classifier.fit(scaled_train_x_label_1_df,train_y_label_1)

# Classify the testing data
y_pred = classifier.predict(scaled_valid_x_label_1_df)
print(y_pred)
y_pred_test=classifier.predict(scaled_test_x_label_1_df)
# Print the classification accuracy

# write to the csv file
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(valid_y_label_1, y_pred)
print(accuracy)

write_predictions_to_csv(y_pred_test, "/kaggle/working/label_4_test_abraha1m_classifier_predictions_with_hyperameter_tuning.csv")

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split



# model = RandomForestClassifier(n_estimators=100)
# model.fit(scaled_train_x_label_1, train_y_label_1)
# y_pred = model.predict(scaled_valid_x_label_1_df)
# from sklearn.metrics import accuracy_score

# # Calculate the accuracy
# accuracy = accuracy_score(valid_y_label_1, y_pred)
# print(f'Accuracy: {accuracy:.2f}')
# Accuracy: 0.77 random forest

# correlated_features = set()
# correlation_matrix = scaled_train_x_label_1_df.corr()
# # print(correlation_matrix)
# for i in range(len(correlation_matrix .columns)):
#     for j in range(i):
#         if abs(correlation_matrix.iloc[i, j]) > 0.5:
#             colname = correlation_matrix.columns[i]
#             correlated_features.add(colname)
# # print(correlated_features)
# scaled_train_x_label_1_df.drop(labels=correlated_features, axis=1, inplace=True)
# scaled_valid_x_label_1_df.drop(labels=correlated_features, axis=1, inplace=True)
# scaled_test_x_label_1_df.drop(labels=correlated_features, axis=1, inplace=True)
# # print(scaled_train_x_label_1_df.describe(),scaled_valid_x_label_1_df.describe())
# # knn(scaled_train_x_label_1_df,train_y_label_1,scaled_valid_x_label_1_df,valid_y_label_1)
# # train_and_evaluate_models(scaled_train_x_label_1_df,train_y_label_1,scaled_valid_x_label_1,valid_y_label_1)

#Accuracy using knn: 0.76

# train_and_evaluate_models(scaled_train_x_label_1_df,train_y_label_1,scaled_valid_x_label_1_df,valid_y_label_1)
# print("Before pca accuaracy")
# {'Random Forest': 0.76,
#  'SVM': 0.9133333333333333,
#  'Logistic Regression': 0.9266666666666666,
#  'K-Nearest Neighbors': 0.9133333333333333,
#  'Naive Bayes': 0.432,
#  'Decision Tree': 0.668}
# Before pca accuaracy

from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
# Create a SelectKBest instance with a scoring function (e.g., chi-squared)
selector = SelectKBest(score_func=f_classif, k=400)  # Select the top 2 features

# Fit and transform your data to select the best k features
scaled_train_x_label_1_df = selector.fit_transform(scaled_train_x_label_1_df, train_y_label_1)
scaled_valid_x_label_1_df = selector.transform(scaled_valid_x_label_1_df)
scaled_test_x_label_1_df = selector.transform(scaled_test_x_label_1_df)

scaled_train_x_label_1_df_pca,scaled_valid_x_label_1_df_pca,scaled_test_x_label_1_df_pca=pca(scaled_train_x_label_1_df,train_y_label_1,scaled_valid_x_label_1_df,valid_y_label_1,scaled_test_x_label_1_df)

print("after PCA")
train_and_evaluate_models(scaled_train_x_label_1_df_pca,train_y_label_1,scaled_valid_x_label_1_df_pca,valid_y_label_1)

from sklearn.linear_model import LogisticRegression
model=LogisticRegression(max_iter=1000, random_state=42)
model.fit(scaled_train_x_label_1_df_pca,train_y_label_1)
y_pred = model.predict(scaled_valid_x_label_1_df_pca)
y_pred_test=model.predict(scaled_test_x_label_1_df_pca)
y_pred

# Import necessary libraries
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

# Define hyperparameter grid for KNN
param_grid = {
    'n_neighbors': [3, 5, 7],  # Adjust the range based on your needs
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

# Create a KNN classifier
knn = KNeighborsClassifier()

# Perform Grid Search with cross-validation (e.g., 5-fold cross-validation)
grid_search = GridSearchCV(estimator=knn, param_grid=param_grid, scoring='accuracy', cv=5)

# Fit the Grid Search to your training data
grid_search.fit(scaled_train_x_label_1_df_pca, train_y_label_1)

# Get the best hyperparameters
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Get the best model
best_model = grid_search.best_estimator_

# Evaluate the best model on the validation data
accuracy = best_model.score(scaled_valid_x_label_1_df_pca, valid_y_label_1)
print("Validation Accuracy with Best Model:", accuracy)

# Make predictions on the validation and test sets
y_pred = best_model.predict(scaled_valid_x_label_1_df_pca)
y_pred_test = best_model.predict(scaled_test_x_label_1_df)

# write to the csv file
write_predictions_to_csv(y_pred, "label_4_logistic_regression_predictions_with_hyperameter_tuning.csv")

# write to the csv file
write_predictions_to_csv(y_pred_test, "label_4_test_logistic_regression_predictions_with_hyperameter_tuning.csv")

y_pred

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC


# Define the parameter grid for hyperparameter tuning
param_grid = {
    'C': [0.1, 1, 10, 100],
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid']
}

# Create the SVC classifier
svc = SVC()

# Perform grid search cross-validation
grid_search = GridSearchCV(estimator=svc, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(scaled_train_x_label_1_df_pca,train_y_label_1)

# Print the best hyperparameters and score
print("Best Hyperparameters:", grid_search.best_params_)
print("Best Score:", grid_search.best_score_)

# Evaluate the tuned model on the test dataset
best_svc = grid_search.best_estimator_
accuracy = best_svc.score(scaled_valid_x_label_1_df_pca, valid_y_label_1)
print("Validation Accuracy with Best Model:", accuracy)
y_pred= best_svc.predict(scaled_valid_x_label_1_df_pca)
y_pred_test= best_svc.predict(scaled_test_x_label_1_df_pca)
print(best_svc)

write_predictions_to_csv(y_pred, "label_4_svc_with_hyperameter_tuning.csv")
write_predictions_to_csv(y_pred_test, "label_4_test_data_svc_with_hyperameter_tuning.csv")