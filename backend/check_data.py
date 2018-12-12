
f = open("bond_info.txt", mode='r',encoding='utf8')

# 描述，字段，数据类型
data_definition ="""公司名称	company_name STRING
债券代码	bond_id STRING
代码简称	abbrev STRING
发布时间	release_date STRING (YYYY-MM-DD)
上市日	on_market_date STRING (YYYY-MM-DD)
发行额(亿元)	issue_amount DOUBLE 
面额(元)	denomination DOUBLE
发行价(元)	initial_offer_price DOUBLE
期限(年)	bond_term DOUBLE
年利率(%)	APR DOUBLE
调整后年利率	adjusted_APR DOUBLE
计息日	dated_date STRING (MM-DD)
到期日	expiration_date STRING (YYYY-MM-DD)
兑付价(元)	redemption_price DOUBLE
发行起始日	issue_start_date STRING (YYYY-MM-DD)
发行截止日	issue_end_date STRING (YYYY-MM-DD)
认购对象	subscriber STRING 
债券价值	bond_value DOUBLE
上市地	list_location STRING
信用级别	credit_rank STRING
发行单位	issue_institution STRING
还本付息方式	repayment_method STRING
发行担保人	guarantor STRING
发行方式	issurance_method STRING
发行对象	issuing_target STRING
主承销机构	lead_underwriter STRING
税收状况	tax_status STRING
债券类型	bond_type STRING
项目	item STRING
备注	remarks STRING
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

bonds = []
current_bond=None
for i in f.readlines():
    # print(i)
    list = i.strip().split("\t", maxsplit=1)
    print(list)
    if list[0] == "公司名称":
        if (current_bond):
            bonds.append(current_bond)
        current_bond = bond()
    if len(list)>1:
        current_bond.update(list[0],list[1])
print(bonds[0].attributes)

attr_order=[]
for i in data_definition.split('\n'):
    if i != '':
        # print(i)
        attr_order.append(i.split('\t')[1].split(' ')[0])
print(attr_order)
content = []
output = open("output.txt", mode='w', encoding="utf-8")
for bond in bonds:
    line = ""
    for i in attr_order:
        attr_value = bond.attributes.get(i)
        if attr_value:
            line+=attr_value+"\t"
        else:
            line+="\\N\t"
    line+="\n"
    print(line)
    content.append(line)
output.writelines(content)