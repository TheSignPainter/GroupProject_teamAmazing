from pyhive import hive
import pandas as pd
import sys
import datetime
import re
import os
import time
from backend.algorithm import Bond
"""
Logic: 
1. Query the database using a single-threaded function.
2. Output the queried results in a temp file.
3. Distributively process the file(generate bond instances, compute, as) via mapper.
4. Reducer used for averaging/sorting.
5. Read the output file into this python program. Cleanup.

The operation can be modified on ./backend/MR_mapper.py, MR_reducer.py 

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
cursor.execute("select denomination,issue_start_date,dated_date,expiration_date,repayment_method,APR,bond_id from bonds")
l = []
for result in cursor.fetchall():
    s = ""
    for item in result:
        s+=str(item)+"\t"
    for i in range(75):
        l.append(s+"\n")
    # print("buyDate=",datetime.datetime.now().date(), "startDate=",date_tuple(result[1]),"maturity=",gen_maturity_date(result[2]))

t1 = time.time()
total = 0
sum = 0.0
for line in l:
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
            # print(result[6], bond_instance.presentValue2(), sep="\t")
            sum+=bond_instance.presentValue2()
            total+=1
    except Exception as e:
        continue
print("---------------------------------")
print("This is python output.")
print(sum/total)
print("time used:", time.time()-t1)