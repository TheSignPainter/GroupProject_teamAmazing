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

def yieldtomaturity(year):
    curve = [[0.5, 2.63],
     [1, 2.738480000000001],
     [2, 2.9711600000000007],
     [3, 3.12],
     [4, 3.15875],
     [5, 3.25],
     [6, 3.468325],
     [7, 3.59],
     [8, 3.5582740740740744],
     [9, 3.526525925925926],
     [10, 3.52],
     [11, 3.535093750000001],
     [12, 3.5512499999999996],
     [13, 3.5682812499999987],
     [14, 3.5860000000000003],
     [15, 3.6042187500000002],
     [16, 3.62275],
     [17, 3.6414062499999997],
     [18, 3.6600000000000006],
     [19, 3.6783437500000002],
     [20, 3.69625],
     [21, 3.7135312500000004],
     [22, 3.7300000000000004],
     [23, 3.7454687499999997],
     [24, 3.75975],
     [25, 3.77265625],
     [26, 3.7840000000000007],
     [27, 3.7935937499999985],
     [28, 3.80125],
     [29, 3.806781250000001],
     [30, 3.81],
     [31, 3.812000000000001],
     [32, 3.814],
     [33, 3.8159999999999994],
     [34, 3.818],
     [35, 3.8200000000000003],
     [36, 3.822],
     [37, 3.824],
     [38, 3.826000000000001],
     [39, 3.8280000000000003],
     [40, 3.83],
     [41, 3.8320000000000007],
     [42, 3.8340000000000005],
     [43, 3.8360000000000003],
     [44, 3.838],
     [45, 3.84],
     [46, 3.842000000000001],
     [47, 3.8439999999999985],
     [48, 3.846],
     [49, 3.848000000000001],
     [50, 3.85]]
    curve = {p[0]: p[1] for p in curve}
    return curve[year]