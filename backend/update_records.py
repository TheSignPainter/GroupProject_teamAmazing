
#TODO check the format of date.

# 描述，字段，数据类型
data_definition ="""
代码	bond_id STRING
简称	abbrev STRING
最新价	latest_price DOUBLE
涨跌	change DOUBLE
涨跌幅(%)	change_rate DOUBLE
成交金额	turnover DOUBLE
成交量	volume DOUBLE
开盘	opening_price DOUBLE
最高	high DOUBLE
最低	low DOUBLE
日期	date STRING (YYYY-MM-DD)
"""

chs_to_attribute = dict()
for i in data_definition.split('\n'):
    if i != '':
        # print(i)
        print(i.split('\t')[0],i.split('\t')[1].split(' ')[0])
        chs_to_attribute[i.split('\t')[0]]=i.split('\t')[1].split(' ')[0]


def generate_record(input_path, output_path):
    f = open(input_path, mode='r', encoding='utf8')
    records=[]
    f.readline()    # 1st line is assigned to descriptions. Skip that.
    for i in f.readlines():
        # print(i)
        line = i.replace("%\t", "\t") # Change rate: omit the "%" symbol.
        #print(line)
        records.append(line)
    output = open(output_path, mode='w', encoding="utf-8")
    output.writelines(records)
    print("Successfully generated trade records at:", output_path)