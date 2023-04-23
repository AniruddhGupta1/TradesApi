from fastapi import FastAPI,Depends,Request
from pydantic import BaseModel
from typing import Optional
from database import engine,SessionLocal
from sqlalchemy.orm import Session,Query
import schemas,models
# from flask import jsonify,Flask,current_app,request
from datetime import date
from sqlalchemy.orm import session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# app2 = Flask(__name__)

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")

def get_db():
 db= SessionLocal()
 try:
  yield db
 finally:
  db.close()

@app.get("/",response_class=HTMLResponse)
def welcome(request:Request):
 context={'request':request}
 return templates.TemplateResponse("index2.html",context)
# @app.get("/tradeno")
# def result(limit:int=10,total:int=20,published:bool=False):
#  if published:
#   return(f"Out of {total}  {limit} are published in the db")
#  else:
#   return(f"Out of {total} {limit} are not published in the db")


models.Base.metadata.create_all(engine)
@app.post("/Trade")
def createTrade(request:schemas.Trade,db:Session = Depends(get_db)):
 new_trade = models.Trade( asset_class= request.asset_class,counterparty= request.counterparty,instrument_id= request.instrument_id,
                          instrument_name= request.instrument_name,


                          trade_date_time= request.trade_date_time,trader= request.trader)
 trade_details = models.TradeDetails(buy_sell_indicator = request.trade_details.buy_sell_indicator, price = request.trade_details.price,quantity = request.trade_details.quantity)
 new_trade.trade_details = [trade_details]
 db.add(new_trade)
 db.commit()
 db.refresh(new_trade)
 return new_trade
@app.get("/Trade")
def all( sort_by='trade_date_time', sort_order='asc',db:Session= Depends(get_db)):
    
    
    trades_query = db.query(models.Trade).join(models.TradeDetails).filter()
    if (sort_by=='trade_date_time'):
        if sort_order=='asc':
           trades_query = trades_query.order_by(getattr(models.Trade,sort_by).asc())
        else :
           trades_query = trades_query.order_by(getattr(models.Trade,sort_by).desc())
    else:
        if sort_order=='asc':
           trades_query = trades_query.order_by(getattr(models.TradeDetails,sort_by).asc())
        else :
           trades_query = trades_query.order_by(getattr(models.TradeDetails,sort_by).desc())
   

    return trades_query.all()
  #   paginating trades 
   

    # Paginate trades
    # trades = paginate(trades_query, page_param)
    
  
@app.get("/Trade/Search")
def search_trades(search:str,db:Session=Depends(get_db)):
 
  trades = []
  for trade in db.query(models.Trade).all():
      if(search in trade.counterparty or search in trade.instrument_id or search in trade.instrument_name or search in trade.trader):
        trades.append(trade)

  return trades
@app.get("/Trade/filter")
def filter_trades(assetClass: Optional[str] = None,
                   start: Optional[date] = None,
                   end: Optional[date] = None,
                   minPrice: Optional[float] = None,
                   maxPrice: Optional[float] = None,
                   tradeType: Optional[str] = None,
                   db: Session = Depends(get_db)):

    query = db.query(models.Trade)
    query2 = db.query(models.Trade).join(models.TradeDetails)
    
    if assetClass:
        query = query.filter(models.Trade.asset_class == assetClass)

    if start:
        query = query.filter(models.Trade.trade_date_time >= start)

    if end:
        query = query.filter(models.Trade.trade_date_time <= end)

    if minPrice:
        query2 = query2.filter(models.TradeDetails.price >= minPrice)

    if maxPrice:
        query2 = query2.filter(models.TradeDetails.price <= maxPrice)

    if tradeType:
        query2 = query2.filter(models.TradeDetails.buy_sell_indicator == tradeType)

    trades = set(query.all()) & set(query2.all())

    return trades


    return trades

  
@app.get("/Trade/{id}")
def show(id:int,db:Session=Depends(get_db)):
 trade= db.query(models.Trade).filter(models.Trade.id==id).all()
 return trade


# def showthis():
#    return (f"Its running ")
    #



  




 