from fileOperations import create_file, load_file
from apiRequest import check_if_tradable, request_order_books, list_exchanges


def display_value():
    data = load_file()
    currencies = []
    for currency in data['currencies']:
        currencies.append(currency['type'])
    order_books = request_order_books(data['exchanges'], currencies)
    if not order_books:
        return False
    for currency in data['currencies']:
        value = 0.0
        quantity = 0.0
        average = 0.0
        for order in order_books:
            if currency['type'] == order['baseSymbol']:
                for bid in order['orderBooks'][0]['orderBook']['bids']:
                    average += float(bid['price'])
                    if quantity < currency['quantity']:
                        if quantity + float(bid['quantity']) <= currency['quantity']:
                            quantity += float(bid['quantity'])
                            value += float(bid['quantity']) * float(bid['price'])
                        else:
                            quantity_buy = currency['quantity'] - quantity
                            value += quantity_buy * float(bid['price'])
                            quantity = currency['quantity']
                if quantity < currency['quantity']:
                    value += (currency['quantity'] - quantity) * average
        print(f"Value of {currency['type']} - {value:>0.6f} with a quantity of {currency['quantity']}")
    return True


def display_exchanges():
    data = load_file()
    for exchange in data['exchanges']:
        print(f"\t{exchange}")


def change_apis(apis_list):
    data = load_file()
    data['exchanges'] = []
    data['currencies'] = []
    exchanges_list = list_exchanges()
    for api in apis_list:
        for exchange in exchanges_list:
            if api.lower() == exchange['exchange']:
                data['exchanges'].append(api)
    create_file(data)


def add_currency(currency_type, quantity):
    data = load_file()
    if check_if_tradable(currency_type, data['exchanges']):
        data['currencies'].append({'type': currency_type.upper(),
                                   'quantity': quantity})
    else:
        return False
    create_file(data)
    return True


def del_currency(currency_type):
    data = load_file()
    index = -1
    for i in range(len(data['currencies'])):
        if data['currencies'][i]['type'] == currency_type.upper():
            index = i
    if index >= 0:
        del data['currencies'][index]
    create_file(data)


def modify_currency(currency_type, new_quantity):
    data = load_file()
    for i in range(len(data['currencies'])):
        if data['currencies'][i]['type'] == currency_type.upper():
            data['currencies'][i]['quantity'] = new_quantity
    create_file(data)


def display_currencies():
    data = load_file()
    for currency in data['currencies']:
        print(f"Currency type: {currency['type']} \n"
              f"\tQuantity: {currency['quantity']}")


def check_currency(currency_type):
    data = load_file()
    for currency in data['currencies']:
        if currency['type'] == currency_type.upper():
            return True
    return False
