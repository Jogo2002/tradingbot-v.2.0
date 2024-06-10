from alpaca.data import CryptoLatestQuoteRequest

import Bootstrapper
from Bootstrapper import *

trading_client = TradingClient('PKR15WNRQMSNV8NZR33I', '8GgBMXxRkDnSbFe2PFs5fDKpCPAmHVwFfU0G00B8', paper=True)

client = CryptoHistoricalDataClient('PKR15WNRQMSNV8NZR33I', '8GgBMXxRkDnSbFe2PFs5fDKpCPAmHVwFfU0G00B8')

isStopLoss = False
while True:
    Crypto = "BTCUSD"
    end = datetime.now()
    RSIstart = end - timedelta(days=13)

    RSI_bars_req = CryptoBarsRequest(
        symbol_or_symbols=Crypto,
        timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
        start = RSIstart,
        end = end,
    )

    SMAstart = end - timedelta(days = 20)
    SMA_bars_req = StockBarsRequest(
        symbol_or_symbols=Crypto,
        timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
        start = SMAstart,
        end = end,
    )
    SMAdf = client.get_stock_bars(SMA_bars_req).df


    portfolio = trading_client.get_all_positions()
    request_params = StockLatestQuoteRequest(symbol_or_symbols=Crypto)
    latest_quote = client.get_stock_latest_quote(request_params)
    price = ((latest_quote[Crypto].ask_price) + (latest_quote[Crypto].bid_price)) /2
    print('curr price is ', price)

    RSIdf = client.get_crypto_bars(RSI_bars_req).df
    # print(df.head)
    # print(df.tail)

    RSIdf['RSI'] = ta.rsi(RSIdf['close'],length=14)
    RSIlatest_data_point = RSIdf.iloc[-2]
    print(RSIlatest_data_point['RSI'])


    SMAdf['sma'] = SMAdf['close'].rolling(window=20).mean()

    # Calculate the standard deviation
    SMAdf['stddev'] = SMAdf['close'].rolling(window=20).std()

    # Calculate upper and lower Bollinger Bands
    SMAdf['upper_band'] =SMAdf['sma'] + (2 *SMAdf['stddev'])
    SMAdf['lower_band'] =SMAdf['sma'] - (2 *SMAdf['stddev'])
    # print(df.columns)
    # print(df)
    SMAlatest_data_point =SMAdf.iloc[-1]

    print('lower band is: ', SMAlatest_data_point['lower_band'])
    print('upper band is: ', SMAlatest_data_point['upper_band'])
    print('latest sma price is ' , SMAlatest_data_point['sma'])

    # Get our position in AAPL.
    # stock_position = trading_client.get_open_position('AAPL')
    # print(type(stock_position))
    #

    # Get a list of all of our positions.
    portfolio = trading_client.get_all_positions()

    if len(portfolio) == 0:
        print("you have 0 posiions")
        if price < SMAlatest_data_point['lower_band'] and RSIlatest_data_point['RSI'] < 50:
            print("buy signal")
            market_order_data = MarketOrderRequest(
                symbol=Crypto,
                notional=100000,
                side=OrderSide.BUY,
                stop_loss=StopLossRequest(stop_price=float(price) * 0.99), #1% stop loss
                time_in_force=TimeInForce.DAY
            )
            market_order = trading_client.submit_order(market_order_data)
    elif len(portfolio) > 0:
        print("you have one position ")
        if price >= SMAlatest_data_point['sma']:
            trading_client.close_all_positions()

    print("")
    time.sleep(55)
