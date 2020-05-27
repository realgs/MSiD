var request = require('request')
var async = require('async')
var schedule = require('node-schedule')

exports.get = (req, res) => {
    var cash = 1000
    
    var s = schedule.scheduleJob('10 * * * *', function() {
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
            function findFinance (bids, asks, nameBids, nameAsks) {
                var sum = 0
                var itog = 0

                for (var i = 0; i < bids.length; i++) {
                    for (var j = 0; j < asks.length; j++) {
                        var percent = bids[i][0] * 0.10

                        if (bids[i][1] == asks[j][1] &&  bids[i][0] + percent < asks[j][0] && cash > bids[i][0]) {
                            itog += (asks[j][0] - (bids[i][0] + percent))
                            sum++
                            cash += asks[j][0] - (bids[i][0] + percent)
                        
                            console.log("Na miejsce " + nameBids + " mozna kupic " + bids[i][1] + " za " + (bids[i][0] + percent) + 
                            " i sprzedac na " + nameAsks + " za " + asks[j][0] + " i otrzymac " + (asks[j][0] - bids[i][0]))

                            bids[i] = "bougth"
                            asks[j] = "sold"                        
                            
                            break
                        }
                    }
                }

                console.log(itog + " | " + sum)
                return itog
            }

            var cbb = findFinance(result.cex.bids, result.bitbay.asks, "cex", "bitbay")
            var cbts = findFinance(result.cex.bids, result.bitstamp.asks, "cex", "bitstamp")
            var cbtt = findFinance(result.cex.bids, result.bittrex.asks, "cex", "bittrex")
            var btsbtt = findFinance(result.bitstamp.bids, result.bittrex.asks, "bitstamp", "bittrex")
            var bbbts = findFinance(result.bitbay.bids, result.bitstamp.asks, "bitbay", "bitstamp")
            var bttbb = findFinance(result.bittrex.bids, result.bitbay.asks, "bittrex", "bitbay")

            res.send(result)
        })
    });
}