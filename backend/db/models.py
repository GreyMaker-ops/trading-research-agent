"""SQLAlchemy models for TimescaleDB."""

from sqlalchemy import Column, DateTime, Float, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Candle(Base):
    __tablename__ = "candles"
    ts = Column(DateTime, primary_key=True)
    pair = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class Indicator(Base):
    __tablename__ = "indicators"
    ts = Column(DateTime, primary_key=True)
    pair = Column(String, primary_key=True)
    ema_fast = Column(Float)
    ema_slow = Column(Float)
    rsi14 = Column(Float)
    bb_width = Column(Float)
    tweet_z = Column(Float)
    news_polarity = Column(Float)
