import os
from dotenv import load_dotenv
from alpaca.trading.requests import MarketOrderRequest, StopLossRequest
from alpaca.data.requests import CryptoBarsRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.trading.client import TradingClient
import time
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as ta
import requests
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data import StockHistoricalDataClient, StockBarsRequest, TimeFrame, TimeFrameUnit
from alpaca.data import StockQuotesRequest
from pandas import DataFrame
from pandas_ta import Imports
from pandas_ta.overlap import ma
from pandas_ta.statistics import stdev
from pandas_ta.utils import get_offset, non_zero_range, tal_ma, verify_series
import vectorbt as vbt

vbt.settings.data['alpaca']['key_id'] = 'PKRFQTGJK2BICR83GNMT'
vbt.settings.data['alpaca']['secret_key'] = 'ZHn648I6vUH38cFiT0xW91uJGQGwarTqSIPR9mlO'

API_KEY = 'PKRZUU58WZP1YJ9KKPU7'
SECRET_KEY = 'rZtc2vlTGIFK5txaaHgCyBFxDfkfo5mdzlHJJDKA'
