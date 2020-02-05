import datetime
import unittest

from python_snippets.datetime.get_date_range import get_date_range, get_datetime_params


class TestDateRange(unittest.TestCase):

    def test_aggregate_customer_revisit(self):
        result = [{'from': datetime.datetime(2019, 3, 1, 0, 0), 'to': datetime.datetime(2019, 3, 7, 23, 59, 59)},
                  {'from': datetime.datetime(2019, 3, 8, 0, 0), 'to': datetime.datetime(2019, 3, 14, 23, 59, 59)},
                  {'from': datetime.datetime(2019, 3, 15, 0, 0), 'to': datetime.datetime(2019, 3, 21, 23, 59, 59)},
                  {'from': datetime.datetime(2019, 3, 22, 0, 0), 'to': datetime.datetime(2019, 3, 28, 23, 59, 59)},
                  {'from': datetime.datetime(2019, 3, 29, 0, 0), 'to': datetime.datetime(2019, 3, 31, 23, 59, 58)}]

        from_date = '2019-03-01 00:00:00'
        to_date = '2019-03-31 23:59:59'

        date_time = get_datetime_params(from_date, to_date)

        date_range = get_date_range(date_time.from_time, date_time.to_time, 'weeks')
        self.assertEqual(date_range, result)
