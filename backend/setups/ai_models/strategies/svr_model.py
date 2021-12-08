from ..svm.svm import SVRModel

import pandas as pd
import numpy as np
import vectorbt as vbt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


class SVRStrategyModel:

    def __init__(self):
        return

    def model_run(self, name, X_train, X_test, y_train, y_test, X_deploy, y_deploy):
        model = SVRModel()
        model.create_model()
        model.fit(X_train, y_train)

        if type(X_deploy) != type(None) and type(y_deploy) != type(None):
            y_pred = model.predict(X_test)
            y_pred_deploy = model.predict(X_deploy)

            print(model.model_summary(y_pred, y_test, y_pred_deploy, y_deploy))

            model.save_model(f'{name}/SVR')

            return True
        else:
            y_pred = model.predict(X_test)
            print(model.model_summary(y_pred, y_test,
                  None, None))
            model.save_model(f'{name}/SVR')

            return True

        return False

    def strategy_run(self, asset_name, df, start_date, end_date, train_size, test_size, deploy_size):
        df['Date'] = df.index

        columns = {
            'Date': 'datetime',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
        }

        df.drop(['Volume', 'Adj Close'], axis=1, inplace=True)

        df.rename(columns=columns, inplace=True)

        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', drop=True, inplace=True)

        df = df[start_date:end_date]

        df['log_return'] = np.log(df['close']/df['close'].shift(-1))

        df['diff'] = df['high'] - df['low']

        df['ma_2'] = vbt.MA.run(df['diff'], 2).ma
        df['ma_5'] = vbt.MA.run(df['diff'], 5).ma
        df['ma_10'] = vbt.MA.run(df['diff'], 10).ma
        df['ma_15'] = vbt.MA.run(df['diff'], 15).ma
        df['ma_30'] = vbt.MA.run(df['diff'], 30).ma

        df.loc[df['ma_2'] > df['ma_2'].shift(1), 'tend_2'] = 1
        df.loc[df['ma_2'] < df['ma_2'].shift(1), 'tend_2'] = -1
        df.loc[df['ma_2'] == df['ma_2'].shift(1), 'tend_2'] = 0

        df.loc[df['ma_5'] > df['ma_5'].shift(4), 'tend_5'] = 1
        df.loc[df['ma_5'] < df['ma_5'].shift(4), 'tend_5'] = -1
        df.loc[df['ma_5'] == df['ma_5'].shift(4), 'tend_5'] = 0

        df.loc[df['ma_10'] > df['ma_10'].shift(9), 'tend_10'] = 1
        df.loc[df['ma_10'] < df['ma_10'].shift(9), 'tend_10'] = -1
        df.loc[df['ma_10'] == df['ma_10'].shift(9), 'tend_10'] = 0

        df.loc[df['ma_15'] > df['ma_15'].shift(14), 'tend_15'] = 1
        df.loc[df['ma_15'] < df['ma_15'].shift(14), 'tend_15'] = -1
        df.loc[df['ma_15'] == df['ma_15'].shift(14), 'tend_15'] = 0

        df.loc[df['ma_30'] > df['ma_30'].shift(29), 'tend_30'] = 1
        df.loc[df['ma_30'] < df['ma_30'].shift(29), 'tend_30'] = -1
        df.loc[df['ma_30'] == df['ma_30'].shift(29), 'tend_30'] = 0

        df['desv_2'] = df['log_return'].rolling(window=2).std()
        df['desv_5'] = df['log_return'].rolling(window=5).std()
        df['desv_10'] = df['log_return'].rolling(window=10).std()
        df['desv_15'] = df['log_return'].rolling(window=15).std()
        df['desv_30'] = df['log_return'].rolling(window=30).std()

        df.loc[(df['close'] > df['close'].shift(2)) &
               df['desv_2'].notnull(), 'var_2'] = df['desv_2']
        df.loc[(df['close'] < df['close'].shift(2)), 'var_2'] = -df['desv_2']

        df.loc[(df['close'] > df['close'].shift(5)) &
               df['desv_5'].notnull(), 'var_5'] = df['desv_5']
        df.loc[(df['close'] < df['close'].shift(5)), 'var_5'] = -df['desv_5']

        df.loc[(df['close'] > df['close'].shift(10)) &
               df['desv_10'].notnull(), 'var_10'] = df['desv_10']
        df.loc[(df['close'] < df['close'].shift(10)),
               'var_10'] = -df['desv_10']

        df.loc[(df['close'] > df['close'].shift(15)) &
               df['desv_15'].notnull(), 'var_15'] = df['desv_15']
        df.loc[(df['close'] < df['close'].shift(15)),
               'var_15'] = -df['desv_15']

        df.loc[(df['close'] > df['close'].shift(30)) &
               df['desv_30'].notnull(), 'var_30'] = df['desv_30']
        df.loc[(df['close'] < df['close'].shift(30)),
               'var_30'] = -df['desv_30']

        df['ma_2'].fillna(df['ma_2'].mean(), inplace=True)
        df['ma_5'].fillna(df['ma_5'].mean(), inplace=True)
        df['ma_10'].fillna(df['ma_10'].mean(), inplace=True)
        df['ma_15'].fillna(df['ma_15'].mean(), inplace=True)
        df['ma_30'].fillna(df['ma_30'].mean(), inplace=True)

        df['tend_2'].fillna(0, inplace=True)
        df['tend_5'].fillna(0, inplace=True)
        df['tend_10'].fillna(0, inplace=True)
        df['tend_15'].fillna(0, inplace=True)
        df['tend_30'].fillna(0, inplace=True)

        df['desv_2'].fillna(df['desv_2'].median(), inplace=True)
        df['var_2'].fillna(df['var_2'].median(), inplace=True)

        df['desv_5'].fillna(df['desv_5'].median(), inplace=True)
        df['var_5'].fillna(df['var_5'].median(), inplace=True)

        df['desv_10'].fillna(df['desv_10'].median(), inplace=True)
        df['var_10'].fillna(df['var_10'].median(), inplace=True)

        df['desv_15'].fillna(df['desv_15'].median(), inplace=True)
        df['var_15'].fillna(df['var_15'].median(), inplace=True)

        df['desv_30'].fillna(df['desv_30'].median(), inplace=True)
        df['var_30'].fillna(df['var_30'].median(), inplace=True)

        y = df['log_return'].shift(-1).fillna(df['log_return'].median())
        X = df.drop(['log_return', 'tend_2', 'tend_5',
                    'tend_10', 'tend_15', 'tend_30', ], axis=1)

        if deploy_size == 0.0:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, train_size=train_size, random_state=123, shuffle=False)

            return self.model_run(asset_name, X_train, X_test, y_train, y_test, None, None)
        else:
            train_value = int(len(X)*((1-deploy_size) - train_size))
            test_value = int(len(X)*((1-deploy_size) - test_size))
            deploy_value = int(len(X)*((train_size + test_size)) - deploy_size)

            X_train, X_test, X_deploy, y_train, y_test, y_deploy = X[:train_value], X[test_value: deploy_value], X[
                deploy_value:], y[: train_value], y[test_value: deploy_value], y[deploy_value:]

            return self.model_run(asset_name, X_train, X_test, y_train, y_test, X_deploy, y_deploy)
