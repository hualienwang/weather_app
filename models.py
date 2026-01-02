from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherQuery(Base):
    __tablename__ = 'weather_queries'
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    query_time = Column(DateTime, default=func.now())
    ip_address = Column(String, nullable=True)
    icon_code = Column(String, nullable=True)
    api_key_id = Column(Integer, index=True, nullable=True)

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, default="anonymous")
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)