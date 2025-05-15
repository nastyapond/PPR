from dotenv import load_dotenv
from datetime import datetime
import os

from db import save_to_db
from logger import logger
from parser import fetch_currency_rates, parse_xml

def app():
    input_date = input("Enter date in DD.MM.YYYY format: ")
    try:
        date_obj = datetime.strptime(input_date, "%d.%m.%Y")
        xml = fetch_currency_rates(date_obj.strftime("%d/%m/%Y"))
        rates = parse_xml(xml)
        save_to_db(rates, date_obj.date())
        logger.info(f"Exchange rates for {input_date} saved successfully")
    except Exception as e:
        logger.error("Error: %s", e)

if __name__ == "__main__":
    app()
