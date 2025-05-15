import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Numeric, Date, Integer, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

from logger import logger

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

Base = declarative_base()

class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True)
    currency_code = Column(String(10))
    currency_name = Column(String(100))
    rate = Column(Numeric)
    rate_date = Column(Date)

    __table_args__ = (
        UniqueConstraint('currency_code', 'rate_date', name='uix_currency_date'),
    )

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def save_to_db(rates, date_obj):
    try:
        Base.metadata.create_all(engine)
        session = Session()

        records = [
            CurrencyRate(
                currency_code=code,
                currency_name=name,
                rate=rate,
                rate_date=date_obj
            )
            for code, name, rate in rates
        ]

        session.add_all(records)
        session.commit()
        logger.info(f"{len(records)} records saved in the database for {date_obj}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving data in database: {e}")
    finally:
        session.close()
