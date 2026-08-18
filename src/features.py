from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from config import TRAIN_CSV_PATH
from data import load_data

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
    def __init__(self, dayColumn='date'): 
        self.dayColumn = dayColumn
    def fit(self, X, y=None):
        self.diaPrimero_ = X[self.dayColumn].min()
        return self
    def transform(self, X, y=None):
        output = (X[self.dayColumn] - self.diaPrimero_).dt.days + 1

        return output.to_frame()

######################

    
def get_column_transformer():
    """
    
    Prepare a column transformer for the data to preprocces it before training the model

    Returns:
        ColumnTransformer: The column transformer
    """
    ct = ColumnTransformer([
        ('days_since_start', DaysSinceStartTransformer(), ['date']),
        ()
    ])
    return ct



if __name__ == "__main__":
    train_df = load_data(TRAIN_CSV_PATH)

    ct = get_column_transformer()
    trf = ct.fit(train_df)

    print(trf.transform(train_df))