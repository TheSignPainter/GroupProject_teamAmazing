from pyhive import hive
#import pandas as pd
import sys
from algorithm.algorithm import Bond
import datetime
import re
from util import id_generator

def to_date(date_string):
    lst=date_string.split('-')
    return(datetime.date(int(lst[0]),int(lst[1]),int(lst[2])))

def gen_maturity_date(matu):
    regex = re.compile(r'\.|、')
    splt = regex.split(matu)
    return datetime.date(datetime.datetime.now().year, int(splt[0]), int(splt[1]))



conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")

cursor = conn.cursor()
# An example on inserting data. Note: only "users" table supports that.
# command = 'CREATE TABLE users(id STRING, user_name STRING, email STRING, password STRING)' \
#           'CLUSTERED BY(id) INTO 64 BUCKETS STORED AS ORC ' \
#           'TBLPROPERTIES("transactional"="true",' \
#           '  "compactor.mapreduce.map.memory.mb"="2048",' \
#           '  "compactorthreshold.hive.compactor.delta.num.threshold"="4",' \
#           '  "compactorthreshold.hive.compactor.delta.pct.threshold"="0.5"' \
#           ')'
command = "show tables"
cursor.execute(command)
# print("insertion done.")
for result in cursor.fetchall():
     print(result)
cursor.execute("select denomination,issue_start_date,dated_date,expiration_date,repayment_method,APR from bonds where bond_id='000696'")
for result in cursor.fetchall():
    print(result)
    bond_instance = Bond(parValue=result[0], buyDate=datetime.datetime.now().date(), startDate=date_tuple(result[1]),maturity=gen_maturity_date(result[2]),frequency=result[4],ir=result[5])


def getQueryResults(q):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
    cursor = conn.cursor()
    cursor.execute(
        "select bond_id, abbrev, company_name from bonds where company_name LIKE '%{query}%' or bond_id LIKE '{query}%' or abbrev LIKE '%{query}%' limit 5".format(query=q))
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data


def getBondInfoDetail(q):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
    cursor = conn.cursor()
    cursor.execute(
        "select * from bonds where bond_id = '{query}' limit 1".format(
            query=q))
    data = cursor.fetchall()[0]
    bond_instance = Bond(yieldToMaturity=0.055, parValue=data[6], buyDate=datetime.datetime.now().date(), startDate=to_date(data[14].split('-')[0]+'-'+('-'.join(data[11].split('.')))),
                         maturity=to_date(data[12]), frequency=data[21], ir=data[9]/100)
    result = {'FullName': data[0], 'Code': data[1], 'ShortName': data[2], 'StartDate': data[14], 'Range': data[8], 'IR': data[9],
              'IRDate': data[11], 'DirtyPrice': bond_instance.pv_dirty, 'CleanPrice': bond_instance.pv_clean, 'YTM': bond_instance.yieldToMaturity*100,
              'Duration': bond_instance.duration, 'Convexity': bond_instance.convexity}
    cursor.close()
    conn.commit()
    conn.close()
    return result


def getUser(username, password):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
    cursor = conn.cursor()
    cursor.execute(
        "select * from users where email = '{username}' and password = '{passwd}'".format(
            username=username, passwd=password))
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data

def getUserByID(ID):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
    cursor = conn.cursor()
    cursor.execute(
        "select * from users where id = '{id}'".format(id=ID))
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data

def addUser(username, email, password):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL", username='fourier')
    cursor = conn.cursor()
    id = ''
    while(1):
        id = id_generator()
        cursor.execute("select * from users where id='{id}'".format(id=id))
        if (len(cursor.fetchall())==0):
            break
    cursor.execute("insert into users (id, user_name, email, password) VALUES ('{id}', '{username}', '{email}', '{password}')".format(id=id,username=username,email=email, password=password))
    cursor.close()
    conn.commit()
    conn.close()
    return [id, username, email]


def print_all_users():
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
    cursor = conn.cursor()
    cursor.execute(
        "select * from users ")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    conn.commit()
    conn.close()

def print_bond_info(id):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")
    cursor = conn.cursor()
    cursor.execute(
        "select * from bonds where bond_id = "+id)
    data = cursor.fetchall()
    print(data)
    cursor.close()
    conn.commit()
    conn.close()


def addSubscribe_(user_id, bond_id):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL", username='fourier')
    cursor = conn.cursor()
    cursor.execute("select status from subscribe where user_id='{user_id}' and bond_id = '{bond_id}'".format(user_id=user_id, bond_id = bond_id))
    judge = cursor.fetchall()
    if (len(judge) == 0):
        cursor.execute(
        "insert into subscribe (user_id, bond_id, status) VALUES ('{user_id}', '{bond_id}', '1')".format(
            user_id=user_id, bond_id=bond_id))
    elif (judge[0]=='0'):
        cursor.execute("update subscribe set status = '1' where user_id='{user_id}' and bond_id='{bond_id}'".format(user_id=user_id, bond_id=bond_id))
    cursor.close()
    conn.commit()
    conn.close()


def getSubscribe_(user_id):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL", username='fourier')
    cursor = conn.cursor()
    cursor.execute("select company_name, abbrev, bonds.bond_id from subscribe inner join bonds on subscribe.bond_id = bonds.bond_id where user_id='{user_id}' and status = '1'".format(user_id=user_id))
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data


'''conn = hive.Connection(host="202.120.38.90", port=10086, username='fourier', auth="NOSASL")
cursor = conn.cursor()
cursor.execute('select * from subscribe')
print(cursor.fetchall())
cursor.close()
conn.commit()
conn.close()'''
#print_all_users()
#print(getSubscribe_('3d93314c'))
