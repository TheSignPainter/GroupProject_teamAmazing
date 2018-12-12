
f = open("bonds_181210.txt", mode='r',encoding='utf8')

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
"""

chs_to_attribute = dict()
for i in data_definition.split('\n'):
    if i != '':
        # print(i)
        print(i.split('\t')[0],i.split('\t')[1].split(' ')[0])
        chs_to_attribute[i.split('\t')[0]]=i.split('\t')[1].split(' ')[0]

class bond:
    def __init__(self):
        self.attributes=dict()
        # self.company_name = None
        # self.bond_id = None
        # self.abbrev = None
        # self.release_date = None
        # self.on_market_date = None
        # self.issue_amount = None
        # self.denomination = None
        # self.initial_offer_price = None
        # self.bond_term = None
        # self.APR = None
        # self.adjusted_APR = None
        # self.dated_date = None
        # self.expiration_date = None
        # self.redemption_price = None
        # self.issue_start_date = None
        # self.issue_end_date = None
        # self.subscriber = None
        # self.bond_value = None
        # self.list_location = None
        # self.credit_rank = None
        # self.issue_institution = None
        # self.repayment_method = None
        # self.guarantor = None
        # self.issurance_method = None
        # self.issuing_target = None
        # self.lead_underwriter = None
        # self.tax_status = None
        # self.bond_type = None
        # self.remarks = None
    def update(self,description,value):
        attribute = chs_to_attribute.get(description)
        assert attribute is not None
        self.attributes[attribute]=value

records=[]
f.readline()
for i in f.readlines():
    # print(i)
    line = i.replace("%\t", "\t")
    print(line)
    records.append(line)
    # if list[0] == "公司名称":
    #     if (current_bond):
    #         bonds.append(current_bond)
    #     current_bond = bond()
    # if len(list)>1:
    #     current_bond.update(list[0],list[1])
# print(bonds[0].attributes)

output = open("output_trades.txt", mode='w', encoding="utf-8")
output.writelines(records)