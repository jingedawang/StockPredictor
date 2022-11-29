from service import Service


if __name__ == '__main__':
    """
    Update stock list according to official stock exchange website.
    """
    service = Service()
    service.load_stock_list()