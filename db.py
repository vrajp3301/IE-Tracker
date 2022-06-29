from deta import Deta
import os
from dotenv import load_dotenv

load_dotenv(".env")

DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

db = deta.Base("monthly_reports")

def insert_period(period,incomes,expenses):
    return db.put({"key":period,"incomes":incomes,"expenses":expenses})

def fetch_all():
    res = db.fetch()
    return res.items

def get_period(period):
    return db.get(period)

def get_all_periods():
    items = fetch_all()
    periods = [item["key"] for item in items]
    return periods