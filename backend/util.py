import re
import uuid
from algorithm.algorithm import Bond
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
        bond = Bond(parValue=float(form['par_value']), buyDate=datetime.strptime(form['buy_date'], "%Y-%m-%d").date(),
                    buyPrice=float(form['buy_price']), maturity=datetime.strptime(form['maturity'], "%Y-%m-%d").date(),
                    ir=float(form['ir']), frequency=int(form['frequency']))
        print(float(form['par_value']), datetime.strptime(form['buy_date'], "%Y-%m-%d").date(),
              float(form['buy_price']), datetime.strptime(form['maturity'], "%Y-%m-%d").date(),
              float(form['ir'])/100, int(form['frequency']))
        return bond.computed_YTM