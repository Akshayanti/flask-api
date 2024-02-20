import json

import pytest

from index import app

valid_buy_sell_nvidia = {
    "stock_symbol":   "NVDA",
    "price_per_unit": 1000,
    "units":          20
}

valid_buy_sell_barclays = {
    "stock_symbol":   "BARC.L",
    "price_per_unit": 1000,
    "units":          20
}

status_200_msg = {"code": 200, "msg": "ok"}
status_404_msg = {"code": 404, "msg": "Requested resource was Not Found"}

test_client = app.test_client()


@pytest.mark.buy_request
def test_buy_valid_stock_returns_200():
    response = test_client.post('/buy', json=valid_buy_sell_nvidia)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    assert response.json == status_200_msg


@pytest.mark.buy_request
@pytest.mark.parametrize(('input_json'), (
        ({"stock_symbol": "NVDA", "price_per_unit": -1000, "units": 10}),
        ({"stock_symbol": "NVDA", "price_per_unit": 1000, "units": -10})
))
def test_buy_invalid_value_returns_400(input_json):
    response = test_client.post('/buy', json=input_json)
    assert response.content_type == 'application/json'
    assert response.status_code == 422
    assert response.json[0]["msg"] == "Input should be greater than 0"


@pytest.mark.buy_request
def test_buy_invalid_stock_returns_404():
    buy_body = {
        "stock_symbol":   "NVDAAAAAAAAAAAAAAA",
        "price_per_unit": 1000,
        "units":          10
    }
    response = test_client.post('/buy', json=buy_body)
    assert response.content_type == 'application/json'
    assert response.status_code == 404
    assert response.json == status_404_msg


@pytest.mark.get_all
def test_get_all_returns_200():
    test_client.post('/buy', json=valid_buy_sell_barclays)
    test_client.post('/buy', json={
        "stock_symbol":   "nvda",
        "price_per_unit": 2000,
        "units":          20
    })
    test_client.post('/buy', json={
        "stock_symbol":   "barc",
        "price_per_unit": 2000,
        "units":          20
    })
    
    response = test_client.get('/stocks/all')
    data = json.loads(response.data.decode('utf-8'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {'price': 1500.0, 'qty': 40.0, 'symbol': 'NVIDIA'} in response.json
    assert {'price': 1500.0, 'qty': 40.0, 'symbol': 'BARCLAYS'} in data


@pytest.mark.get_specific
@pytest.mark.parametrize(('symbol1', 'symbol2', 'input_json'), (
        ('nvda', 'NVDA', {'price': 1500.0, 'qty': 40.0, 'symbol': 'NVDA'}),
        ('barc.l', 'BARC.L', {'price': 1500.0, 'qty': 40.0, 'symbol': 'BARC.L'}),
        ('barc', 'BARC', {'price': 1500.0, 'qty': 40.0, 'symbol': 'BARC'}),
))
def test_get_valid_returns_200(symbol1, symbol2, input_json):
    response1 = test_client.get(f'/stock/{symbol1}')
    response2 = test_client.get(f'/stock/{symbol2}')
    assert response1.content_type == response2.content_type == "application/json"
    assert response1.status_code == response2.status_code == 200
    assert response1.json == response2.json == input_json


@pytest.mark.get_specific
def test_get_invalid_returns_404():
    response = test_client.get('/stock/barcl')
    assert response.status_code == 404
    assert response.json == status_404_msg


@pytest.mark.sell_request
@pytest.mark.parametrize(('body', 'symbol', 'result'), (
        (valid_buy_sell_nvidia, 'nvda', {"symbol": "NVDA", "price": 2000.0, "qty": 20.0}),
        (valid_buy_sell_barclays, 'barc', {"symbol": "BARC", "price": 2000.0, "qty": 20.0})
))
def test_sell_valid_returns_200(body, symbol, result):
    sell_response = test_client.post('/sell', json=body)
    assert sell_response.status_code == 200
    assert sell_response.content_type == "application/json"
    assert sell_response.json == status_200_msg
    
    get_response = test_client.get(f'/stock/{symbol}')
    assert get_response.status_code == 200
    assert get_response.content_type == "application/json"
    assert get_response.json == result


@pytest.mark.sell_request
@pytest.mark.parametrize(('body'), (
        ({"stock_symbol": "NVDA", "price_per_unit": 2000.0, "units": 200000.0}),
        ({"stock_symbol": "BARC", "price_per_unit": 2000.0, "units": 200000.0})
))
def test_sell_more_than_held_returns_400(body):
    response = test_client.post('/sell', json=body)
    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.json == {"code": 400, "msg": "Cannot sell more than held units"}


@pytest.mark.sell_request
@pytest.mark.parametrize(('body'), (
        ({"stock_symbol": "NVDAAAAAAAAAAAAA", "price_per_unit": 2000.0, "units": 200000.0}),
        ({"stock_symbol": "TWLO", "price_per_unit": 2000.0, "units": 200000.0})
))
def test_sell_unknown__or_non_portfolio_stock_returns_404(body):
    response = test_client.post('/sell', json=body)
    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.json == status_404_msg
