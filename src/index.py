from flask import jsonify, Response
from flask_openapi3 import Info, OpenAPI, Tag

from src.model.schemas import GetMultipleResponseSchema, GetParameterSchema, GetResponseSchema, \
    PostBodySchema
from src.model.stock import Stock
from src.model.stock_symbols_enum import StockSymbolsEnum

transactions: list[Stock] = [Stock(symbol=z) for z in StockSymbolsEnum]

info = Info(title="Stocks Viewer API", version="1.0.0")
app = OpenAPI(__name__, info=info)

get_stocks = Tag(name="Get Methods", description="Get All Stocks")
post_stocks = Tag(name="Post Methods", description="Post Specific Stocks")


@app.get("/stocks/all",
         summary="Get stocks",
         description="Get stats for all stocks",
         responses={200: GetMultipleResponseSchema},
         tags=[get_stocks])
def get_all():
    return [x.to_json() for x in transactions if x.qty != 0]


@app.get('/stock/<symbol>',
         summary="Get stock",
         description="Get stats for a specific stock",
         responses={200: GetResponseSchema},
         tags=[get_stocks])
def get_specific_stock(path: GetParameterSchema):
    try:
        stock_name = StockSymbolsEnum(path.symbol.split(".")[0])
        return [x.to_json() for x in transactions if x.qty != 0 and x.symbol == stock_name][0]
    except:
        return jsonify({})


@app.post('/purchase',
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
        try:
            stock_symbol = StockSymbolsEnum(body.stock_symbol.split(".")[0])
        except ValueError:
            return Response(response="Requested Resource was Not Found\n", status=404)
        stock = [x for x in transactions if x.symbol == stock_symbol][0]
        stock.buy_units(units=body.units, price=body.price_per_unit)
        return Response("ok\n", status=200)
    except Exception:
        return Response("Unexpected error while processing the purchase request\n", status=500)


@app.post('/sell',
          summary="Sell stock",
          description="Post the details of stock to sell",
          responses={
              404: {"msg": "Requested Resource was Not Found\n"},
              200: {"msg": "ok\n"},
              500: {"msg": "Unexpected error while processing the sale request\n"}
          },
          tags=[post_stocks])
def add_sale(body: PostBodySchema):
    try:
        try:
            stock_symbol = StockSymbolsEnum(body.stock_symbol.split(".")[0])
        except ValueError:
            return Response(response="Requested Resource was Not Found\n", status=404)
        already_included_stock = [x for x in transactions if x.symbol == stock_symbol and x.qty != 0]
        if already_included_stock:
            stock = already_included_stock[0]
            stock.sell_units(units=body.units, price=body.price_per_unit)
            return Response("ok\n", status=200)
        else:
            return Response(response="Requested Resource was Not Found\n", status=404)
    except Exception:
        return Response("Unexpected error while processing the sale request\n", status=500)


if __name__ == "__main__":
    app.run(debug=True)
