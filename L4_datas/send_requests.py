import requests
import json
import math
import time
import work_with_requests.config as config

def get_parsed_list_from_request(url):
    try:
        json_obj = requests.get(url)
        parsed_list = json.loads(json_obj.text)
    except BaseException:
        time.sleep(60)
        json_obj = requests.get(url)
        parsed_list = json.loads(json_obj.text)
    return parsed_list

def equallyWithProcent(proc, firstNum, secondNum):
    return (math.fabs(firstNum/secondNum - 1) * 100 < proc)

def get_possible_profit_bitbay_sel_bittrex_buy(parsed_string_bitbay_sell, parsed_string_bittrex_buy, index):
    sell_list = parsed_string_bitbay_sell["sell"]
    buy_list = parsed_string_bittrex_buy['result']['buy']
    for sell in sell_list:
        sell_price = float(sell['ra'])
        sell_quantity = float(sell['ca'])
        for buy in buy_list:
            buy_price = float(buy['Rate'])
            buy_quantity = float(buy['Quantity'])
            if (buy_price > sell_price):
                #count_profit(sell_price, buy_price, sell_quantity, buy_quantity, index)
                count_profit_consider_take_commision(sell_price, buy_price, sell_quantity, buy_quantity, index, config.BITTBAY_SELLER_BITTREX_BUYER)

def get_possible_profit_bittrex_sell_bitbay_buy(parsed_string_bittrex_sell, parsed_string_bitbay_buy, index):
    sell_list = parsed_string_bittrex_sell['result']['sell']
    buy_list = parsed_string_bitbay_buy["buy"]
    for sell in sell_list:
        sell_price = float(sell['Rate'])
        sell_quantity = float(sell['Quantity'])
        for buy in buy_list:
            buy_price = float(buy['ra'])
            buy_quantity = float(buy['ca'])
            if (buy_price > sell_price):
                #without commision: count_profit(sell_price, buy_price, sell_quantity, buy_quantity, index)
                count_profit_consider_take_commision(sell_price, buy_price, sell_quantity, buy_quantity, index, config.BITTREX_SELLER_BITBAY_BUYER)

def get_possible_profits(define_sides, url_bittrex, url_bitbay, index):
    if(define_sides == config.BITTBAY_SELLER_BITTREX_BUYER):
        get_possible_profit_bitbay_sel_bittrex_buy(get_parsed_list_from_request(url_bitbay),get_parsed_list_from_request(url_bittrex), index)
    elif(define_sides == config.BITTREX_SELLER_BITBAY_BUYER):
        get_possible_profit_bittrex_sell_bitbay_buy(get_parsed_list_from_request(url_bittrex), get_parsed_list_from_request(url_bitbay), index)
    else:
        print("MISTAKE DATAS")

def find_profit_ofers():
    for index in config.LISTS_LENGTH_HELPER:
        get_possible_profits(config.BITTREX_SELLER_BITBAY_BUYER, config.URL_BITTREX_FIRST_P + config.LIST_BITTREX_ARGS[index] + config.URL_BITTREX_SECOND_P, config.URL_BITBAY + config.LIST_BITBAY_ARGS[index], index)
        get_possible_profits(config.BITTBAY_SELLER_BITTREX_BUYER,config.URL_BITTREX_FIRST_P + config.LIST_BITTREX_ARGS[index] + config.URL_BITTREX_SECOND_P,config.URL_BITBAY + config.LIST_BITBAY_ARGS[index], index)

def count_profit(sell_price_propos, buy_price_propos, sell_quantity, buy_quantity, index):
    result_profit = 0
    result_quantity = 0
    if (buy_quantity <= sell_quantity):
        result_quantity = buy_quantity
    else:
        result_quantity = sell_quantity
    result_profit = (buy_price_propos - sell_price_propos) * result_quantity
    print("currencies: " + config.LIST_BITBAY_ARGS[index] + "quantity: " + str(result_quantity) + "zyzk: " + str(result_profit))
    return result_profit

def count_profit_consider_take_commision(sell_price_propos, buy_price_propos, sell_quantity, buy_quantity, index, def_seller_buyer):
    if (def_seller_buyer == config.BITTBAY_SELLER_BITTREX_BUYER):
        firstCommision = config.MIN_TAKER_BITBAY
        secondCommisson = config.TAKER_BITTREX
    else:
        firstCommision = config.TAKER_BITTREX
        secondCommission = config.MIN_TAKER_BITBAY
    result_profit = 0
    result_quantity = 0
    if (buy_quantity <= sell_quantity):
        result_quantity = buy_quantity
    else:
        result_quantity = sell_quantity
    spend_by_me_price = (sell_price_propos * result_quantity) * (1 + firstCommision)
    earned_by_me_price = (1 - secondCommission) * result_quantity * buy_price_propos
    result_profit = earned_by_me_price - spend_by_me_price
    if (result_profit > 0):
        print("currencies: " + config.LIST_BITBAY_ARGS[index] + "quantity: " + str(result_quantity) + "zyzk: " + str(result_profit))
    return result_profit

if( __name__ == '__main__'):
    while(True):
        find_profit_ofers()