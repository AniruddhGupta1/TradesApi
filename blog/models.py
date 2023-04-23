from database import Base
from sqlalchemy import Column,Integer,String,Date,Time,MetaData,Float,ForeignKey

from sqlalchemy.orm import relationship


# SQLAlchemy models
class TradeDetails(Base):
    __tablename__ = "trade_details"
    id = Column(Integer, primary_key=True)
    buy_sell_indicator= Column(String, nullable=False, doc="A value of BUY for buys, SELL for sells.")
    price = Column(Float, nullable=False, doc="The price of the Trade.")
    quantity = Column(Integer, nullable=False, doc="The amount of units traded.")
    trade_id = Column(Integer, ForeignKey("trades.id"), nullable=False)
    trade = relationship("Trade", back_populates="trade_details")


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True,nullable=False)
    asset_class = Column(String, nullable=False, doc="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty = Column(String, doc="The counterparty the trade was executed with. May not always be available")
    instrument_id = Column(String, nullable=False, doc="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name = Column(String, nullable=False, doc="The name of the instrument traded.")
    trade_date_time = Column(Date, nullable=False, doc="The date-time the Trade was executed")
    trader = Column(String, nullable=False, doc="The name of the Trader")
    trade_details = relationship("TradeDetails", back_populates="trade")


    # One-to-one relationship with TradeDetails
   



    # One-to-one relationship with Trade




# class TradeDetails(Base):
#     __tablename__ = "TradeDetails"
#     buySellIndicator= Column(String)

#     price = Column(String)

#     quantity = Column(Integer)