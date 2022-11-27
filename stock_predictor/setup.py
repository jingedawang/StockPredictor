from service import Service


if __name__ == '__main__':
    """
    Setup the environment and initialize the data.

    This script should be executed only once at the deployment stage.
    """
    service = Service()
    # Load stock list.
    service.load_stock_list()
    # Predict for all the stocks in all date range.
    service.predict_all()