from pyhive import hive
import pandas as pd
import sys

conn = hive.Connection(host="192.168.1.113", port=10000, auth="NOSASL")
cursor = conn.cursor()
cursor.execute("select * from bonds")
for result in cursor.fetchall():
    print( result)
