import joblib
import os

from ..model import Model

from sklearn.svm import *
from sklearn.pipeline import *
from sklearn.preprocessing import *
from sklearn.metrics import *


class SVRModel(Model):
    def __init__(self):
        super().__init__()

        self.__model = None
        self.__model_sum = None

    def __del__(self):
        super().__del__()

        del self.__model
        del self.__model_sum 


    def create_model(self):
        self.__model = Pipeline([('scaler', StandardScaler()), ('svr', SVR())], verbose=True)


    def fit(self, X_train, y_train):
        self.__model.fit(X_train, y_train)


    def predict(self, X_test):
        return self.__model.predict(X_test)


    def model_summary(self, y_pred, y_test):
        summary = {}

        if y_test.shape == () or y_pred.shape == ():
            self.__model_sum = {}
            return {}
        else:
            summary = {
                'MAE': mean_absolute_error(y_test, y_pred),
                'MSE': mean_squared_error(y_test, y_pred),
                # 'R2': r2_score(y_test, y_pred),
                'MDAE': median_absolute_error(y_test, y_pred)
            }

            self.__model_sum = summary

        return summary


    def save_model(self, name):
        temp = name.split('/')

        if not os.path.exists(f'static/saved_models/{temp[0]}'):
            os.mkdir(f'static/saved_models/{temp[0]}')

        model_filename = f'static/saved_models/{name}.pkl'
        model_summary_filename = f'static/saved_models/{name}_summary.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.__model, model_filename)
        joblib.dump(self.__model_sum, model_summary_filename)