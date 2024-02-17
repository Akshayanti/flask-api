curl -X POST -H "Content-Type: application/json" -d '{
	"stock_symbol": "NVDA",
	"price_per_unit": 1000.0,
	"units": 10
}' http://localhost:5000/buy

sleep 1

curl -X POST -H "Content-Type: application/json" -d '{
	"stock_symbol": "NVDA",
	"price_per_unit": 2000.0,
	"units": 10
}' http://localhost:5000/buy

sleep 1

curl http://localhost:5000/stocks/all

sleep 1

curl -X POST -H "Content-Type: application/json" -d '{
	"stock_symbol": "BARC",
	"price_per_unit": 1000.0,
	"units": 10
}' http://localhost:5000/sell

sleep 1

curl http://localhost:5000/stocks/all

sleep 1

curl -X POST -H "Content-Type: application/json" -d '{
	"stock_symbol": "BARC.L",
	"price_per_unit": 15000.0,
	"units": 5
}' http://localhost:5000/sell

sleep 1

curl -X POST -H "Content-Type: application/json" -d '{
	"stock_symbol": "BARCL",
	"price_per_unit": 15000.0,
	"units": 5
}' http://localhost:5000/sell

sleep 1

curl http://localhost:5000/stocks/all

sleep 1

curl http://localhost:5000/stock/BARC

sleep 1

curl http://localhost:5000/stock/BARCELONA