import logging


class DeepSeaSharcq:
    def __init__(self):
        logging.error(NotImplementedError)

    def predict(self, data):
        logging.error(NotImplementedError)
        return "Not Implemented"

    def train(self, data_path: str):
        return NotImplementedError

    def evaluate(self, data_path: str):
        return NotImplementedError
