from pyhive import hive
import pandas as pd
import sys
from algorithm.algorithm import Bond
import datetime
import re
from backend.util import id_generator, yieldtomaturity
import json

def to_date(date_string):
    lst=date_string.split('-')
    return(datetime.date(int(lst[0]),int(lst[1]),int(lst[2])))

def gen_maturity_date(matu):
    regex = re.compile(r'\.|、')
    splt = regex.split(matu)
    return datetime.date(datetime.datetime.now().year, int(splt[0]), int(splt[1]))


'''
conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL")

cursor = conn.cursor()
command = ("drop table users")
cursor.execute(command)
command = 'CREATE TABLE users(id STRING, user_name STRING, email STRING, password STRING)' \
          'CLUSTERED BY(id) INTO 2 BUCKETS STORED AS ORC ' \
          'TBLPROPERTIES("transactional"="true"' \
           ')'
# command = "show tables"
cursor.execute(command)
# print("insertion done.")
for result in cursor.fetchall():
     print(result)
cursor.execute("select denomination,issue_start_date,dated_date,expiration_date,repayment_method,APR from bonds where bond_id='000696'")
for result in cursor.fetchall():
    print(result)
    bond_instance = Bond(parValue=result[0], buyDate=datetime.datetime.now().date(), startDate=date_tuple(result[1]),maturity=gen_maturity_date(result[2]),frequency=result[4],ir=result[5])
'''

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
    cursor.close()
    conn.commit()
    conn.close()
    remainingYear = int(data[12].split('-')[0]) - int(datetime.datetime.now().date().year)
    remainingDay = to_date(data[12]) - datetime.datetime.now().date()
    if remainingDay.days < 0 or data[20] != '0':
        return {'FullName': data[0], 'Code': data[1], 'ShortName': data[2], 'StartDate': data[14], 'Range': data[8], 'IR': data[9],
              'IRDate': data[11], 'DirtyPrice': '-', 'CleanPrice': '-', 'YTM': '-',
              'Duration': '-', 'Convexity': '-'}
    else:
        yield2maturity = yieldtomaturity(remainingYear)
        bond_instance = Bond(yieldToMaturity=float(yield2maturity)/100, parValue=data[6], buyDate=datetime.datetime.now().date(), maturity=to_date(data[12]), frequency=data[21], ir=data[9]/100)
        result = {'FullName': data[0], 'Code': data[1], 'ShortName': data[2], 'StartDate': data[14], 'Range': data[8], 'IR': data[9],
                  'IRDate': data[11], 'DirtyPrice': bond_instance.pv_dirty, 'CleanPrice': bond_instance.pv_clean, 'YTM': bond_instance.yieldToMaturity*100,
                  'Duration': bond_instance.duration, 'Convexity': bond_instance.convexity}
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
    result = 'fail'
    try:
        if (len(judge) == 0):
            cursor.execute(
            "insert into subscribe (user_id, bond_id, status) VALUES ('{user_id}', '{bond_id}', '1')".format(
                user_id=user_id, bond_id=bond_id))
            result = 'success'
        elif (judge[0]=='0'):
            cursor.execute("update subscribe set status = '1' where user_id='{user_id}' and bond_id='{bond_id}'".format(user_id=user_id, bond_id=bond_id))
            result = 'success'
        else:
            result = 'existed'
    except:
        result = 'fail'
    cursor.close()
    conn.commit()
    conn.close()
    return result


def getSubscribe_(user_id):
    conn = hive.Connection(host="202.120.38.90", port=10086, auth="NOSASL", username='fourier')
    cursor = conn.cursor()
    #cursor.execute("select company_name, abbrev, bonds.bond_id from subscribe inner join bonds on subscribe.bond_id = bonds.bond_id where user_id='{user_id}' and status = '1'".format(user_id=user_id))
    #cursor.execute("SELECT company_name, abbrev, bonds.bond_id FROM subscribe LEFT OUTER JOIN bonds ON (subscribe.bond_id=bonds.bond_id AND subscribe.user_id='{user_id}' AND subscribe.status='1')".format(user_id=user_id))
    #cursor.execute("select company_name, abbrev, bonds.bond_id from bonds where bonds.bond_id in (select bond_id from subscribe where user_id='{user_id}' and status = '1')".format(user_id=user_id))
    cursor.execute("select bond_id from subscribe where user_id='{user_id}' and status = '1'".format(
            user_id=user_id))
    data = cursor.fetchall()
    data = json.dumps([d[0] for d in data], ensure_ascii=False)
    data = '(' + data[1:-1] + ')'
    cursor.execute("select company_name, abbrev, bond_id from bonds where bond_id in "+data)
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return data



'''conn = hive.Connection(host="202.120.38.90", port=10086, username='fourier', auth="NOSASL")
cursor = conn.cursor()
cursor.execute("SELECT company_name, abbrev, bonds.bond_id FROM subscribe INNER JOIN bonds ON (subscribe.bond_id=bonds.bond_id AND subscribe.user_id='c3be8630' AND subscribe.status='1')")
print(cursor.fetchall())
cursor.close()
conn.commit()
conn.close()'''
#print_all_users()
#print(getSubscribe_('c3be8630'))
