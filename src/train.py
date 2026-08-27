import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.utils.validation import check_is_fitted
from xgboost import XGBRegressor
import pandas as pd
from data import load_data
from config import TRAIN_CSV_PATH
from features import get_full_preprocessing

##### Modelo custom

class HybridModel(RegressorMixin, BaseEstimator):
    def __init__(self, *, feature_linear=["days_since_start"], feature_XGBoost=["day", "month", "store_nbr", "onpromotion"], category="store_nbr",
                 family_feature="family", random_state=None):
        self.feature_linear = feature_linear
        self.feature_XGBoost = feature_XGBoost
        self.category = category
        self.family_feature = family_feature
        self.random_state = random_state

    def _validate_input(self, X):
        if not isinstance(X, pd.DataFrame):
                    raise TypeError(
                        f"HybridModel requiere un pandas DataFrame como entrada X, "
                        f"pero se recibió {type(X).__name__}."
                    )

        if self.family_feature not in X.columns or self.category not in X.columns:
            raise ValueError(
                f"HybridModel requiere la columna '{self.family_feature}' o la columna '{self.category}' en el DataFrame X."
            )

        X_copy = X.copy()

        X_copy[self.category] = X[self.category].astype("category")

        return X_copy[self.feature_linear], X_copy[self.feature_XGBoost]
    def fit(self, X, y):
        cols_linear, cols_XGBoost = self._validate_input(X)

        # Asegurar que y tenga el mismo índice que X para poder usar máscaras booleanas
        if not isinstance(y, pd.Series):
            y = pd.Series(y, index=X.index)

        self.families_ = X[self.family_feature].unique()

        self.models_linear_ = {}

        y_pred_linear = pd.Series(index=y.index, dtype=float)

        for family in self.families_:
            mask = X[self.family_feature] == family
            if mask.any():
                X_linear = cols_linear.loc[mask, self.feature_linear]
                lr = LinearRegression().fit(X_linear, y[mask])
                self.models_linear_[family] = lr
                y_pred_linear[mask] = lr.predict(X_linear)

        y_residuals = y - y_pred_linear

        self.models_XGBoost_ = {}
        for family in self.families_:
            mask = X[self.family_feature] == family
            if mask.any():
                X_XGBoost = cols_XGBoost.loc[mask, self.feature_XGBoost]
                xgb = XGBRegressor(enable_categorical=True, random_state=self.random_state).fit(X_XGBoost, y_residuals[mask])
                self.models_XGBoost_[family] = xgb


        self.is_fitted_ = True
        return self
    def predict(self, X):
        check_is_fitted(self, "is_fitted_")

        cols_linear, cols_XGBoost = self._validate_input(X)

        y_pred_linear = pd.Series(index=X.index, dtype=float)

        for family in self.families_:
            mask = X[self.family_feature] == family
            if mask.any():
                X_linear = cols_linear.loc[mask, self.feature_linear]
                y_pred_linear[mask] = self.models_linear_[family].predict(X_linear)

        y_pred_XGBoost = pd.Series(index=X.index, dtype=float)

        for family in self.families_:
            mask = X[self.family_feature] == family
            if mask.any():
                X_XGBoost = cols_XGBoost.loc[mask, self.feature_XGBoost]
                y_pred_XGBoost[mask] = self.models_XGBoost_[family].predict(X_XGBoost)

        y_pred = y_pred_linear + y_pred_XGBoost

        y_pred[y_pred < 0] = 0

        return y_pred.to_numpy()


if __name__ == "__main__":
    train_df = load_data(TRAIN_CSV_PATH)

    ct = get_full_preprocessing()
    ct.set_output(transform='pandas')

    trf = ct.fit(train_df)

    model = HybridModel()

    model.fit(trf.transform(train_df), train_df["sales"])

    print(model.predict(trf.transform(train_df)))