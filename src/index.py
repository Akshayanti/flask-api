import json
import logging

from flask import Response
from flask_openapi3 import Info, OpenAPI, Tag
from google.protobuf import json_format
from google.protobuf.message import Message

from src.model.schemas import GetMultipleResponseSchema, GetParameterSchema, GetResponseSchema, \
    PostBodySchema
from src.protobuffs import transactions_pb2
from src.utils import utils

transactions: Message = transactions_pb2.Transactions()
logger = logging.getLogger("")
logging.basicConfig(level=logging.INFO)

info = Info(title="Stocks Viewer API", version="1.0.0")
app = OpenAPI(__name__, info=info)

get_stocks = Tag(name="Get Methods", description="Get All or Individual Stocks")
post_stocks = Tag(name="Post Methods", description="Buy/Sell Specific Stocks")
status_200_msg = '{"code": 200, "msg": "ok"}'
status_400_msg = '{"code": 400, "msg": "Cannot sell more than held units"}'
status_404_msg = '{"code": 404, "msg": "Requested resource was Not Found"}'
status_500_get_msg = '{"code": 500, "msg": "Unexpected error while processing the get request"}'
status_500_buy_msg = '{"code": 500, "msg": "Unexpected error while processing the buy request"}'
status_500_sale_msg = '{"code": 500, "msg": "Unexpected error while processing the sale request"}'


@app.get("/stocks/all",
         summary="Get all stocks",
         description="Get stats for all stocks",
         responses={
             200: GetMultipleResponseSchema,
             500: {"msg": "Unexpected error while processing the get request"}
         },
         tags=[get_stocks])
def get_all():
    all_stocks = json_format.MessageToDict(transactions)
    try:
        return Response(status=200, response=json.dumps(all_stocks["stock"]), content_type="application/json")
    except KeyError:
        return Response(status=200, response=json.dumps(all_stocks), content_type="application/json")
    except Exception as e:
        logger.log(level=logging.ERROR, msg=str(e))
        with open("logs.txt", "a", encoding="utf-8") as logfile:
            logfile.write(str(e))
        return Response(status=500, response=status_500_get_msg, content_type="application/json")


@app.get('/stock/<symbol>',
         summary="Get stock",
         description="Get stats for a specific stock",
         responses={
             200: GetResponseSchema,
             404: {"msg": "Requested resource was Not Found"}
         },
         tags=[get_stocks])
def get_specific_stock(path: GetParameterSchema):
    stock_of_interest = utils.get_stock_of_interest_from_message(parent=transactions,
                                                                 use_integers_for_enums=True,
                                                                 search_key=path.symbol)
    if stock_of_interest is None:
        logger.log(level=logging.INFO, msg=f"No such symbol {path.symbol}")
        return Response(status=404, response=status_404_msg, content_type="application/json")
    else:
        stock_of_interest['symbol'] = path.symbol.upper()
        return Response(status=200, response=json.dumps(stock_of_interest), content_type="application/json")


@app.post('/buy',
          summary="Buy stock",
          description="Post the details of stock to buy",
          responses={
              200: {"msg": "ok"},
              404: {"msg": "Requested resource was Not Found"},
              500: {"msg": "Unexpected error while processing the buy request"}
          },
          tags=[post_stocks])
def add_purchase(body: PostBodySchema):
    print(body.units, body.price_per_unit)
    if body.units <= 0 or body.price_per_unit <= 0.0:
        return Response(status=400, response=status_400_msg, content_type="application/json")
    try:
        existing_stock = utils.get_stock_of_interest_from_message(parent=transactions,
                                                                  use_integers_for_enums=True,
                                                                  search_key=body.stock_symbol)
        new_stock = transactions_pb2.Stock()
        symbol = utils.get_enum_value_from_name(body.stock_symbol.split(".")[0].upper())
        new_stock.symbol = symbol
        
        if existing_stock is None and symbol != 0:
            new_stock.price = body.price_per_unit
            new_stock.qty = body.units
        elif existing_stock is None and symbol == 0:
            logger.log(level=logging.INFO, msg=f"No such symbol {body.stock_symbol}")
            return Response(status=404, response=status_404_msg, content_type="application/json")
        else:
            price = existing_stock['price']
            qty = existing_stock['qty']
            
            stock_to_remove = transactions_pb2.Stock()
            stock_to_remove.symbol = symbol
            stock_to_remove.price = price
            stock_to_remove.qty = qty
            transactions.stock.remove(stock_to_remove)
            
            new_stock.qty = qty + body.units
            new_stock.price = ((price * qty) + (body.price_per_unit * body.units)) / new_stock.qty
        
        transactions.stock.extend([new_stock])
        return Response(status=200, response=status_200_msg, content_type="application/json")
    except Exception as e:
        with open("logs.txt", "a", encoding="utf-8") as logfile:
            logfile.write(str(e))
        logger.log(level=logging.ERROR, msg=str(e))
        return Response(status=500, response=status_500_buy_msg, content_type="application/json")


@app.post('/sell',
          summary="Sell stock",
          description="Post the details of stock to sell",
          responses={
              404: {"msg": "Requested resource was Not Found"},
              200: {"msg": "ok"},
              500: {"msg": "Unexpected error while processing the sale request"}
          },
          tags=[post_stocks])
def add_sale(body: PostBodySchema):
    try:
        existing_stock = utils.get_stock_of_interest_from_message(parent=transactions,
                                                                  use_integers_for_enums=True,
                                                                  search_key=body.stock_symbol)
        if existing_stock is None:
            logger.log(level=logging.INFO, msg=f"No such symbol {body.stock_symbol}")
            return Response(status=404, response=status_404_msg, content_type="application/json")
        else:
            qty = existing_stock['qty']
            if qty < body.units:
                logger.log(level=logging.ERROR, msg=f"{qty} is less than {body.units}")
                return Response(status=400, response=status_400_msg, content_type="application/json")
            symbol = existing_stock['symbol']
            price = existing_stock['price']
            
            stock_to_remove = transactions_pb2.Stock()
            stock_to_remove.symbol = symbol
            stock_to_remove.price = price
            stock_to_remove.qty = qty
            transactions.stock.remove(stock_to_remove)
            
            if qty - body.units > 0:
                new_stock = transactions_pb2.Stock()
                new_stock.symbol = symbol
                new_stock.qty = qty - body.units
                new_stock.price = ((price * qty) - (body.price_per_unit * body.units)) / new_stock.qty
                transactions.stock.extend([new_stock])
            return Response(status=200, response=status_200_msg, content_type="application/json")
    except Exception as e:
        with open("logs.txt", "a", encoding="utf-8") as logfile:
            logfile.write(str(e))
        logger.log(level=logging.ERROR, msg=str(e))
        return Response(status=500, response=status_500_sale_msg, content_type="application/json")


if __name__ == "__main__":
    app.run(debug=True)
