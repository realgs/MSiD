fee = 0.002


def avg(data):
    sum = 0
    for item in data:
        sum += item
    return sum / len(data)


def decide_if_buy_or_sell(data, current_value):
    avg_val = avg(data)
    #buy if value of currency is less than avg value + fee you would get from it
    if current_value < avg_val + avg_val * fee:
        return 'BUY'
    # sell if value of currency is greater than avg value + fee you would get from it
    elif current_value > avg_val + avg_val * fee:
        return 'SELL'
    else:
        return None


def get_diff_percent(data, current_price):
    diff = current_price - avg(data)
    if diff < 0:
        return -diff / 100
    else:
        return diff / 100
