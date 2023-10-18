# Library imports
import datetime
import requests_cache
import matplotlib.pyplot as plt
from pandas_datareader import data as wb


class Ticker:
    """Class for fetching data for option pricing."""

    @staticmethod
    def get_historical_data(ticker, start_date, end_date):
        """
        Fetches stock data for option pricing.
        """
        try:
            # Initializing session for caching Yahoo Finance requests
            expire_after = datetime.timedelta(days=1)
            session = requests_cache.CachedSession(
                cache_name='cache', backend='sqlite', expire_after=expire_after)

            if (start_date is not None and end_date is not None):
                data = wb.get_data_yahoo(
                    ticker, start=start_date, end=end_date)
            else:
                data = wb.get_data_yahoo(ticker)

            if data is None:
                return None
            return data

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def plot_data(data, ticker, column_name):
        """
        Plots specified column values from dataframe.
        """
        try:
            if data is None:
                return
            data[column_name].plot()
            plt.ylabel(f'{column_name}')
            plt.xlabel('Date')
            plt.title(f'Historical data for {ticker} - {column_name}')
            plt.legend(loc='best')
            plt.show()

        except Exception as e:
            print(e)
            return

    @staticmethod
    def get_columns(data):
        """
        Gets dataframe columns from previously fetched stock data.
        """
        if data is None:
            return None
        return [column for column in data.columns]

    @staticmethod
    def get_last_price(data, column_name):
        """
        Returns last available price for specified column from already fetched data.
        """
        if data is None or column_name is None:
            return None
        if column_name not in Ticker.get_columns(data):
            return None
        return data[column_name].iloc[-1]
