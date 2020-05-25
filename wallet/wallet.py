import config
import work_with_database as db
import requests
import json

def updateCurrencyByAdding():
    currency = input("input currency: ").upper()
    quantity = float(input("input quantity: "))
    if (ifExistInApi(currency)):
        db.setValueByAdding(currency, quantity)
        print("currency " + currency + " successfuly added")
    else:
        print("Wallet has no options to work with this currency. It works ONLY with CRYPTO CURRENCIES")

def setBasicCurrency():
    print("Input one currency from this: ")
    for curr in config.BASIC_CURRENCIES:
        print(curr)
    currency = input()
    if (currency.upper() in config.BASIC_CURRENCIES):
        config.basic_currency = currency
    else:
        print("Input correct currency")

def getAllMoneyInChosenCurrency():
    if not config.basic_currency.__eq__(""):
        result_sum = 0
        list_tuples_currencies_quantity = db.getListOfTuplesWithData() #[('USD', 5.0), ('BTC', 4.2)]
        for currency_quantity_pair in list_tuples_currencies_quantity:
            list_of_orders = getParsedObj(config.URL_BITBAY_ORDERBOOK + currency_quantity_pair[0] + "-" + config.basic_currency)["buy"]
            result_sum += sumInBasicCurrency(list_of_orders, float(currency_quantity_pair[1]))
        return  result_sum
    else:
        print("You need to input basic currency firstly")
        return -1

def sumInBasicCurrency(list_of_orders, quantity):
    result_sum = 0
    quantity_less = quantity #input this variables to increase readability
    index = 0
    while (quantity_less > 0):
        if(quantity_less < float(list_of_orders[index]['ca'])):
            result_sum += quantity_less * float(list_of_orders[index]['ra'])
            quantity_less = 0
        else:
            result_sum += float(list_of_orders[index]['ca']) * float(list_of_orders[index]['ra'])
            quantity_less -= float(list_of_orders[index]['ca'])
    return result_sum

def ifExistInApi(currency):
    list_of_evailable_curencies = getListofAllCurrencies()
    if (currency in list_of_evailable_curencies):
        return True
    else:
        return False

def getListofAllCurrencies():
    list_of_evailable_curencies = []
    parsed_dict = getParsedObj(config.URL_BITBAY_TICKER)['items']  # parsed to dictionary, view: {'LML-BTC':{...}, 'LTC-USD':{...}}
    for currency_group in parsed_dict:
        pair_of_currencies = currency_group.split("-")
        if not pair_of_currencies[0] in list_of_evailable_curencies:#because all first values of json are cryptocurrencies. Wallet cant save non crypto currencies because byttrex cant let you work with for ex. USD - PLN OR PLN - USD.
            list_of_evailable_curencies.append(pair_of_currencies[0])
    return list_of_evailable_curencies

def make_new_wallet():
    db.deleteDB()
    db.createDataBase()
    print("wallet successfuly added")

def getParsedObj(url):
    try:
        json_obj = requests.get(url)
        parsed_dict = json.loads(json_obj.text)
    except BaseException:
        parsed_dict = None
    return parsed_dict