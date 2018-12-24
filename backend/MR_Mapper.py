from pyhive import hive
import pandas as pd
import sys
from algorithm.algorithm import Bond
import datetime
import re


def date_tuple(date_string):
    lst=date_string.split('-')
    return(datetime.date(int(lst[0]),int(lst[1]),int(lst[2])))


def gen_maturity_date(matu):
    regex = re.compile(r'\.|、')
    splt = regex.split(matu)
    return datetime.date(datetime.datetime.now().year, int(splt[0]), int(splt[1]))


conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
cursor = conn.cursor()
# cursor.execute("select DISTINCT dated_date from bonds")
# for result in cursor.fetchall():
#     print(result)
cursor.execute("select denomination,issue_start_date,dated_date,expiration_date,repayment_method,APR,bond_id from bonds")
for result in cursor.fetchall():
    print(result)
    print("buyDate=",datetime.datetime.now().date(), "startDate=",date_tuple(result[1]),"maturity=",gen_maturity_date(result[2]))
    bond_instance = Bond(parValue=result[0], buyDate=datetime.datetime.now().date(), startDate=date_tuple(result[1]),maturity=gen_maturity_date(result[2],datetime.datetime.now()),frequency=result[4],ir=result[5], verbose=False)
    # Operations goes here. Make sure each line of output is "identifier (\t) numerical_value".
    print(result[6], bond_instance.presentValue2(), sep="\t")

