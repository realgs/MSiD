var request = require('request');
var async = require('async');

exports.get = function (req, res) {
    async.parallel({
        bitstamp: (callback) => {
            request.get('https://www.bitstamp.net/api/order_book/btcusd', (err, resp, body) => {
                if (err) console.log(err);

                var r = JSON.parse(resp.body);

                var bids = [];
                var asks = [];

                for (var i = 0; i < r.bids.length; i++) {
                    bids[i] = new Array(1);
                    bids[i][0] = r.bids[i][0];
                    bids[i][1] = r.bids[i][1];
                }

                for (var i = 0; i < r.asks.length; i++) {
                    asks[i] = new Array(1);
                    asks[i][0] = r.asks[i][0];
                    asks[i][1] = r.asks[i][1];
                }

                console.log("ok")

                callback(null, {
                    bids: bids,
                    asks: asks
                })
            })
        },
        bittrex: (callback) => {
            request.get('https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both', (err, resp, body) => {
                if (err) console.log(err);

                var r = JSON.parse(resp.body);

                var bids = [];
                var asks = [];

                for (var i = 0; i < r.result.buy.length; i++) {
                    bids[i] = new Array(1);
                    bids[i][0] = r.result.buy[i].Rate;
                    bids[i][1] = r.result.buy[i].Quantity;
                }

                for (var i = 0; i < r.result.sell.length; i++) {
                    asks[i] = new Array(1);
                    asks[i][0] = r.result.sell[i].Rate;
                    asks[i][1] = r.result.sell[i].Quantity;
                }

                console.log("ok")

                callback(null, {
                    bids: bids,
                    asks: asks
                })
            })
        },
        cex: (callback) => {
            request.get('https://cex.io/api/order_book/BTC/USD/', (err, resp, body) => {
                if (err) console.log(err);

                var r = JSON.parse(resp.body);

                var bids = [];
                var asks = [];

                for (var i = 0; i < r.bids.length; i++) {
                    bids[i] = new Array(1);
                    bids[i][0] = r.bids[i][0];
                    bids[i][1] = r.bids[i][1];
                }

                for (var i = 0; i < r.asks.length; i++) {
                    asks[i] = new Array(1);
                    asks[i][0] = r.asks[i][0];
                    asks[i][1] = r.asks[i][1];
                }

                callback(null, {
                    bids: bids,
                    asks: asks
                })
            })
        },
        bitbay: (callback) => {
            request.get('https://bitbay.net/API/Public/BTC/orderbook.json', (err, resp, body) => {
                if (err) console.log(err);

                var r = JSON.parse(resp.body);

                var asks = [];
                var bids = [];

                for (var i = 0; i < r.bids.length; i++) {
                    bids[i] = new Array(1);
                    bids[i][0] = r.bids[i][0];
                    bids[i][1] = r.bids[i][1];
                }

                for (var i = 0; i < r.asks.length; i++) {
                    asks[i] = new Array(1);
                    asks[i][0] = r.asks[i][0];
                    asks[i][1] = r.asks[i][1];
                }

                callback(null, {
                    bids: bids,
                    asks: asks
                })
            })
        }
    }, (err, result) => {

        res.send(result)
    })
}