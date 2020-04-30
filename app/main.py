# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, jsonify, request, render_template, url_for
# from google.cloud import storage
import pickle
import os
import numpy as np
import yfinance as yf
import datetime
import logging
import matplotlib.pyplot as plt
import json
import gym
import gym_anytrading

app = Flask(__name__,
            static_folder='./static',
            template_folder="./templates")

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.


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
    logger.info("curr_pair: %s", curr_pair)
    logger.info("period: %s", period)
    logger.info("interval: %s", interval)
    logger.info("window_size: %s", window_size)

    curr = yf.Ticker(curr_pairs[curr_pair.upper()])
    # This will be a configurable call in custom function
    df = curr.history(period=period, interval=interval, )
    df = df[["Open", "High", "Low", "Close"]]
    # Data cleaning, not totally necessary.
    df.index.rename('Time', inplace=True)
    df.reset_index(inplace=True)
    df['Time'] = df['Time'].dt.tz_localize(None)
    df.set_index('Time', inplace=True)

    logger.info("\nData start Time: %s", str(min(df.index)))
    logger.info("\nData end Time: %s", str(max(df.index)))

    env = gym.make('forex-v0', df=df, window_size=window_size, frame_bound=(window_size, df.shape[0]), unit_side=unit_side)
    env.reset()
    i = 0
    while True:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if i % window_size == 0:
            logger.info("Model info at end of observation %s: %s", str(i), json.dumps(info))
        i += 1
        if done:
            logger.info("Final model info: %s", json.dumps(info))
            break

    plt.cla()
    env.render_all()
    plt.savefig("app/model_output/rl_model_output_{curr_pair}_{utc_datetime}.png".format(
                curr_pair=curr_pair.split("/")[0] + "_" + curr_pair.split("/")[1],
                utc_datetime=datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")))
    return info


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    currency_pair = request.form["currency_pair"]
    period = request.form["period"]
    interval = request.form["interval"]
    window_size = request.form["window_size"]

    return f"Running on {currency_pair}, over {period} of data in {interval} intervals with {window_size} window_size"


@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/name/<value>')
def name(value):
    val = {"value": value}
    return jsonify(val)


@app.route('/params', methods=['POST'])
def run_model():
    req_data = request.get_json()
    return req_data

@app.route('/dir')
def dir():
    files = os.listdir()
    return jsonify(files)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
