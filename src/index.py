import json

from flask import Response
from flask_openapi3 import Info, OpenAPI, Tag
from google.protobuf import json_format
from google.protobuf.message import Message

from src.model.schemas import GetMultipleResponseSchema, GetParameterSchema, GetResponseSchema, \
    PostBodySchema
from src.protobuffs import transactions_pb2
from src.utils import utils

transactions: Message = transactions_pb2.Transactions()

info = Info(title="Stocks Viewer API", version="1.0.0")
app = OpenAPI(__name__, info=info)

get_stocks = Tag(name="Get Methods", description="Get All Stocks")
post_stocks = Tag(name="Post Methods", description="Post Specific Stocks")


@app.get("/stocks/all",
         summary="Get all stocks",
         description="Get stats for all stocks",
         responses={200: GetMultipleResponseSchema},
         tags=[get_stocks])
def get_all():
    all_stocks = json_format.MessageToDict(transactions)['stock']
    return json.dumps(all_stocks)


@app.get('/stock/<symbol>',
         summary="Get stock",
         description="Get stats for a specific stock",
         responses={200: GetResponseSchema, 404: {}},
         tags=[get_stocks])
def get_specific_stock(path: GetParameterSchema):
    stock_of_interest = utils.get_stock_of_interest_from_message(parent=transactions,
                                                                 use_integers_for_enums=True,
                                                                 search_key=path.symbol)
    if stock_of_interest is None:
        return Response("Status Code 404: Symbol not in portfolio\n", status=404)
    else:
        stock_of_interest['symbol'] = path.symbol
        return json.dumps(stock_of_interest)


@app.post('/buy',
          summary="Purchase stock",
          description="Post the details of stock to buy",
          responses={
              404: {},
              200: {},
              500: {}
          },
          tags=[post_stocks])
def add_purchase(body: PostBodySchema):
    try:
        existing_stock = utils.get_stock_of_interest_from_message(parent=transactions,
                                                                  use_integers_for_enums=False,
                                                                  search_key=body.stock_symbol)
        if existing_stock is None:
            new_stock = transactions_pb2.Stock()
            stock1.price = 12
            stock1.symbol = 15
            stock1.qty = 15
            # add stock for the thingy and add it to transactions
            pass
        else:
            # do some calculations here
            pass
        return Response("ok\n", status=200)
    except Exception:
        return Response("Unexpected error while processing the purchase request\n", status=500)
        # stock.buy_units(units=body.units, price=body.price_per_unit)


# @app.post('/sell',
#           summary="Sell stock",
#           description="Post the details of stock to sell",
#           responses={
#               404: {"msg": "Requested Resource was Not Found\n"},
#               200: {"msg": "ok\n"},
#               500: {"msg": "Unexpected error while processing the sale request\n"}
#           },
#           tags=[post_stocks])
# def add_sale(body: PostBodySchema):
#     try:
#         try:
#             stock_symbol = StockSymbolsEnum(body.stock_symbol.split(".")[0])
#         except ValueError:
#             return Response(response="Requested Resource was Not Found\n", status=404)
#         already_included_stock = [x for x in transactions if x.symbol == stock_symbol and x.qty != 0]
#         if already_included_stock:
#             stock = already_included_stock[0]
#             stock.sell_units(units=body.units, price=body.price_per_unit)
#             return Response("ok\n", status=200)
#         else:
#             return Response(response="Requested Resource was Not Found\n", status=404)
#     except Exception:
#         return Response("Unexpected error while processing the sale request\n", status=500)


# if __name__ == "__main__":

# Dummy data
stock1 = transactions_pb2.Stock()
stock1.price = 12
stock1.symbol = 15
stock1.qty = 15
stock2 = transactions_pb2.Stock()
stock2.price = 12
stock2.symbol = 18
stock2.qty = 15
transactions.stock.extend([stock1, stock2])
# End Dummy data
app.run(debug=True)
