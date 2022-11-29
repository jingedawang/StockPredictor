import datetime
import json
import tqdm
import unittest

import context
from service import Service


class TestService(unittest.TestCase):
    """
    Tests for stock predictor services.

    Note that currently, we are not able to test the whole workflow.
    These tests are more like integrated test than unit tests.
    """

    def setUp(self) -> None:
        self.service = Service()

    def test_get_stock_list(self):
        stock_list_json = self.service.get_stock_list()
        stock_list = json.loads(stock_list_json)
        for stock in stock_list:
            self.assertTrue(stock['id'].isdigit() and len(stock['id']) == 6, msg=f'{stock["id"]} is not 6-width digit.')
            self.assertTrue(len(stock['name']) > 0 and len(stock['name']) < 10, msg=f'Unexpected stock name {stock["name"]}')
            self.assertTrue(len(stock['pinyin']) == len(stock['pinyin']), msg=f'Pinyin {stock["pinyin"]} has different length with name {stock["name"]}')

    def test_get_history_and_predict_result(self):
        stock_list_json = self.service.get_stock_list()
        stock_list = json.loads(stock_list_json)
        for stock in tqdm.tqdm(stock_list):
            try:
                history_and_predict_result_json = self.service.get_history_and_predict_result(stock['id'], datetime.date.today().strftime('%Y-%m-%d'))
            except LookupError:
                continue
            history_and_predict_result = json.loads(history_and_predict_result_json)
            self.assertEqual(history_and_predict_result['id'], stock['id'], msg='Id not consistent.')
            self.assertEqual(history_and_predict_result['name'], stock['name'], msg='Name not consistent.')
            self.assertEqual(history_and_predict_result['pinyin'], stock['pinyin'], msg='Pinyin not consistent.')
            self.assertEqual(history_and_predict_result['qlib_id'][2:], stock['id'], msg='Qlib id not consistent with id.')
            self.assertTrue(history_and_predict_result['qlib_id'][:2] in ['SH', 'SZ'], msg='Qlib id not starts with SH/SZ.')
            for date_price_pair in history_and_predict_result['history']:
                for date, price in date_price_pair.items():
                    try:
                        datetime.datetime.strptime(date, '%Y-%m-%d')
                    except ValueError:
                        self.fail(msg=f'Unexpected date format for {date}')
                    self.assertGreater(price, 0, msg='History price must greater than 0.')
            for date, predicted_price in history_and_predict_result['predict'].items():
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    self.fail(msg=f'Unexpected date format for {date}')
                self.assertGreater(predicted_price, 0, msg='Predicted price must greater than 0.')
            listing_date_obj = None
            delisted_date_obj = None
            if history_and_predict_result['listing_date']:
                try:
                    listing_date_obj = datetime.datetime.strptime(history_and_predict_result['listing_date'], '%Y-%m-%d')
                except ValueError:
                    self.fail(msg=f'Unexpected date format for {history_and_predict_result["listing_date"]}')
            if history_and_predict_result['delisted_date']:
                try:
                    delisted_date_obj = datetime.datetime.strptime(history_and_predict_result['delisted_date'], '%Y-%m-%d')
                except ValueError:
                    self.fail(msg=f'Unexpected date format for {history_and_predict_result["delisted_date"]}')
            if listing_date_obj and delisted_date_obj:
                self.assertGreater(delisted_date_obj, listing_date_obj, msg='Delisted date must be later than listing date.')
            if delisted_date_obj:
                self.assertTrue(history_and_predict_result['delisted'], msg='Delisted flag must be true if delisted date exists.')

if __name__ == '__main__':
    unittest.main()