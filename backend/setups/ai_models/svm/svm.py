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
        self.__model_sum_deploy = None

    def __del__(self):
        super().__del__()

        del self.__model
        del self.__model_sum
        del self.__model_sum_deploy

    def create_model(self):
        self.__model = Pipeline(
            [('scaler', StandardScaler()), ('svr', SVR())], verbose=True)

    def fit(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.__model.predict(X_test)

    def model_summary(self, y_pred, y_test, y_pred_deploy, y_deploy):
        summary = {}

        if y_test.shape == () or y_pred.shape == ():
            self.__model_sum = {}
            return {}, {}
        else:
            summary = {
                'MAE': round(mean_absolute_error(y_test, y_pred)*100, 2),
                'MSE': round(mean_squared_error(y_test, y_pred)*100, 2),
                # 'R2': r2_score(y_test, y_pred),
                'MDAE': round(median_absolute_error(y_test, y_pred)*100, 2)
            }

            self.__model_sum = summary

            if type(y_deploy) == type(None) and type(y_pred_deploy) == type(None):
                self.__model_sum_deploy = {}
                return summary, {}
            else:
                summary_deploy = {
                    'MAE': mean_absolute_error(y_deploy, y_pred_deploy),
                    'MSE': mean_squared_error(y_deploy, y_pred_deploy),
                    'R2': r2_score(y_deploy, y_pred_deploy),
                    'MDAE': median_absolute_error(y_deploy, y_pred_deploy)
                }

                self.__model_sum_deploy = summary_deploy

        return summary, summary_deploy

    def save_model(self, name):
        temp = name.split('/')

        if not os.path.exists(f'static/saved_models/{temp[0]}'):
            os.mkdir(f'static/saved_models/{temp[0]}')

        model_filename = f'static/saved_models/{name}.pkl'
        model_summary_filename = f'static/saved_models/{name}_summary.pkl'
        model_summary_deploy_filename = f'static/saved_models/{name}_summary_deploy.pkl'

        print(f'Saving model to {model_filename}...')

        joblib.dump(self.__model, model_filename)
        joblib.dump(self.__model_sum, model_summary_filename)
        joblib.dump(self.__model_sum_deploy, model_summary_deploy_filename)
