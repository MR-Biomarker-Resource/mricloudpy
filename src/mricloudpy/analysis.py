import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
import statsmodels.api as sm
from sklearn.metrics import roc_curve, auc, roc_auc_score, mean_squared_error, RocCurveDisplay
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Ordinary Least Squares (OLS) regression method
def OLS(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, 
        residual_plot: bool = False):
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
def Logit(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, 
          roc_plot: bool = False):
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

def RandomForest(self, covariate_dataset, covariates: list, outcome: str, log: bool = False, 
                 classifier: bool = False, n_estimators: int = 200, random_state: int = 42, 
                 importance_plot: bool = False):
    # Copy the dataset
    df = covariate_dataset.copy()

    # Filter out non-level 5 regions
    filtered_cols = [col for col in df.columns if ('_Type' not in col) or ('1.0_L5.0' in col)]
    df = df[filtered_cols]

    # Define the outcome variable
    y = df[outcome]

    # Prepare covariates (if log)
    if log:
        X = np.log(df[covariates])
    else:
        X = df[covariates]

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=random_state)

    # Initialize the Random Forest
    if classifier:
        rf_regressor = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    else:
        rf_regressor = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)

    # Fit model on training data
    rf_regressor.fit(X_train, y_train)

    # Make predictions on test data
    y_pred = rf_regressor.predict(X_test)

    # Calculate model accuracy
    accuracy = rf_regressor.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

    # Calculate MSE
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE: {mse:.2f}")

    # Model feature importance
    feature_importances = rf_regressor.feature_importances_
    print("Feature Importance:")
    for feature, importance in zip(covariates, feature_importances):
        print(f"\t{feature}: {importance:.4f}")

    # If importance_plot is True
    if importance_plot:
        # Feature importance plot
        df_plot = pd.DataFrame({
            'Features': covariates,
            'Importance': feature_importances
        }).sort_values('Importance')

        fig = px.bar(df_plot, x='Importance', y='Features', orientation='h', title='Feature Importances')
        fig.show()

    return rf_regressor, y_pred, accuracy, mse, fig