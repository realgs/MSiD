class bitbay_socket extends WebSocket
{
    create_subscription_message(currency, channel)
    {
        return JSON.stringify
        ({
            "action": "subscribe-public",
            "module": "trading",
            "path": channel + "/" + currency + "-USD"
        });
    }
    create_proxy_request_message(currency, channel, request_id)
    {
        return JSON.stringify
        ({
            "requestId": request_id,
            "action": "proxy",
            "module": "trading",
            "path": channel + "/" + currency + "-USD"
        });
    }

    subscribe(currency)
    {
        let orders_subscription_message = this.create_subscription_message(currency, 'orderbook');
        let transactions_subscription_message = this.create_subscription_message(currency, 'transactions');
        let orders_request_message = this.create_proxy_request_message(currency, 'orderbook', this.current_code++);
        let transactions_request_message = this.create_proxy_request_message(currency, 'transactions', this.current_code++);

        this.request_codes.push(currency);
        this.request_codes.push(currency);

        if(this.readyState != 1)
        {
            this.awaiting_subs.push(orders_subscription_message);
            this.awaiting_subs.push(transactions_subscription_message);
            this.awaiting_subs.push(orders_request_message);
            this.awaiting_subs.push(transactions_request_message);
        }
        else
        {
            this.awaiting_subs.forEach((sub) => { this.send(sub); });
            this.awaiting_subs = null;
            this.send(orders_subscription_message);
            this.send(transactions_subscription_message);
            this.send(orders_request_message);
            this.send(transactions_request_message);
        }
    }

    constructor(currency)
    {
        super('wss://api.bitbay.net/websocket/');

        this.data = {ticker: {}, trades: {}};
        this.awaiting_subs = [];
        this.request_codes = [];
        this.current_code = 0;

        this.onopen = function(event) { this.subscribe(currency) };

        this.onmessage = function(event)
        {
            let cur_data = JSON.parse(event.data);

            if (cur_data.action === "subscribe-public-confirm")
            {
                let path = cur_data.path.split('/');
                let symbol = path[1].substr(0, 3).toUpperCase();;
                let channel = path[0] === "orderbook" ? "ticker" : "trades";

                this.data[channel][symbol] = {};

                // target2.innerHTML += "<h4>" + symbol + " " + channel + "</h4>";
                //
                // let pre = document.createElement('pre');
                // pre.id = cur_data.path;
                // target2.appendChild(pre);
            }
            else if (cur_data.action === "push")
            {
                let topic = cur_data.topic.split('/');
                let currency = topic[2].substr(0, 3).toUpperCase();
                // let out = "";
                if(topic[1] === "orderbook")
                {
                    let current = this.data.ticker[currency];

                    cur_data.message.changes.forEach((item) =>
                    {
                        if(item.entryType === "Buy" && item.action === "update" && item.state)
                        {
                            current.bid_price = item.state.ra;
                            current.bid_amount = item.state.ca;
                        }
                        else if(item === "Sell" && item.action === "update" && item.state)
                        {
                            current.ask_price = item.state.ra;
                            current.amount = item.state.ca;
                        }
                    });

                    // out = "BID: " + current.bid_price + " &times " + current.bid_amount;
                    // out += "\nASK: " + current.ask_price + " &times " + current.amount;
                }
                else if(topic[1] === "transcations")
                {
                    let current = this.data.trades[currency];

                    current.price = cur_data.message.transcations[0].r;
                    current.amount = cur_data.message.transcations[0].a;

                    // out = "PRICE: " + current.price + "\nAMOUNT: " + current.amount;
                }
                // document.getElementById(topic[1] + "/" + topic[2]).innerHTML = out;
            }
            else if(cur_data.action === "proxy-response")
            {
                // let out = "";
                let currency = this.request_codes[cur_data.requestId];

                if(cur_data.body.items)
                {
                    let current = this.data.trades[currency];
                    current.price = cur_data.body.items[0].r;
                    current.amount = cur_data.body.items[0].a;

                    // out = "PRICE: " + current.price + "\nAMOUNT: " + current.amount;
                    // document.getElementById("transactions/" + currency.toLowerCase() + "-usd").innerHTML = out;
                }
                else(cur_data.body.buy && cur_data.body.sell && Array.isArray(cur_data.body.buy) && Array.isArray(cur_data.body.sell))
                {
                    let current = this.data.ticker[currency];

                    current.bid_price = cur_data.body.buy[0].ra;
                    current.bid_amount = cur_data.body.buy[0].ca;

                    current.ask_price = cur_data.body.sell[0].ra;
                    current.amount = cur_data.body.sell[0].ca;

                    // out = "BID: " + current.bid_price + " &times " + current.bid_amount;
                    // out += "\nASK: " + current.ask_price + " &times " + current.amount ;
                    // document.getElementById("orderbook/" + currency.toLowerCase() + "-usd").innerHTML = out;
                }
            }
        };
    }
};
