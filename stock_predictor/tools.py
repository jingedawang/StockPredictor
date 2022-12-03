import argparse
import datetime

from service import Service


if __name__ == '__main__':
    """
    Command line tools for stock predictor.
    """
    # Read params from command line.
    argparser = argparse.ArgumentParser(description='Tools of stock predictor.')
    argparser.add_argument('name', type=str, help='The name of the requested tool. Choose from [predict_all], [fix_missing_prediction] and [update_stock_list].')
    args = argparser.parse_args()

    service = Service()
    # Run the tool specified by the name param.
    if args.name == 'predict_all':
        # Do today's prediction for all stocks.
        service.predict_all(date=datetime.date.today().strftime('%Y-%m-%d'))
    elif args.name == 'fix_missing_prediction':
        # Fix the missing predictions by re-try predicting for the missed dates.
        service.fix_mising_prediction()
    elif args.name == 'update_stock_list':
        # Update stock list according to official stock exchange website.
        service.load_stock_list()
    else:
        print(f'Not supported tool name: {args.name}')