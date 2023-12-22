import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
import statsmodels.api as sm
from sklearn.metrics import roc_curve, roc_auc_score

# Ordinary Least Squares (OLS) regression method
def OLS(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, residual_plot: bool = False):
    # Copy the dataset
    df = covariate_dataset.copy()

    # If log is True, apply log transformation to the covariates
    if log:
        X = sm.add_constant(np.log(df[covariates]))
    else:
        X = sm.add_constant(df[covariates])
        
    # Define the outcome variable
    y = df[outcome]

    # Fit the OLS model
    model = sm.OLS(y, X)
    result = model.fit()

    # If residual_plot is True, plot the residuals
    fig = None
    if residual_plot:
        fig = px.scatter(x=result.fittedvalues, y=result.resid)
        fig.add_hline(y=0)
        fig.update_layout(
            title='Residuals vs Fitted Values', 
            xaxis_title='Fitted Values', 
            yaxis_title='Residuals'
        )
        fig.show()

    # Return the summary of the model and the figure
    return result.summary(), fig

# Logistic regression method
def Logit(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, roc_plot: bool = False):
    # Copy the dataset
    df = covariate_dataset.copy()

    # Convert the 'Gender' column into dummy variables
    df = pd.get_dummies(df, columns=['Gender'], drop_first=True)

    # If log is True, apply log transformation to the covariates
    if log:
        X = sm.add_constant(np.log(df[covariates]))
    else:
        X = sm.add_constant(df[covariates])

    # Define the outcome variable
    y = df[outcome]

    # Fit the logistic regression model
    model = sm.Logit(y, X)
    result = model.fit()

    # If roc_plot is True, plot the ROC curve
    fig = None
    if roc_plot:
        y_pred = result.predict(X)
        fpr, tpr, thresholds = roc_curve(y, y_pred)
        roc_auc = roc_auc_score(y, y_pred)
        fig = go.Figure(data=[
            go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC Curve'),
            go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random Classifier')
        ])
        fig.update_layout(
            title='ROC Curve (AUC = ' + str(round(roc_auc, 3)) + ')',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
        )
        fig.show()

    # Return the summary of the model and the figure
    return result.summary(), fig