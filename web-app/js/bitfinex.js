class bitfinex_socket extends WebSocket
{
    create_subscription_message(currency, channel)
    {
        return JSON.stringify
        ({
            event: 'subscribe',
            channel: channel,
            symbol: 't' + currency + 'USD'
        });
    }

    subscribe(currency)
    {
        let ticker_subscription_message = this.create_subscription_message(currency, 'ticker');
        let trades_subscription_message = this.create_subscription_message(currency, 'trades');

        if(this.readyState != 1)
        {
            this.awaiting_subs.push(ticker_subscription_message);
            this.awaiting_subs.push(trades_subscription_message);
        }
        else
        {
            this.awaiting_subs.forEach((sub) => { this.send(sub); });
            this.awaiting_subs = null;
            this.send(ticker_subscription_message);
            this.send(trades_subscription_message);
        }
    }

    // constructor(currency)
    constructor(currency)
    {
        super('wss://api-pub.bitfinex.com/ws/2');

        this.data = {ticker: {}, trades: {}};
        this.channels = {};
        this.awaiting_subs = [];

        this.onopen = function(event) { this.subscribe(currency) };

        this.onmessage = function(event)
        {
            let cur_data = JSON.parse(event.data);

            if (cur_data.event === "subscribed")
            {
                let symbol = cur_data.symbol.substring(1, 4);
                let channel = cur_data.channel;
                let chanId = cur_data.chanId;

                this.channels[chanId.toString()] = [channel, symbol];
                this.data[channel][symbol] = {};
                // this.data[channel][chanId.toString()] = {currency: symbol};

                // target.innerHTML += "<h4>" + symbol + " " + channel + " [" + chanId + "]</h4>";

                // let pre = document.createElement('pre');
                // pre.id = chanId;
                // target.appendChild(pre);
            }
            else if (cur_data[0] && Object.keys(this.channels).includes(cur_data[0].toString()))
            {
                // var out = "";
                let currency = this.channels[cur_data[0].toString()][1];

                if (this.channels[cur_data[0].toString()][0] === "ticker")
                {
                    if(cur_data[1][0] === "h" || cur_data[1][1] === "b") return;

                    let current = this.data.ticker[currency];
                    current.bid_price = cur_data[1][0];
                    current.bid_amount = cur_data[1][1];
                    current.ask_price = cur_data[1][2];
                    current.ask_amount = cur_data[1][3];

                    // out = "BID: " + current.bid_price + " &times " + current.bid_amount;
                    // out += "\nASK: " + current.ask_price + " &times " + current.ask_amount;
                }
                else
                {
                    let current = this.data.trades[currency];

                    if(cur_data[1] === "hb") return;
                    else if (cur_data[1] === "tu")
                    {
                        if(Array.isArray(cur_data[2][0]))
                        {
                            current.price = cur_data[2][0][3];
                            current.amount = cur_data[2][0][2];
                        }
                        else
                        {
                            current.price = cur_data[2][3];
                            current.amount  = cur_data[2][2];
                        }
                    }
                    else if(Array.isArray(cur_data[1][0]))
                    {
                        current.price = cur_data[1][0][3];
                        current.amount  = cur_data[1][0][2];
                    }
                    else
                    {
                        current.price = cur_data[1][3];
                        current.amount  = cur_data[1][2];
                    }

                    // out = "PRICE: " + current.price + "\nAMOUNT: " + current.amount;
                }

                // document.getElementById(cur_data[0].toString()).innerHTML = out;
            }
        };
    }
};
