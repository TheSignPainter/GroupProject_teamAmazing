import re
import uuid
from algorithm import Bond
from datetime import date, datetime


def check_date(string): # Check whether a string is given form "YYYY-MM-DD".
    if re.match(r"^\d{4}-\d{2}-\d{2}$",string):
        return True
    else:
        return False

def id_generator():
    return str(uuid.uuid4())[0:8]


def calculate_(form):
    type = form['type']
    if type == 'ytm':
        buy_date = datetime.strptime(form['buy_date'], "%Y-%m-%d").date()
        maturity = datetime.strptime(form['maturity'], "%Y-%m-%d").date()
        bond = Bond(parValue=float(form['par_value']), buyDate=buy_date,
                    buyPrice=float(form['buy_price']), maturity=maturity,
                    ir=float(form['ir'])/100, frequency=int(form['frequency']))
        return round(bond.computed_YTM*100,4)
    if type == 'pricing':
        buy_date = datetime.strptime(form['buy_date'], "%Y-%m-%d").date()
        maturity = datetime.strptime(form['maturity'], "%Y-%m-%d").date()
        bond = Bond(yieldToMaturity=float(form['ytm'])/100, buyDate=buy_date,
                    parValue=float(form['par_value']), maturity=maturity,
                    ir=float(form['ir']) / 100, frequency=int(form['frequency']))
        return round(bond.pv_dirty, 4), round(bond.pv_clean, 4)
    if type == 'risk':
        buy_date = datetime.strptime(form['buy_date'], "%Y-%m-%d").date()
        maturity = datetime.strptime(form['maturity'], "%Y-%m-%d").date()
        bond = Bond(yieldToMaturity=float(form['ytm'])/100, buyDate=buy_date,
                    parValue=float(form['par_value']), maturity=maturity,
                    ir=float(form['ir']) / 100, frequency=int(form['frequency']))
        return round(bond.modifiedD, 4), round(bond.convexity, 4)