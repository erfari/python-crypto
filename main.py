import datetime as dt
import backtrader as bt
import pandas as pd
from backtrader_binance import BinanceStore
from config import Config
from strategy import StrategySaveOHLCVToDF

# Торговая система



# Исторические/новые бары тикера
if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    cerebro = bt.Cerebro(quicknotify=True)

    coin_target = 'USDT'  # базовый тикер, в котором будут осуществляться расчеты
    symbol = 'BTC' + coin_target  # тикер, по которому будем получать данные в формате <КодТикераБазовыйТикер>

    store = BinanceStore(
        api_key=Config.BINANCE_API_KEY,
        api_secret=Config.BINANCE_API_SECRET,
        coin_target=coin_target,
        testnet=False)  # Хранилище Binance
    broker = store.getbroker()
    cerebro.setbroker(broker)

    # 1. Исторические D1 бары за 365 дней + График т.к. оффлайн/ таймфрейм D1
    from_date = dt.datetime.utcnow() - dt.timedelta(days=365)  # берем данные за 365 дней от текущего времени
    data = store.getdata(timeframe=bt.TimeFrame.Days, compression=1, dataname=symbol, start_date=from_date, LiveBars=False)

    cerebro.adddata(data)  # Добавляем данные
    cerebro.addstrategy(StrategySaveOHLCVToDF, coin_target=coin_target)  # Добавляем торговую систему
  
    results = cerebro.run()  # Запуск торговой системы

    print(results[0].df)

    df = pd.DataFrame(results[0].df[symbol], columns=["datetime", "open", "high", "low", "close", "volume"])
    print(df)

    tf = results[0].df_tf[symbol]

    # save to file
    df.to_csv(f"{symbol}_{tf}.csv", index=False)

    # save to file
    df[:-5].to_csv(f"{symbol}_{tf}_minus_5_days.csv", index=False)

    cerebro.plot()  # Рисуем график