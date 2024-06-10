import Bootstrapper
from Bootstrapper import *

trading_client = TradingClient('PKRFQTGJK2BICR83GNMT', 'ZHn648I6vUH38cFiT0xW91uJGQGwarTqSIPR9mlO', paper=True)

client = StockHistoricalDataClient('PKRFQTGJK2BICR83GNMT', 'ZHn648I6vUH38cFiT0xW91uJGQGwarTqSIPR9mlO')
while True:
    Stock = "AAPL"
    end = datetime.now()
    RSIstart = end - timedelta(days=13)

    RSI_bars_req = StockBarsRequest(
        symbol_or_symbols=Stock,
        timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
        start = RSIstart,
        end = end,
    )
    
    SMAstart = end - timedelta(days = 20)
    SMA_bars_req = StockBarsRequest(
        symbol_or_symbols=Stock,
        timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
        start = SMAstart,
        end = end,
    )
    SMAdf = client.get_stock_bars(SMA_bars_req).df


    portfolio = trading_client.get_all_positions()
    request_params = StockLatestQuoteRequest(symbol_or_symbols=Stock)
    latest_quote = client.get_stock_latest_quote(request_params)
    price = ((latest_quote[Stock].ask_price) + (latest_quote[Stock].bid_price)) /2
    print('curr price is ', price)

    RSIdf = client.get_stock_bars(RSI_bars_req).df
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
                symbol=Stock,
                notional=100000, #$100,000
                side=OrderSide.BUY,
                stop_loss=StopLossRequest(stop_price=float(price) * 0.99), #1% stop loss
                time_in_force=TimeInForce.DAY
            )
            market_order = trading_client.submit_order(market_order_data)
    elif len(portfolio) > 0:
        print("you have one position ")
        if price >= SMAlatest_data_point['sma']:
            trading_client.close_all_positions()


    time.sleep(5)








    # print(df[['close', 'upper_band', 'lower_band']])
    # print(latest_data_point)





    # delta =SMAdf['close'].diff()
    # print(df.columns)
    # gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    # loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    # rs = gain / loss
    # rsi = 100 - (100 / (1 + rs))
    #SMAdf['RSI'] = rsi
    # latest_data_point =SMAdf.iloc[-1]


    # print(latest_data_point["RSI"])
    # print(rsi)
    #  print(df.head())

    time.sleep(30)  # Sleep for 5 seconds

