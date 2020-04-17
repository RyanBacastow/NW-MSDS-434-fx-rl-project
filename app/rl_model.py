import yfinance as yf
import os
import sys
import datetime
import logging
import matplotlib.pyplot as plt
import json
import gym
import gym_anytrading

curr_pairs = {
"EUR/USD":"EURUSD=X",
"USD/JPY":"JPY=X",
"GBP/USD":"GBPUSD=X",
"AUD/USD":"AUDUSD=X",
"NZD/USD":"NZDUSD=X",
"GBP/JPY":"GBPJPY=X",
"EUR/GBP":"EURGBP=X",
"EUR/CAD":"EURCAD=X",
"EUR/SEK":"EURSEK=X",
"EUR/CHF":"EURCHF=X",
"EUR/HUF":"EURHUF=X",
"EUR/JPY":"EURJPY=X",
"USD/CNY":"CNY=X",
"USD/HKD":"HKD=X",
"USD/SGD":"SGD=X",
"USD/INR":"INR=X",
"USD/MXN":"MXN=X",
"USD/PHP":"PHP=X",
"USD/IDR":"IDR=X",
"USD/THB":"THB=X",
"USD/MYR":"MYR=X",
"USD/ZAR":"ZAR=X",
"USD/RUB":"RUB=X"
}

logger = logging.getLogger('rl_model')
logging.basicConfig(level=logging.INFO)

# os.environ['ALPHAVANTAGE_API_KEY'] = '95O0QW8Y4UM8U9WA'
# os.environ['CURR_PAIR'] = "EUR/USD"
# os.environ['WINDOW_SIZE'] = "100"
# os.environ['PERIOD'] = "7d"
# os.environ['INTERVAL'] = "1m"

#Periods are key = time that will go into yfinance call, value = amount of that will be set as default window_size
periods = ["1d",
           "5d",
           "1mo",
           "3mo",
           "6mo",
           "1y",
           "2y",
           "5y",
           "10y",
           "ytd",
           "max"
           ]


def main(curr_pair="EUR/USD", period="1y", interval="1h", window_size=1, unit_side='left'):
    """
    :param curr_pair: str: Choose from the list of valid trading pairs seen in curr_pairs dict object. Not case sensitive.
    :param period: str: Valid period strings user can choose from are in the period object.
    :param interval: str: Valid pairing of interval given period. Max period for 1 minute interval is 7d.
    :param window_size: str: amount of data that should be considered for making decisions.
    :param unit_side: str: which side of the pair should be the one denominating the results.
    :return: info: dict: dictionary with returns and model information.
    """
    logger.info("curr_pair: {}".format(curr_pair))
    logger.info("period: {}".format(period))
    logger.info("interval: {}".format(interval))
    logger.info("window_size: {}".format(window_size))

    curr = yf.Ticker(curr_pairs[curr_pair.upper()])
    # This will be a configurable call in custom function
    df = curr.history(period=period, interval=interval, )
    df = df[["Open", "High", "Low", "Close"]]
    # Data cleaning, not totally necessary.
    df.index.rename('Time', inplace=True)
    df.reset_index(inplace=True)
    df['Time'] = df['Time'].dt.tz_localize(None)
    df.set_index('Time', inplace=True)

    logger.info("\nData start Time: {}".format(str(min(df.index))))
    logger.info("\nData end Time: {}".format(str(max(df.index))))

    env = gym.make('forex-v0', df=df, window_size=window_size, frame_bound=(window_size, df.shape[0]), unit_side=unit_side)
    env.reset()
    i = 0
    while True:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if i % window_size == 0:
            logger.info("Model info at end of observation {}: {}".format(str(i), json.dumps(info)))
        i += 1
        if done:
            logger.info("Final model info: {}".format(json.dumps(info)))
            break

    plt.cla()
    env.render_all()
    plt.savefig("model_output/rl_model_output_{curr_pair}_{utc_datetime}.png".format(
                curr_pair=curr_pair.split("/")[0] + "_" + curr_pair.split("/")[1],
                utc_datetime=datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")))
    return info


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print("Running model with default settings.")
        main()
