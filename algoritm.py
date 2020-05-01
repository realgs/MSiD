
fee = 0.002

def avg(data):
    sum = 0
    for item in data:
        sum += item
    return sum / len(data)


def decide_if_buy_or_sell(data, current_price):
    diff = current_price - avg(data)
    if  current_price < avg(data) + current_price * fee:
        return 'BUY'
    elif current_price > avg(data) + current_price * fee:
        return 'SELL'
    else:
        return None
