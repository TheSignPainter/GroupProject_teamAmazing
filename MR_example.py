from pyhive import hive
import pandas as pd
import sys
import datetime
import re
import os

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
cursor.execute("select denomination,issue_start_date,dated_date,expiration_date,repayment_method,APR,bond_id from bonds")
total = 0
f = open("tmp.txt",mode='w',encoding='utf-8')
l = []
for result in cursor.fetchall():
    s = ""
    for item in result:
        s+=str(item)+"\t"
    l.append(s+"\n")
    # print("buyDate=",datetime.datetime.now().date(), "startDate=",date_tuple(result[1]),"maturity=",gen_maturity_date(result[2]))
    # if result[4]==1 or result[4]==2 :
    #     try:
    #         assert datetime.datetime.now().date()<date_tuple(result[3])
    #         # bond_instance = Bond(parValue=result[0], buyDate=datetime.datetime.now().date(), startDate=date_tuple(result[1]),maturity=date_tuple(result[3]),frequency=result[4],ir=result[5], verbose=False)
        # Operations goes here. Make sure each line of output is "identifier (\t) numerical_value".
        #     print(result[6], bond_instance.presentValue2(), sep="\t")
        # except:
        #     continue
f.writelines(l)
output_path = "hd_output"
os.system("hadoop fs -rm -r %s" % output_path)
os.system('hadoop jar /home/fourier/Invoke/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar -D stream.non.zero.exit.is.failure=false -files backend -input tmp/tmp.txt  -output hd_output -mapper "python3 backend/MR_mapper.py" -reducer "python3 backend/MR_reducer.py"')
out_str = os.popen('hadoop fs -cat %s/part-00000' % output_path).read()
print("This is python output.")
print(out_str)