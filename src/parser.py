import os
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

from logger import logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
print(BASE_URL)

def fetch_currency_rates(date_str):
    url = BASE_URL + '=' + date_str
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = 'windows-1251'
        logger.info(f"Reply received from {url}")
        return response.text
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP request error {url}: {http_err}")
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
    except requests.exceptions.Timeout:
        logger.error("The timeout for a response from the server has been exceeded")
    except requests.exceptions.RequestException as err:
        logger.error(f"Error executing request: {err}")
    return None

def parse_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        logger.error(f"Error parsing XML: {e}")
        return []

    rates = []
    for valute in root.findall('Valute'):
        try:
            char_code = valute.find('CharCode').text
            name = valute.find('Name').text
            value_str = valute.find('Value').text
            nominal_str = valute.find('Nominal').text

            if not all([char_code, name, value_str, nominal_str]):
                raise ValueError("One of the required tags is missing")

            value = float(value_str.replace(',', '.'))
            nominal = int(nominal_str)
            rate = value / nominal
            rates.append((char_code, name, rate))
        except Exception as e:
            logger.error(f"Error processing currency: {ET.tostring(valute, encoding='unicode')} - {e}")
            continue
    return rates
