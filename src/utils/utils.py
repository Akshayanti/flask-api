from google.protobuf import json_format

from protobuffs import transactions_pb2


def get_enum_value_from_name(input_symbol):
    new_dict = {
        "TWLO":  transactions_pb2.Stock.Symbol.TWILIO,
        "AAPL":  transactions_pb2.Stock.Symbol.APPLE,
        "AMZN":  transactions_pb2.Stock.Symbol.AMAZON,
        "GOOGL": transactions_pb2.Stock.Symbol.GOOGLE,
        "MSFT":  transactions_pb2.Stock.Symbol.MICROSOFT,
        "BARC":  transactions_pb2.Stock.Symbol.BARCLAYS,
        "IBM":   transactions_pb2.Stock.Symbol.IBM,
        "MET":   transactions_pb2.Stock.Symbol.METLIFE,
        "PHIA":  transactions_pb2.Stock.Symbol.PHILIPS,
        "PM":    transactions_pb2.Stock.Symbol.PHILIP_MORRIS,
        "UPS":   transactions_pb2.Stock.Symbol.UPS,
        "AMD":   transactions_pb2.Stock.Symbol.AMD,
        "HON":   transactions_pb2.Stock.Symbol.HONEYWELL,
        "MA":    transactions_pb2.Stock.Symbol.MASTERCARD,
        "MSI":   transactions_pb2.Stock.Symbol.MSI,
        "NVDA":  transactions_pb2.Stock.Symbol.NVIDIA,
        "PSTG":  transactions_pb2.Stock.Symbol.PURE_STORAGE,
        "S":     transactions_pb2.Stock.Symbol.SENTINEL_ONE,
        "SPLK":  transactions_pb2.Stock.Symbol.SPLUNK,
        "V":     transactions_pb2.Stock.Symbol.VISA,
        "CAT":   transactions_pb2.Stock.Symbol.CATERPILLAR,
        "CL":    transactions_pb2.Stock.Symbol.COLGATE,
        "FDX":   transactions_pb2.Stock.Symbol.FEDEX,
        "GE":    transactions_pb2.Stock.Symbol.GENERAL_ELECTRIC,
        "JNJ":   transactions_pb2.Stock.Symbol.JOHNSON,
        "MRK":   transactions_pb2.Stock.Symbol.MERK,
        "PEP":   transactions_pb2.Stock.Symbol.PEPSI,
        "PG":    transactions_pb2.Stock.Symbol.PROCTOR_AND_GAMBLE,
        "SBUX":  transactions_pb2.Stock.Symbol.STARBUCKS,
        "SCHW":  transactions_pb2.Stock.Symbol.SCHWAB,
        "SHEL":  transactions_pb2.Stock.Symbol.SHELL,
        "BP":    transactions_pb2.Stock.Symbol.BP,
        "PBR":   transactions_pb2.Stock.Symbol.PETROLEO_BRASILEIRO,
        "VOW":   transactions_pb2.Stock.Symbol.VOLKSWAGEN,
        "CSCO":  transactions_pb2.Stock.Symbol.CISCO,
        "ASTR":  transactions_pb2.Stock.Symbol.ASTRA_SPACE,
        "SPCE":  transactions_pb2.Stock.Symbol.VIRGIN_GALACTIC_SPACE
    }
    if input_symbol in new_dict:
        return new_dict[input_symbol]
    else:
        return transactions_pb2.Stock.Symbol.UNKNOWN


def get_stock_of_interest_from_message(parent, use_integers_for_enums, search_key):
    stock_name = search_key.split(".")[0].upper()
    stock_enum = get_enum_value_from_name(stock_name)
    if stock_enum != -1:
        for x in json_format.MessageToDict(message=parent,
                                           use_integers_for_enums=use_integers_for_enums)['stock']:
            if x['symbol'] == stock_enum:
                return x
    return None
