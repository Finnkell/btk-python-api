from abc import ABCMeta, abstractmethod


class Model(metaclass=ABCMeta):
    def __init__(self):
        return

    def __del__(self):
        return

    @abstractmethod
    def create_model(self, **kwargs):
        return

    @abstractmethod
    def fit(self, X_train, y_train):
        return

    @abstractmethod
    def predict(self, X_test):
        return

    @abstractmethod
    def model_summary(self):
        return

    @abstractmethod
    def save_model(self):
        return