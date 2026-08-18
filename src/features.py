from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.pipeline import Pipeline
from config import TRAIN_CSV_PATH
from data import load_data
import numpy as np

# The next class is a custom tranformer for the features days_since_start
class DaysSinceStartTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer class to add a new feature 'days_since_start' to the input dataframe.
    
    This transformer calculates the number of days since the first date in the input dataframe.
    
    Parameters
    ----------
    dayColumn : str, optional
        The name of the column containing the dates. Default is 'date'.
    outputColumn : str, optional
        The name of the output column containing the number of days since the first date. Default is 'days_since_start'.
    
    Attributes
    ----------
    diaPrimero_ : datetime
        The first date in the input dataframe.
    
    Methods
    -------
    fit(self, X, y=None)
        Calculates the first date in the input dataframe.
    transform(self, X, y=None)
        Calculates the number of days since the first date for each row in the input dataframe.
    """
    def __init__(self, dayColumn='date', outputColumn='days_since_start'): 
        self.dayColumn = dayColumn
        self.outputColumn = outputColumn
    def fit(self, X, y=None):
        self.diaPrimero_ = X[self.dayColumn].min()
        return self
    def transform(self, X, y=None):
        output = (X[self.dayColumn] - self.diaPrimero_).dt.days + 1

        return output.to_frame(self.outputColumn)

######################

def extract_month_year(df):
    year = df['date'].dt.year
    month = df['date'].dt.month

    return np.column_stack((year, month))

def features_dates():
    return ['year', 'month']
day_month_transformer = FunctionTransformer(extract_month_year, feature_names_out=features_dates)

######################

    
def get_date_transformer():
    """
    
    Prepare a pipeline transformer for the data to preprocces the date before training the model

    Returns:
        Pipeline: The pipeline transformer
    """
    ct_create = ColumnTransformer([
        ('days_since_start', DaysSinceStartTransformer(), ['date']),
        ('dates', day_month_transformer, ['date'])
    ])
    general_pipeline = Pipeline([
        ('transform', ct_create),
        ('scaler', StandardScaler())
    ])
    return general_pipeline

def get_full_preprocessing():
    """
    Prepare the full pipeline with all the preprocessing steps

    Returns: 
        Pipeline: The pipeline with all the preprocessing steps
    """

    ct = ColumnTransformer([
        ('dates', get_date_transformer(), ['date']),
        ('remainder', 'passthrough', ['store_nbr', 'family'])
    ])
    return ct

######################

if __name__ == "__main__":
    train_df = load_data(TRAIN_CSV_PATH)

    ct = get_date_transformer()
    trf = ct.fit(train_df)

    print(trf.transform(train_df))