# -*- coding: utf-8 -*-
"""layer-11-label-2-190088H.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d-O-Nfn9xtwNY3q6uF7zdfm-Uu1guWfW
"""

#function for knn model using and check accuarcy

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
def knn(train_x,train_y,valid_x,valid_y):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(train_x, train_y)
    y_pred = model.predict(valid_x)
    accuracy = accuracy_score(valid_y, y_pred)
    print(f'Accuracy using knn: {accuracy:.2f}')

#function for data preprocessing
from sklearn.preprocessing import StandardScaler
def preprocessing(label,test_x_label_1,valid_x_label_1):
    train=pd.read_csv("train.csv")
    test=pd.read_csv("test.csv")
    valid=pd.read_csv("valid.csv")
    train_x_label_1=train.iloc[:, :-4]
    train_y_label_1=train.iloc[:,-5+label]

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

train=pd.read_csv("/kaggle/input/ml-grp-project-train-data-set/train.csv")
test=pd.read_csv("/kaggle/input/ml-grp-project-test-data-set/test.csv")
valid=pd.read_csv("/kaggle/input/ml-grp-project-test-data-set/valid.csv")

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

# hyper parameter tuninng
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression


def logistic_regression_hyper_parameter(scaled_train_x_label_1_df,train_y_label_1,scaled_valid_x_label_1_df,valid_y_label_1):
    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],  # Adjust the range based on your needs
        'penalty': ['l1', 'l2', 'elasticnet', 'none'],
        'solver': ['liblinear', 'lbfgs', 'newton-cg', 'sag', 'saga'],
        'max_iter': [100, 200, 300]  # Adjust the range based on your needs
    }

    # Create a Logistic Regression classifier
    logistic_regression = LogisticRegression()

    # Perform Grid Search with cross-validation (e.g., 5-fold cross-validation)
    grid_search = GridSearchCV(estimator=logistic_regression, param_grid=param_grid, scoring='accuracy', cv=5)

    # Fit the Grid Search to your training data
    grid_search.fit(scaled_train_x_label_1_df,train_y_label_1)

    # Get the best hyperparameters
    best_params = grid_search.best_params_
    print("Best Hyperparameters:", best_params)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Evaluate the best model on the validation data
    accuracy = best_model.score(scaled_valid_x_label_1_df, valid_y_label_1)
    print("Validation Accuracy with Best Model:", accuracy)
    y_pred= best_model.predict(scaled_valid_x_label_1_df)

