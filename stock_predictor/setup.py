import service


if __name__ == '__main__':
    """
    Setup the environment and initialize the data.

    This script should be executed only once at the deployment stage of the service.
    It will take some time to load the data.
    """
    # Load stock list.
    service.load_stock_list()
    # Predict all the stocks in all date range.
    service.predict_all()