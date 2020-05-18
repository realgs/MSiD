#!/usr/bin/env python3

HOST='0.0.0.0'
PORT=80
DEBUG_PORT=8099

import os
import json
from flask import Flask, render_template, Response, request, redirect, url_for
from app.data_gatherer import gather_data
from app.trader import simulate
import app.data as data
from app.config import INITIAL_WALLET, CURRENCIES, MARKETS
from threading import Thread

app = Flask(__name__)

@app.route("/")
def main():
    if wallet_empty():
        page = render_template('wallet_init.html', initial_wallet=INITIAL_WALLET)
    else:
        page = render_template('main_view.html', wallet=data.get_wallet())
    return page

@app.route("/init_wallet", methods=['POST'])
def init_wallet():
    curr_val_map = {}
    for currency in CURRENCIES:
        curr_val_map[currency] = float(request.form.get(currency))
    data.insert_into_wallet(curr_val_map)
    return redirect(url_for('main'))

@app.route("/update_wallet", methods=['POST'])
def update_wallet():
    for currency in CURRENCIES:
        data.update_in_wallet(currency, float(request.form.get(currency)))
    return redirect(url_for('main'))

@app.route("/get_wallet")
def get_wallet():
    return Response(json.dumps(data.get_wallet()), mimetype='application/json')

@app.route("/get_markets")
def get_markets():
    return Response(json.dumps(MARKETS), mimetype='application/json')

@app.route("/get_tickers/<market>")
def get_tickers(market):
    return Response(json.dumps(data.get_tickers(market)), mimetype='application/json')

def wallet_empty():
    return not bool(data.get_wallet())

if __name__ == "__main__":
    Thread(target=gather_data, daemon=True).start()
    Thread(target=simulate, daemon=True).start()

    if 'DEBUG' not in os.environ:
        app.run(host=HOST, port=PORT, debug=False)
    else:
        app.run(host=HOST, port=DEBUG_PORT, debug=True)
