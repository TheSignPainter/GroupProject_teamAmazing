from pyhive import hive
import pandas as pd
import sys
import sys
import os.path
this_dir = os.path.dirname(__file__)
sys.path.insert(0, this_dir)
from algorithm import Bond
import datetime
import re

"""
Logic: 
1. Query the database using a single-threaded function.
2. Output the queried results in a temp file.
3. Distributively process the file(generate bond instances, compute, as) via mapper.
4. Reducer used for averaging/sorting.
5. Read the output file into this python program. Cleanup.

*****
Note that this can only be executed on the server.
*****
"""


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
for line in sys.stdin:
    line = line.strip()
    result = line.split("\t")
    # print(result)
    try:
        result[0]=float(result[0])
        result[4]=int(result[4])
        result[5] = float(result[5])
    # print("buyDate=",datetime.datetime.now().date(), "startDate=",date_tuple(result[1]),"maturity=",gen_maturity_date(result[2]))
        if result[4]==1 or result[4]==2 :
            assert datetime.datetime.now().date()<date_tuple(result[3])
            bond_instance = Bond(parValue=result[0], buyDate=datetime.datetime.now().date(), startDate=date_tuple(result[1]),maturity=date_tuple(result[3]),frequency=result[4],ir=result[5], verbose=False)
            # Operations goes here. Make sure each line of output is "identifier (\t) numerical_value".
            print(result[6], bond_instance.presentValue2(), sep="\t")
    except Exception as e:
        continue
