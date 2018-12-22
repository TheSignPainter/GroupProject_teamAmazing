# Todo: Ensure the date is legal. Otherwise we'll get NULL(\N).
from util import check_date


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
计息日	dated_date STRING (MM.DD)
到期日	expiration_date STRING (YYYY-MM-DD)
兑付价(元)	redemption_price DOUBLE
发行起始日	issue_start_date STRING (YYYY-MM-DD)
发行截止日	issue_end_date STRING (YYYY-MM-DD)
认购对象	subscriber STRING 
债券价值	bond_value DOUBLE
上市地	list_location STRING
信用级别	credit_rank STRING
发行单位	issue_institution STRING
还本付息方式	repayment_method INT
发行担保人	guarantor STRING
发行方式	issurance_method STRING
发行对象	issuing_target STRING
主承销机构	lead_underwriter STRING
税收状况	tax_status STRING
债券类型	bond_type STRING
项目	item STRING
备注	remarks STRING
"""

date_attributes=["release_date","on_market_date","expiration_date","issue_start_date","issue_end_date"]

class Bond():
    def __init__(self):
        self.attributes = dict()
        self.chs_to_attribute = dict()
        for i in data_definition.split('\n'):
            if i != '':
                # print(i.split('\t')[0],i.split('\t')[1].split(' ')[0])
                self.chs_to_attribute[i.split('\t')[0]] = i.split('\t')[1].split(' ')[0]

    def update(self, description, value):
        value = value.replace('\u3000','')
        attribute = self.chs_to_attribute.get(description)
        assert attribute is not None
        if attribute in date_attributes:
            if not check_date(value):
                return -1
        self.attributes[attribute] = value
        return 0


def generate_output(input_path, output_path):
    f = open(input_path, mode='r',encoding='utf8')
    bonds = []
    current_bond=None
    for i in f.readlines():
        # print(i)
        list = i.strip().split("\t", maxsplit=1)
        # print(list)
        if list[0] == "公司名称":
            if (current_bond):
                bonds.append(current_bond)
            current_bond = Bond()
        if len(list)>1:
            current_bond.update(list[0],list[1])
    # print(bonds[0].attributes)

    attr_order=[]
    for i in data_definition.split('\n'):
        if i != '':
            # print(i)
            attr_order.append(i.split('\t')[1].split(' ')[0])
    # print(attr_order)
    content = []
    output = open(output_path, mode='w', encoding="utf-8")
    for bond in bonds:
        line = ""
        for i in attr_order:
            attr_value = bond.attributes.get(i)
            if attr_value:
                line+=attr_value.strip()+"\t"
            else:
                line+="\\N\t"
        line+="\n"
        # print(line)
        content.append(line)
    output.writelines(content)
    print("Successfully generated output at:", output_path)

generate_output("formal_bond_info.txt","output.txt")