"""**label 2**

impute the nan al
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load your dataset (replace 'your_dataset.csv' with your actual dataset)
data = pd.read_csv('/kaggle/input/ml-grp-project-layer-11/train.csv')

# Separate the dataset into two parts: one with missing target values and one without
data_missing_target = data[data['label_2'].isna()]
data_not_missing_target = data[~data['label_2'].isna()]

# Define features (X) and the target variable (y) for regression
X = data_not_missing_target.drop(columns=['label_2','label_1','label_3','label_4'])  # Features
y = data_not_missing_target['label_2']  # Target variable


# Train a Linear Regression model
regression_model = LinearRegression()
regression_model.fit(X, y)

# Use the trained model to predict missing target values
X_missing_target = data_missing_target.drop(columns=['label_2','label_1','label_3','label_4'])  # Features for rows with missing targets
predicted_target_values = regression_model.predict(X_missing_target)


# Update the original dataset with imputed target values
data_missing_target['label_2'] = predicted_target_values.round(decimals=0)

# Concatenate the two datasets back together
imputed_data = pd.concat([data_not_missing_target, data_missing_target])

# Now 'imputed_data' contains the original data with missing target values imputed
imputed_data

# scaling
# scaling function
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
def scale(train,valid_x,test,label):
    train_x_label_1=train.iloc[:, :-4]
    train_y_label_1=train.iloc[:,-5+label]

    valid_x_label_1=valid.iloc[:, :-4]
    valid_y_label_1=valid.iloc[:,-5+label]

    test_x_label_1=test.iloc[:, :-4]
    test_y_label_1=test.iloc[:,-5+label]

    ss = RobustScaler()
    scaled_train_x_label = ss.fit_transform(train_x_label_1)
    scaled_test_x_label=ss.fit_transform(test_x_label_1)
    scaled_valid_x_label=ss.fit_transform(valid_x_label_1)

    scaled_train_x_label_df = pd.DataFrame(scaled_train_x_label,columns = train_x_label_1.columns)
    scaled_test_x_label_df=pd.DataFrame(scaled_test_x_label,columns=test_x_label_1.columns)
    scaled_valid_x_label_df=pd.DataFrame(scaled_valid_x_label,columns=valid_x_label_1.columns)

    return scaled_train_x_label_df,scaled_valid_x_label_df,scaled_test_x_label_df,train_y_label_1,valid_y_label_1



valid=pd.read_csv('/kaggle/input/ml-grp-project-layer-11/valid.csv')
valid=valid.dropna()
test=pd.read_csv('/kaggle/input/ml-grp-project-layer-11/test.csv')
scaled_train_x_label_2,scaled_valid_x_label_2,scaled_test_x_label_2,train_y_label_2,valid_y_label_2=scale(imputed_data,valid,test,2)

# print(scaled_train_x_label_2,scaled_valid_x_label_2,train_y_label_2,valid_y_label_2)

# remove  nan values in valid data set

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

def train_and_evaluate_models(X_train, y_train, X_val, y_val,test_x):

    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='linear', C=1.0, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
#         'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
#         'Naive Bayes': GaussianNB(),
#         'Decision Tree': DecisionTreeClassifier(random_state=42)
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

scaled_valid_x_label_2
cross_validation(scaled_train_x_label_2,train_y_label_2,scaled_valid_x_label_2,valid_y_label_2)

#use knn without preprocessing
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import hamming_loss, jaccard_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# knn = KNeighborsClassifier(n_neighbors=5)

# Train the model
# knn.fit(scaled_train_x_label_2,train_y_label_2)

# # Make predictions on the test set
# y_pred = knn.predict(scaled_valid_x_label_2)
# print(accuracy_score(valid_y_label_2, y_pred))
# print(classification_report(valid_y_label_2,y_pred))


train_and_evaluate_models(scaled_train_x_label_2,train_y_label_2,scaled_valid_x_label_2,valid_y_label_2,scaled_test_x_label_2)
# {'Random Forest': 0.7635869565217391,
#  'SVM': 0.7880434782608695,
#  'Logistic Regression': 0.7894021739130435,
#  'K-Nearest Neighbors': 0.8383152173913043,
#  'Naive Bayes': 0.3383152173913043,
#  'Decision Tree': 0.3654891304347826}

scaled_train_x_label_2_df = pd.DataFrame(scaled_train_x_label_2,columns = scaled_train_x_label_2.columns)
scaled_train_x_label_2_df.describe()
scaled_test_x_label_2_df=pd.DataFrame(scaled_test_x_label_2,columns=scaled_valid_x_label_2.columns)
scaled_valid_x_label_2_df=pd.DataFrame(scaled_valid_x_label_2,columns=scaled_test_x_label_2.columns)

from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
# Create a SelectKBest instance with a scoring function (e.g., chi-squared)
selector = SelectKBest(score_func=f_classif, k=400)  # Select the top 2 features

# Fit and transform your data to select the best k features
scaled_train_x_label_2_df = selector.fit_transform(scaled_train_x_label_2_df, train_y_label_2)
scaled_valid_x_label_2_df = selector.transform(scaled_valid_x_label_2_df)
scaled_test_x_label_2_df = selector.transform(scaled_test_x_label_2_df)

acc,pred=train_and_evaluate_models(scaled_train_x_label_2_df,train_y_label_2,scaled_valid_x_label_2_df,valid_y_label_2,scaled_test_x_label_2_df)
print("accuracy after k best.")
y_pred_test=pred['Logistic Regression']
write_predictions_to_csv(y_pred_test,"lgistic regression label 1 layer 8 after k best.csv")

from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
# Create a SelectKBest instance with a scoring function (e.g., chi-squared)
selector = SelectKBest(score_func=f_classif, k=400)  # Select the top 2 features

# Fit and transform your data to select the best k features
scaled_train_x_label_2_df = selector.fit_transform(scaled_train_x_label_2_df,train_y_label_2)
scaled_valid_x_label_2_df = selector.transform(scaled_valid_x_label_2_df)
scaled_test_x_label_2_df = selector.transform(scaled_test_x_label_2_df)

acc,pred=train_and_evaluate_models(scaled_train_x_label_2_df,train_y_label_2,scaled_valid_x_label_2_df,valid_y_label_2,scaled_test_x_label_2_df)
print("accuracy after k best.")
y_pred_test=pred['Logistic Regression']
write_predictions_to_csv(y_pred_test,"lgistic regression label 2 layer 11 after k best.csv")

y_pred_test=pred['SVM']
write_predictions_to_csv(y_pred_test,"SVC label 2 layer 11 after k best.csv")

# correlated_features = set()
# correlation_matrix = scaled_train_x_label_2.corr()
# # print(correlation_matrix)
# for i in range(len(correlation_matrix .columns)):
#     for j in range(i):
#         if abs(correlation_matrix.iloc[i, j]) > 0.5:
#             colname = correlation_matrix.columns[i]
#             correlated_features.add(colname)
# # print(correlated_features)
# scaled_train_x_label_2.drop(labels=correlated_features, axis=1, inplace=True)
# scaled_valid_x_label_2.drop(labels=correlated_features, axis=1, inplace=True)
# scaled_test_x_label_2.drop(labels=correlated_features, axis=1, inplace=True)
# print(scaled_train_x_label_2.shape,scaled_valid_x_label_2.shape)
# # knn(scaled_train_x_label_2,train_y_label_2,scaled_valid_x_label_2,valid_y_label_2)
# train_and_evaluate_models(scaled_train_x_label_2,train_y_label_2,scaled_valid_x_label_2,valid_y_label_2)
# after removing corelated features
# {'Random Forest': 0.7472826086956522,
#  'SVM': 0.7703804347826086,
#  'Logistic Regression': 0.7635869565217391,
#  'K-Nearest Neighbors': 0.8315217391304348,
#  'Naive Bayes': 0.3736413043478261,
#  'Decision Tree': 0.3845108695652174}

# pca approch_
from sklearn.decomposition import PCA
def pca(train_x,train_y,valid_x,valid_y,test):
    pca=PCA(.95, svd_solver='full')
    pca=pca.fit(train_x)
    train_features_pca=pca.transform(train_x)
    valid_features_pca=pca.transform(valid_x)
    test_features_pca=pca.transform(test_x)
    return train_features_pca,valid_features_pca,test_features_pca


scaled_train_x_label_2_df_pca,scaled_valid_x_label_2_df_pca,scaled_test_x_label_2_df_pca=pca(scaled_train_x_label_2_df,train_y_label_2,scaled_valid_x_label_2_df,valid_y_label_2,scaled_test_x_label_2_df)
acc,pred=train_and_evaluate_models(scaled_train_x_label_2_df_pca,train_y_label_2,scaled_valid_x_label_2_df_pca,valid_y_label_2,scaled_test_x_label_2_df_pca)
print("accuracy after k best.")
y_pred_test=pred['Logistic Regression']
y_pred_test_svc=pred['SVM']
write_predictions_to_csv(y_pred_test,"logistic regression label 2 layer 11 after pca.csv")
write_predictions_to_csv(y_pred_test_svc,"SVM label 2 layer 11 after pca.csv")
# after pca for the data set
# {'Random Forest': 0.7472826086956522,
#  'SVM': 0.7703804347826086,
#  'Logistic Regression': 0.7635869565217391,
#  'K-Nearest Neighbors': 0.8315217391304348,
#  'Naive Bayes': 0.3736413043478261,
#  'Decision Tree': 0.3845108695652174}

from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf', 'poly'],
}

grid_search = GridSearchCV(
    estimator=SVC(kernel="linear"),
    param_grid=param_grid,
    scoring='accuracy',
    cv=5,
    n_jobs=-1
)

# Fit the grid search to your data
grid_search.fit(scaled_train_x_label_2_df_pca,train_y_label_2)
# Get the best hyperparameters
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Get the best model
best_model = grid_search.best_estimator_

# Evaluate the best model on the validation data
accuracy = best_model.score(scaled_valid_x_label_2_df_pca, valid_y_label_2)
print("Validation Accuracy with Best Model:", accuracy)
y_pred= best_model.predict(scaled_valid_x_label_2_df_pca)
y_pred_test=best_model.predict(scaled_test_x_label_2_df_pca)

write_predictions_to_csv(y_pred_test, "label_2_layer_11_svc_predictions_with_hyperameter_tuning.csv")



