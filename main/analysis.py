import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
# from statsmodels.tools.eval_measures import rmse

def OLS(self, covariate_dataset, covariates: list, outcome: str, log: bool = False):
    
    df = covariate_dataset.copy()

    # Temp age cleanup (REMOVE)
    df['Age'] = df['Age'].str.slice(0,2).astype(int)

    if log:
        X = sm.add_constant(np.log(df[covariates]))
    else:
        X = sm.add_constant(df[covariates])
        
    y = df[outcome]

    model = sm.OLS(y, X)
    result = model.fit()

    return result.summary()

def Logit(self, covariate_dataset, covariates: list, outcome: str, log: bool = False):

    df = covariate_dataset.copy()

    # Temp age cleanup (REMOVE)
    df['Age'] = df['Age'].str.slice(0,2).astype(int)

    if log:
        X = sm.add_constant(np.log(df[covariates]))
    else:
        X = sm.add_constant(df[covariates])

    y = df[outcome]

    model = sm.Logit(y, X)
    result = model.fit()

    return result.summary()

def RandomForest(self, covariate_dataset, covariates: list, outcome: str):

    df = covariate_dataset.copy()

    # Temp age cleanup (REMOVE)
    df['Age'] = df['Age'].str.slice(0,2).astype(int)

    X = df.drop(['ID', 'Release', 'Gender'], axis=1)._get_numeric_data().dropna(axis=1)
    y = df[outcome]

    # Assuming X is your feature set and y are your labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Train the model
    model = RandomForestClassifier(n_estimators=500, max_features='sqrt', random_state=44)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Now we can use sklearn's metrics to evaluate the model's performance

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print(y_pred)

    # # Precision
    # precision = precision_score(y_test, y_pred)
    # print(f'Precision: {precision}')

    # # Recall
    # recall = recall_score(y_test, y_pred)
    # print(f'Recall: {recall}')

    # # F1 Score
    # f1 = f1_score(y_test, y_pred)
    # print(f'F1 Score: {f1}')

    # AUC-ROC
    # auc_roc = roc_auc_score(y_test, y_pred, multi_class='ovo')
    # print(f'AUC-ROC: {auc_roc}')

    # # Confusion Matrix
    # cm = confusion_matrix(y_test, y_pred)
    # print(f'Confusion Matrix: \n{cm}')

    # # Classification Report
    # cr = classification_report(y_test, y_pred)
    # print(f'Classification Report: \n{cr}')

if __name__ == '__main__':
    print(__name__)