from src.protobuffs import transactions_pb2
from utils import utils

msg = transactions_pb2.Transactions()
stock1 = transactions_pb2.Stock()
stock1.symbol = 5
stock1.qty = 15
stock1.price = 100

stock2 = transactions_pb2.Stock()
stock2.symbol = 1
stock2.qty = 150
stock2.price = 1_000

msg.stock.extend([stock1, stock2])


def test_stock_is_fetched_properly_with_correct_case():
    actual = utils.get_stock_of_interest_from_message(parent=msg,
                                                      use_integers_for_enums=True,
                                                      search_key="AAPL")
    expected = {'symbol': 1, 'price': 1000.0, 'qty': 150.0}
    assert actual == expected


def test_stock_is_fetched_properly_regardless_of_currency():
    actual = utils.get_stock_of_interest_from_message(parent=msg,
                                                      use_integers_for_enums=True,
                                                      search_key="BARC.L")
    expected = {'symbol': 5, 'price': 100.0, 'qty': 15.0}
    assert actual == expected


def test_stock_is_fetched_properly_with_incorrect_case():
    actual = utils.get_stock_of_interest_from_message(parent=msg,
                                                      use_integers_for_enums=True,
                                                      search_key="aapl")
    expected = {'symbol': 1, 'price': 1000.0, 'qty': 150.0}
    assert actual == expected


def test_no_fetch_when_wrong_symbol():
    assert utils.get_stock_of_interest_from_message(parent=msg,
                                                    use_integers_for_enums=True,
                                                    search_key="TWLO") is None
    assert utils.get_stock_of_interest_from_message(parent=msg,
                                                    use_integers_for_enums=True,
                                                    search_key="GOOGLE") is None
