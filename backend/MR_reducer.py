
import sys

total = 0
sum = 0
for data in sys.stdin:
    data = data.strip()
    record = data.split("\t")
    sum += float(record[1])
    total+=1
sys.stdout.write("%f\n" % (sum/total))