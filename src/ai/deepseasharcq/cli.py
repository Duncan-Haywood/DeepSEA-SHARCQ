from .main import DeepSeaSharcq
import logging
import typer


def main(ai_action, data_path, result_path="./results"):
    """For use as CLI
    params:
    ai_action (str): predict or train
    data_path (str): path to data to predict for
    result_path (str): path to store results
    """
    # run ai program
    dss = DeepSeaSharcq()
    if ai_action == "train":
        dss.train(data_path)
    elif ai_action == "predict":
        # read from  data_path: str, result_path: str and pass in data
        data = None
        logging.error(NotImplementedError)
        result = dss.predict(data)
        logging.info(result)
    else:
        logging.error(
            'invalid ai_action input: choose "train" or "predict" and provide "path" for data to use'
        )


if __name__ == "__main__":
    typer.run(main)
