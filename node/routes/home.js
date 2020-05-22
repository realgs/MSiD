var request = require('request');
var async = require('async');

exports.get = function (req, res) {
    async.parallel({
        cex: (callback) => {
            request.get('https://cex.io/api/order_book/BTC/USD/', (err, resp, body) => {
                if (err) console.log(err);

                callback(null, JSON.parse(resp.body));
            })
        },
        bitstamp: (callback) => {
            request.get('https://www.bitstamp.net/api/order_book/btcusd', (err, resp, body) => {
                if (err) console.log(err);

                callback(null, JSON.parse(resp.body));
            })
        },
        bittrex: (callback) => {
            request.get('https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both', (err, resp, body) => {
                if (err) console.log(err);

                callback(null, JSON.parse(resp.body));
            })
        },
        bitbay: (callback) => {
            request.get('https://bitbay.net/API/Public/BTC/orderbook.json', (err, resp, body) => {
                if (err) console.log(err);

                callback(null, JSON.parse(resp.body));
            })
        }
    }, (err, result) => {
        console.log(typeof result);

        res.send(result);
    })
}