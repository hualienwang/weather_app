import os
import secrets
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from models import Base, WeatherQuery, APIKey
from datetime import datetime, timedelta

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./weather.db"
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def create_api_key(owner: str = "anonymous") -> str:
    key = secrets.token_urlsafe(32)
    db = SessionLocal()
    try:
        db_key = APIKey(key=key, owner=owner, is_active=True)
        db.add(db_key)
        db.commit()
        return key
    finally:
        db.close()

def validate_api_key(key: str) -> bool:
    db = SessionLocal()
    try:
        key_obj = db.query(APIKey).filter(
            APIKey.key == key,
            APIKey.is_active == True
        ).first()
        return key_obj is not None
    finally:
        db.close()

def get_api_key_id(key: str) -> int:
    db = SessionLocal()
    try:
        key_obj = db.query(APIKey).filter(
            APIKey.key == key,
            APIKey.is_active == True
        ).first()
        return key_obj.id if key_obj else None
    finally:
        db.close()

def log_query(city: str, ip: str = None, icon_code: str = None, api_key_id: int = None):
    db = SessionLocal()
    try:
        query = WeatherQuery(
            city=city.lower(),
            ip_address=ip,
            icon_code=icon_code,
            api_key_id=api_key_id
        )
        db.add(query)
        db.commit()
    finally:
        db.close()

def get_top_cities(days: int = 7):
    db = SessionLocal()
    try:
        since = datetime.utcnow() - timedelta(days=days)
        results = (
            db.query(
                WeatherQuery.city,
                func.count(WeatherQuery.city).label('count')
            )
            .filter(WeatherQuery.query_time >= since)
            .group_by(WeatherQuery.city)
            .order_by(func.count(WeatherQuery.city).desc())
            .limit(10)
            .all()
        )
        return [{"city": r.city, "count": r.count} for r in results]
    finally:
        db.close()