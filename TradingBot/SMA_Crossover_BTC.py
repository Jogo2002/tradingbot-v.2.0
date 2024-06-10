import Bootstrapper
from Bootstrapper import *
trading_client = TradingClient(Bootstrapper.API_KEY, Bootstrapper.SECRET_KEY, paper=True)

client = CryptoHistoricalDataClient()

# Get today's date
end = datetime.now()

load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv('PKRZUU58WZP1YJ9KKPU7')
SECRET_KEY = os.getenv('rZtc2vlTGIFK5txaaHgCyBFxDfkfo5mdzlHJJDKA')

trading_client = TradingClient('PKRZUU58WZP1YJ9KKPU7', 'rZtc2vlTGIFK5txaaHgCyBFxDfkfo5mdzlHJJDKA', paper=True)


while True:
    url = "https://paper-api.alpaca.markets/v2/account"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "PKRZUU58WZP1YJ9KKPU7",
        "APCA-API-SECRET-KEY": "rZtc2vlTGIFK5txaaHgCyBFxDfkfo5mdzlHJJDKA"
    }

    response = requests.get(url, headers=headers)

    print(response.text)
    print(type(requests))



    portfolio = trading_client.get_all_positions()

    end = datetime.now()
    start = end - timedelta(days=2)

    # Fetch fresh data inside the loop
    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
        start=start,
        end=end,
        time_in_force=TimeInForce.GTC
    )
    client = CryptoHistoricalDataClient()
    bars = client.get_crypto_bars(request_params)
    df = bars.df


    # Calculate moving averages and RSI
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    delta = df['close'].diff()


    # Define the signal
    df['Signal'] = 0.0
    df.loc[df['SMA_20'] > df['SMA_50'], 'Signal'] = 1.0
    df.loc[df['SMA_20'] < df['SMA_50'], 'Signal'] = -1.0
    latest_data_point = df.iloc[-1]

#   print(bars)
    print("SMA_50:", latest_data_point['SMA_50'])
    print("SMA_20:", latest_data_point['SMA_20'])

    # Check for trading signals and execute orders accordingly
    if latest_data_point['SMA_20'] > latest_data_point['SMA_50']: #check condition
        print("Buy signal: The 20-minute moving average has crossed above the 50-minute moving average.")
        market_order_data = MarketOrderRequest(
            symbol="BTCUSD",
            notional=300, #$300
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC #Good 'Till Cancelled order type
        )
        market_order = trading_client.submit_order(market_order_data)
    elif latest_data_point['SMA_20'] < latest_data_point['SMA_50']:
        print("Sell signal: The 20-minute moving average has crossed below the 50-minute moving average.")
        market_order_data = MarketOrderRequest(
            symbol="BTCUSD",
            notional=300, #$300
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC #Good 'Till Cancelled order type
        )
        market_order = trading_client.submit_order(market_order_data)


    time.sleep(70)  # Sleep for 70 seconds


