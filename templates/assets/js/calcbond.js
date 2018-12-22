window.onerror = Function();
/* 债券计算器所用方法集
   @20091201 by fangliming 
*/
var bondCache={};

/*债券持有计算切换
 */
function ChgItem(x){
	document.getElementById("c0").style.display = (x=="c0") ? "block" : "none";	
	document.getElementById("c1").style.display = (x=="c1") ? "block" : "none";	
	document.getElementById("c2").style.display = (x=="c2") ? "block" : "none";
}

/*国债收益计算器
 */
function calWinPdet(){
	var cal_time = document.getElementById("cal_time");
	var cal_amount = document.getElementById("cal_amount");
	var cal_rate = document.getElementById("cal_rate");

	if(cal_time==null){
		return false;
	}else if(cal_time.value==0){
		alert("请选择存期!");
		return false;
	}
	if(cal_amount==null){
		return false;
	}else if (cal_amount.value==""){
		alert("请输入国债金额!");
		return false;
	}
	if(cal_rate == null){
		return false;
	}else if (cal_rate.value==""){
		alert("请输入国债利率!");
		return false;
	}
	if(isNaN(cal_amount.value)){
		alert("请输入数字(国债金额)!");
		return false;
	}
	if(isNaN(cal_rate.value)){
		alert("请输入数字(国债利率)!");
		return false;
	}
	if(cal_amount.value<=0){
		alert("请输入正确的国债金额!");
		return false;
	}
	if(cal_rate.value<=0){
		alert("请输入正确的国债利率!");
		return false;
	}
	var cal_interest = cal_time.value*cal_amount.value *cal_rate.value/100;
	var cal_result = cal_amount.value*1 + cal_interest;
	cal_interest=Math.round(cal_interest*100)/100+"";
	cal_result=Math.round(cal_result*100)/100+"";

	if(document.getElementById("cal_interest")){
		document.getElementById("cal_interest").value = cal_interest;
	}
	if(document.getElementById("cal_result")){
		document.getElementById("cal_result").value=cal_result;
	}	
};

/*国债买卖计算方法
 */
function calBuyPdet(){
	var cal_price = document.getElementById("cal_price");
	var cal_amount = document.getElementById("cal_amount");
	
	if(cal_price==null){
		return false;
	}else if (cal_price.value=="" || isNaN(cal_price.value) || (parseFloat(cal_price.value)<=0)){
		alert("请正确输入国债的价格!");
		return false;
	}
	if(cal_amount==null){
		return false;
	}else if (cal_amount.value=="" || isNaN(cal_amount.value) || (parseInt(cal_amount.value)<=0)){
		alert("请正确输入国债数量!");
		return false;
	}
	var cal_result=parseFloat(cal_price.value)*parseInt(cal_amount.value);
	cal_result=Math.round(cal_result*100)/100;
	if(document.getElementById("cal_result")){
		document.getElementById("cal_result").value = cal_result;
	}
} 


/*债券买卖计算器
*/

bondCache.finger=[["cal_deadline","cal_cost","cal_buyday","cal_presellday","cal_prebuyday"],[true,,,,true],[false,true,true,true,false]];
bondCache.type=[["cal_price","cal_freq","cal_month","cal_rate"],[[true,,,],[true,,true,true],[true,true,,true]],[[true,,,],[true,,,true],[true,true,,true]]]

//初始化选项[选项更更改时更新]
function initMmbjBond(){
	var cal_finger = (document.getElementById('cal_figure_0').checked) ? 1 : 2;
	var cal_type = document.getElementById('cal_type').value;
	var lenght = bondCache.finger[0].length;
	for(var i =0;i<lenght;i++){
		var obj = document.getElementById(bondCache.finger[0][i]);
		var parentobj = document.getElementById(bondCache.finger[0][i]).parentNode
		if(bondCache.finger[cal_finger][i]){
			obj.disabled = "";
			parentobj.className = parentobj.className.replace("disable","");	
		}else{
			obj.disabled = "disabled";
			parentobj.className = parentobj.className.replace("disable","") + " disable";
		}
	}
	lenght = bondCache.type[0].length;
	for(var i =0;i<lenght;i++){
		var obj = document.getElementById(bondCache.type[0][i]);
		var parentobj = document.getElementById(bondCache.type[0][i]).parentNode;
		if(bondCache.type[cal_finger][cal_type][i]){
			obj.disabled = false;
			parentobj.className = parentobj.className.replace("disable","");	
		}else{
			obj.disabled = true;
			parentobj.className = parentobj.className.replace("disable","") + " disable";
		}
	}
	var cal_today = new Date();
	cal_today = cal_today.getFullYear() + "-" + (cal_today.getMonth()+1)+ "-" + cal_today.getDate();
	document.getElementById("cal_deadline").value = cal_today;
	document.getElementById("cal_buyday").value = cal_today;
	document.getElementById("cal_presellday").value = cal_today;
	document.getElementById("cal_prebuyday").value = cal_today;
	document.getElementById('cal_result').innerHTML = "";
}
function calMmbjBond(){
	var cal_finger = (document.getElementById('cal_figure_0').checked) ? 1 : 2;
	var cal_type = document.getElementById('cal_type').value;
	
	var cal_price = document.getElementById('cal_price').value;
	var cal_freq = document.getElementById('cal_freq').value;
	var cal_month = document.getElementById('cal_month').value;
	var cal_rate = document.getElementById('cal_rate').value;
	var cal_deadline = document.getElementById('cal_deadline').value;
	var cal_cost = document.getElementById('cal_cost').value;
	var cal_buyday = document.getElementById('cal_buyday').value;
	var cal_presellday = document.getElementById('cal_presellday').value;
	var cal_prebuyday = document.getElementById('cal_prebuyday').value;
	
	var msg="作为0方，您的债券最1价格是2元，否则，您的投资回报将低于当前银行利率。";
	var result,Rate;
	if (cal_finger == 1){ //买方
		var HaveMonth=Cal_MonthDiff(Cal_strtodate(cal_prebuyday),Cal_strtodate(cal_deadline));
		Rate=GetRate(HaveMonth);
		switch(parseInt(cal_type))
		{
			//贴现债券
			case 0:
				if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
					alert("请输入正确的债券票面面值!");return false;
				}
				if (cal_deadline==""){
					alert("请输入债券到期兑换日期!");return false;
				}
				if (cal_prebuyday==""){
					alert("请输入预计购入日期!");return false;
				}
				if(Cal_DateDiff(Cal_strtodate(cal_prebuyday),Cal_strtodate(cal_deadline))<0){
					alert("预计购入日期不能晚于债券到期兑换日期！");return false;
				}
				result=CalcBuyTx(cal_price,cal_deadline,cal_prebuyday,Rate);
				break;
				
			//到期一次性还本付息	
			case 1:
				if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
					alert("请输入正确的债券票面面值!");	return false;
				}
				if (cal_month=="" || isNaN(cal_month) || cal_month<=0){
					alert("请输入正确的债券偿还期限!"); return false;
				}
				if (cal_rate=="" || isNaN(cal_rate) || cal_rate<=0){
					alert("请输入正确的债券票面年利率!"); return false;
				}
				if (cal_deadline==""){
					alert("请输入债券到期兑换日期!"); return false;
				}
				if (cal_prebuyday=="" ){
					alert("请输入预计购入日期!"); return false;	
				}
				if(Cal_DateDiff(Cal_strtodate(cal_prebuyday),Cal_strtodate(cal_deadline))<0){
					alert("预计购入日期不能晚于债券到期兑换日期！");return false;
				}
				var RetTerm = parseInt(cal_month);
				result=CalcBuyDq(cal_price,parseFloat(cal_rate)/100,cal_deadline,cal_prebuyday,Rate, RetTerm);
				break;
				
			//固定利率债券和浮动利率债券	
			case 2:
				if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
					alert("请输入正确的债券票面面值!");	return false;
				}
				if (cal_rate=="" || isNaN(cal_rate) || cal_rate<=0){
					alert("请输入正确的债券票面年利率!"); return false;
				}
				if (cal_freq=="" || isNaN(cal_freq) || cal_freq<=0){
					alert("请输入正确的年付息次数!"); return false;
				}
				if (cal_deadline==""){
					alert("请输入债券到期兑换日期!"); return false;
				}
				if (cal_prebuyday==""){
					alert("请输入预计购入日期!"); return false;	
				}
				if(Cal_DateDiff(Cal_strtodate(cal_prebuyday),Cal_strtodate(cal_deadline))<0){
					alert("预计购入日期不能晚于债券到期兑换日期！");return false;
				}
				result=CalcBuyGd(cal_price,parseFloat(cal_rate)/100,cal_freq,cal_deadline,cal_prebuyday,Rate);
				break;
		}
		document.getElementById('cal_result').innerHTML=msg.replace("0","买").replace("1","高买入").replace("2",NBround(result,2).toString());
	}else{//卖方
		var HaveMonth=Cal_MonthDiff(Cal_strtodate(cal_buyday),Cal_strtodate(cal_presellday));
		Rate=GetRate(HaveMonth);
		switch(parseInt(cal_type))
		{
			//贴现债券
			case 0:
				if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
					alert("请输入正确的债券票面面值!");return false;
				}
				if (cal_cost=="" || isNaN(cal_cost) || cal_cost<=0){
					alert("请输入正确的债券成本价格!");return false;
				}
				if (cal_buyday==""){
					alert("请输入债券购入日期!");return false;
				}
				if (cal_presellday==""){
					alert("请输入预计卖出日期!");return false;
				}
				if(Cal_DateDiff(Cal_strtodate(cal_buyday),Cal_strtodate(cal_presellday))<0){
					alert("预计卖出日期不能早于债券购入日期！");return false;
				}
				result=CalcSaleTx(cal_price,cal_deadline,cal_cost,cal_buyday,cal_presellday,Rate);
				break;
			//到期一次性还本付息		
			case 1:
				if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
					alert("请输入正确的债券票面面值!");return false;
				}
				if (cal_rate=="" || isNaN(cal_rate) || cal_rate<=0){
					alert("请输入正确的债券票面年利率!"); return false;
				}
				if (cal_cost=="" || isNaN(cal_cost) || cal_cost<=0){
					alert("请输入正确的债券成本价格!");return false;
				}
				if (cal_buyday==""){
					alert("请输入债券购入日期!");return false;
				}
				if (cal_presellday==""){
					alert("请输入预计卖出日期!");return false;
				}
				if(Cal_DateDiff(Cal_strtodate(cal_buyday),Cal_strtodate(cal_presellday))<0){
					alert("预计卖出日期不能早于债券购入日期！");return false;
				}
				result=CalcSaleDq(cal_price,parseFloat(cal_rate)/100,cal_deadline,cal_cost,cal_buyday,cal_presellday,Rate);
				break;
			//固定利率债券和浮动利率债券	
			case 2:
				if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
					alert("请输入正确的债券票面面值!");return false;
				}
				if (cal_rate=="" || isNaN(cal_rate) || cal_rate<=0){
					alert("请输入正确的债券票面年利率!"); return false;
				}
				if (cal_freq=="" || isNaN(cal_freq) || cal_freq<=0){
					alert("请输入正确的年付息次数!"); return false;
				}
				if (cal_cost=="" || isNaN(cal_cost) || cal_cost<=0){
					alert("请输入正确的债券成本价格!");return false;
				}
				if (cal_buyday==""){
					alert("请输入债券购入日期!");return false;
				}
				if (cal_presellday==""){
					alert("请输入预计卖出日期!");return false;
				}
				if(Cal_DateDiff(Cal_strtodate(cal_buyday),Cal_strtodate(cal_presellday))<0){
					alert("预计卖出日期不能早于债券购入日期！");return false;
				}
				result=CalcSaleGd(cal_price,parseFloat(cal_rate)/100,cal_freq,cal_deadline,cal_cost,cal_buyday,cal_presellday,Rate);
				break;					
		}
		document.getElementById('cal_result').innerHTML=msg.replace("0","卖").replace("1","低卖出").replace("2",NBround(result,2).toString());
	}
}
// 字符串转换为日期 
function Cal_strtodate(str)
{
  var date = Date.parse(str);
  if (isNaN(date)) {
    date = Date.parse(str.replace(/-/g,"/")); // 识别日期格式：YYYY-MM-DD 
    if (isNaN(date)) date = 0;
  }
  return(date);
}

//返回日期间相差的天数
function Cal_DateDiff(Date1, Date2)
{
	return (Date2-Date1)/(24*60*60*1000);
}

var maxpn=99999999;
var maxfn=99999999.9;
var numerrormsg0="请输入0-99999999之内的数字";
var numerrormsg1="请输入1-99999999之内的数字";
var overerrormsg="数值超过最大值99999999";

function DispMessage(CheckCtl,Msg)
{
	if (Msg!="")
	{					
		alert(Msg);					
		CheckCtl.select();
		CheckCtl.focus();
	}
}

//返回日期间相差的月数(最大误差小于一个月)
function Cal_MonthDiff(DateA, DateB)
{
	Date1=new Date();
	Date2=new Date();
	Date1.setTime(DateA);
	Date2.setTime(DateB);
	months = (Date2.getFullYear() - Date1.getFullYear()) * 12;
	addmonths = Date2.getMonth() - Date1.getMonth();
	months = months + addmonths;
	if(Date2.getDate() < Date1.getDate())
		months--;
	return months;
}

function Cal_datevalid(edit,min,max)
{
  // 检查edit是否为大于等于min，小于等于max的有效日期格式字符串。 
  var date = Cal_strtodate(edit);
  if (date == 0) return false;
  if (max) {
    var max = Cal_strtodate(max);
    if ((max!=0)&&(date>max)) return false;
  }
  if (min) {
    var min = Cal_strtodate(min);
    if ((min!=0)&&(date<min)) return false;
  }
  date = new Date(date);
  //edit.value = date.getFullYear() + "-" + (date.getMonth()+1) +
  //			 "-" + date.getDate();
  return true;
}



function GetHaveYear(s, e)
{
	var dt_s = Date.parse(s.replace(/-/g, "/"));
	var dt_e = Date.parse(e.replace(/-/g, "/"));
	return (dt_e - dt_s) / (1000 * 60 * 60 * 24) / 365;
}

function CalcBuyDq(CurrCost, YearRate, EndYears, BuyYears, Rate, RetTerm)
{
	var MaxBuyPrice;
	CurrCost = new Number(CurrCost);
	YearRate = new Number(YearRate);
	Rate = new Number(Rate);
	RetTerm = new Number(RetTerm);
	//2）	到期一次还本付息债券：
	//增加输入项：债券偿还期限，单位为月。该项输入只有在选择了到期一次性还本付息债券以及计算买方时才显示。默认为12个月。
	//最高买入价格＝债券票面面值×（1+债券偿还期限÷12×债券票面年利率）÷（1+银行年利率×0.8）持有年限
	MaxBuyPrice = CurrCost * (1 + RetTerm / 12 * YearRate) / Math.pow(1 + Rate * 0.8, GetHaveYear(BuyYears, EndYears));
	return MaxBuyPrice;
}

function CalcBuyGd(CurrCost, YearRate, Freq, EndYears, BuyYears, Rate)
{
	var MaxBuyPrice, D, WillInterestTimes;
	CurrCost = new Number(CurrCost);
	YearRate = new Number(YearRate);
	Rate = new Number(Rate);
	Freq = new Number(Freq);
	//3）	固定利率附息债券和浮动利率债券：
	//最高买入价格＝债券票面面值÷（1+银行年利率×0.8）持有年限+（债券票面面值×债券票面年利率÷年付息次数）
	//  ×[1－（1+银行年利率×0.8÷年付息次数）－将领取利息次数]÷（银行年利率×0.8÷年付息次数）
	//其中：将领取利息次数＝（债券到期兑换日期－预计买入日期）/（365÷年付息次数）（如有小数，进1位整数，再取整）
	D = GetHaveYear(BuyYears, EndYears) * Freq;
	WillInterestTimes = Math.ceil(D);
	MaxBuyPrice = CurrCost / Math.pow(1 + Rate * 0.8, GetHaveYear(BuyYears, EndYears)) + (CurrCost * YearRate / Freq)
			* (1 - Math.pow(1 + Rate * 0.8 / Freq, - WillInterestTimes)) / (Rate * 0.8 / Freq);
	return MaxBuyPrice;
}

function CalcBuyTx(CurrCost, EndYears, BuyYears, Rate)
{
	var MaxBuyPrice;
	CurrCost = new Number(CurrCost);
	Rate = new Number(Rate);
	//1）	贴现债券：
	//最高买入价格＝债券票面面值÷（1+银行年利率×持有年限×0.8）
	MaxBuyPrice = CurrCost / (1 + Rate * GetHaveYear(BuyYears, EndYears) * 0.8);
	return MaxBuyPrice;
}

function CalcSaleDq(CurrCost, YearRate, EndYears, Cost, BuyYears, SaleYears, Rate)
{
	var MinSalePrice;
	CurrCost = new Number(CurrCost);
	YearRate = new Number(YearRate);
	Cost = new Number(Cost);
	Rate = new Number(Rate);
	//2）	到期一次还本付息债券：
	//最低卖出价格＝债券成本价格×（1+银行年利率×0.8）持有年限
	MinSalePrice = Cost * Math.pow(1 + Rate * 0.8, GetHaveYear(BuyYears, SaleYears));
	return MinSalePrice;
}

function CalcSaleGd(CurrCost, YearRate, Freq, EndYears, Cost, BuyYears, SaleYears, Rate)
{
	var MinSalePrice, D, AlreadyInterestedTimes;
	CurrCost = new Number(CurrCost);
	YearRate = new Number(YearRate);
	Cost = new Number(Cost);
	Rate = new Number(Rate);
	Freq = new Number(Freq);
	//3）	固定利率附息债券和浮动利率债券：
	//最低卖出价格＝债券成本价格×（1+银行年利率×0.8）持有年限－
	//  （债券票面面值×债券票面年利率÷年付息次数）×[（1+银行年利率×0.8÷年付息次数）已领取利息次数－1]
	//  ÷（银行年利率×0.8÷年付息次数）
	//已领取利息次数＝（预计卖出日期－债券购入日期）/（365÷年付息次数）（如有小数，取整数部分）
	D = GetHaveYear(BuyYears, SaleYears) * Freq;
	AlreadyInterestedTimes = Math.floor(D);
	MinSalePrice = Cost * Math.pow(1 + Rate * 0.8, GetHaveYear(BuyYears, SaleYears))
		- (CurrCost * YearRate / Freq) * (Math.pow(1 + Rate * 0.8 / Freq, AlreadyInterestedTimes) - 1)
		/ (Rate * 0.8 / Freq);
	return MinSalePrice;
}

function CalcSaleTx(Currcost, EndYears, Cost, BuyYears, SaleYears, Rate)
{
	var MinSalePrice;
	Currcost = new Number(Currcost);
	Cost = new Number(Cost);
	Rate = new Number(Rate);
	//1）	贴现债券：
	//最低卖出价格＝债券成本价格×银行年利率×持有年限×0.8+债券成本价格
	MinSalePrice = Cost * Rate * GetHaveYear(BuyYears, SaleYears) * 0.8 + Cost;
	return MinSalePrice;
}


function GetRate(month)
{
	if (month == 0) month = 0.1;
	if (month > 60) month = 60;	// 整存整取最大期限
	return GetRMBSaveRatio("2", month) / 100; 
}

//人民币---(存款方式，存期) return 利率
function GetRMBSaveRatio(typeID, period, xmlDoc)  
{			
	if(typeID == "" || period == "")
	{
		alert("缺少存款方式和存期");
		return;
	}	
	var result=3.6; //2008-12-25 调整,整存整取
	return result;
}

function Trim(strSource) 
{
	return 	strSource.replace(/^\s*/,'').replace(/\s*$/,'');
}

//四舍五入函数，为了兼顾IE5（参数：欲转换数字，小数点后几位）返回NUMBER
function NBround(nb,len)
{
  var strnb=new String(nb);
  if (nb < 0.0000001) return new Number(0); // 小于0.1E-7的按0处理
  pos = strnb.indexOf(".");
  if ((pos == -1) || (strnb.length-pos-1)<len)
    return new Number(strnb);
  else 
  {
    var last = strnb.substring(pos+len+1,pos+len+2);
    var nblast = new Number(last);
    if (nblast<5)
      return new Number(strnb.substring(0,pos+len+1));
    else
       {
           if (strnb.substring(0,1)=="-")
              return new Number(new String(new Number(strnb.substring(0,pos+len+1))-Math.pow(10,-1*len)).substring(0,pos+len+1));
          else
          return new Number(new String(new Number(strnb.substring(0,pos+len+1))+Math.pow(10,-1*len)).substring(0,pos+len+1));
      //return new Number(strnb.substring(0,pos+len+1))+Math.pow(10,-1*len);
       }
  }
}

/*债券持有期计算器
*/

//初始化选项[选项更更改时更新]
function initCyWinBond(){
	var cal_type = document.getElementById('cal_type').value;
	var cal_paymethod = document.getElementById('cal_paymethod').value;
	var cal_today = new Date();
	cal_today = cal_today.getFullYear() + "-" + (cal_today.getMonth()+1)+ "-" + cal_today.getDate();
	document.getElementById("cal_payday").value  = cal_today;
	document.getElementById("cal_buyday").value  = cal_today;
	document.getElementById("cal_sellday").value = cal_today;
	document.getElementById("cal_result").value = "计算得出";
	var obj = parentobj = null;
	if (cal_type==1){
		///贴现模式下，只能一次还本付息
		cal_paymethod = 2; 
		document.getElementById('cal_paymethod').options[1].selected = true;
		
		obj = document.getElementById('cal_price');
		obj.disabled = true;
		obj.value = "不填";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
		obj = document.getElementById('cal_rate');
		obj.disabled = true;
		obj.value = "不填";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
	}else{
		obj = document.getElementById('cal_price');
		obj.disabled = false;
		obj.value = "";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + "";
		obj = document.getElementById('cal_rate');
		obj.disabled = false;
		obj.value = "";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + "";
	}
	if (cal_paymethod==2){
		obj = document.getElementById('cal_payday');
		obj.disabled = true;
		obj.value = cal_today;
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
		obj = document.getElementById('cal_freq');
		obj.disabled = true;
		obj.value = "不填";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
	}else{
		obj = document.getElementById('cal_payday');
		obj.disabled = false;
		obj.value = cal_today;
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + "";
		obj = document.getElementById('cal_freq');
		obj.disabled = false;
		obj.value = "";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + "";
	}
}

function calCyWinBond(){
	var cal_type = document.getElementById('cal_type').value;
	var cal_paymethod = document.getElementById('cal_paymethod').value;
	var cal_price = document.getElementById('cal_price').value;
	var cal_rate = document.getElementById('cal_rate').value;
	var cal_payday = document.getElementById('cal_payday').value;
	var cal_buyday = document.getElementById('cal_buyday').value;
	var cal_buyprice = document.getElementById('cal_buyprice').value;
	var cal_sellday = document.getElementById('cal_sellday').value;
	var cal_sellprice = document.getElementById('cal_sellprice').value;
	var cal_freq = document.getElementById('cal_freq').value;
	if (cal_type=="1"){cal_paymethod=2};
	if ((cal_type=="2") && (cal_price=="" || isNaN(cal_price) || cal_price<=0)){
		alert("请输入正确的债券票面面值!");return false;
	}
	if ((cal_type=="2") && (cal_rate=="" || isNaN(cal_rate) || cal_rate<=0)){
		alert("请输入正确的附息债券利率!");return false;
	}
	if ((cal_paymethod=="1") && (cal_payday=="" || !Cal_datevalid(cal_payday))){
		alert("请输入正确的债券到期日!");return false;
	}
	if (cal_buyday=="" || !Cal_datevalid(cal_buyday)){
		alert("请输入正确的债券买入日期!");return false;
	}
	if (cal_buyprice=="" || isNaN(cal_buyprice) || cal_buyprice<=0){
		alert("请输入正确的债券买入价格!");return false;
	}
	if (cal_sellprice=="" || isNaN(cal_sellprice) || cal_sellprice<=0){
		alert("请输入正确的债券卖出价格!");return false;
	}
	if (cal_sellday=="" || !Cal_datevalid(cal_sellday)){
		alert("请输入正确的债券卖出日期!");return false;
	}
	if ((cal_paymethod=="1") && (cal_freq=="" ||  isNaN(cal_freq) || cal_freq<=0)){
		alert("请输入正确的利息支付频率!");return false;
	}
	if ((cal_paymethod=="1") && (cal_freq>99)){
		alert("债券年利息支付频率不能大于2位数!");return false;
	}
	if(Cal_DateDiff(Cal_strtodate(cal_buyday),Cal_strtodate(cal_sellday))<=0){
		alert("债券卖出日期不能早于债券买入日期！");return false;
	}
	//开始计算
	var FirstPayDate = limitdate = new Date();
	if((cal_type==2)&&(cal_paymethod==1))
	{
		//计算第一次付息日
		limitdate = new Date(Cal_strtodate(cal_payday))
		FirstPayDate = CalcPayDate(limitdate, cal_buyday, cal_freq);
	}
	var BondType = cal_type;
	var PayType =  cal_paymethod;
	
	var BuyYears = new Date();
	var SaleYears = new Date();
	var BuyPrice = parseFloat(cal_buyprice);
	var SalePrice = parseFloat(cal_sellprice);
	var FxRate = parseFloat(cal_rate)/100;
	var Cost = parseInt(cal_price);
	var Freq = cal_freq;
	
	BuyYears.setTime(Cal_strtodate(cal_buyday));
	SaleYears.setTime(Cal_strtodate(cal_sellday));
	
	var DiffYear= Cal_DateDiff(BuyYears,SaleYears)/365;//持有年限＝（卖出日期—买入日期）/365
	var w,n,y;
	var isetp=0.0001;//误差上限
	var s=0.001;//黄金下限值
	var e=1;//黄金上限值
	var pv=0;//收益率计算所得的购买价格
	var tDays;
	tDays=Cal_DateDiff(BuyYears,FirstPayDate);//债券交割日距下一次付息日的实际天数
	if(BondType==2)	    // 付息债券
	{
		if (PayType==1) // 按年付息
		{
			w=tDays*Freq/365;//债券交割日距下一次付息日的实际天数 * 年付息频率 / 365			
			n=parseInt(Cal_DateDiff(FirstPayDate,SaleYears)	/365*Freq);//剩余的付息次数=1+[(卖出日 - 首次付息日)	/365 * 年付息频率]取整，不舍入
			if(FirstPayDate<=SaleYears)//如果第一次付息日早与卖出日期则计算为付息次数+1
				n = n+1;
			if(n>0)//如果购买期间有付息
			{
				y=(e-s)/2;//收益率初次估算值
				while ((Math.abs(pv-BuyPrice)>isetp)&&(Math.abs(e-s)>isetp))
				{
					pv=Calc(y,w,n,Cost*FxRate,Freq,SalePrice, DiffYear);
					if (pv==0) 
						break;
					if (pv<BuyPrice) 
					{
						e=y;
						y=(s+e)/2;
					}
					if (pv>BuyPrice)
					{
						s=y;
						y=(s+e)/2;
					}
				}
			}
			else//购买时间内无付息
			{
				y=(((SalePrice - BuyPrice)/DiffYear)/BuyPrice);
			}
			rate=y;
		}
		else // 一次还本付息
			rate=(((SalePrice - BuyPrice)/DiffYear)/BuyPrice);
	}
	else // 贴现债券
	{
			//if ((BuyPrice==0)||(BuyPrice<0)) return -1;		
			rate=(((SalePrice - BuyPrice)/DiffYear)/BuyPrice);
	}
	rate = NBround(rate*100,2);
	document.getElementById('cal_result').value = rate;
}
function Calc(y, w, n, C, f, M, diffDay)
{
	var PV=0;
	for (var i=0;i<=n-1;i++)
	{
		PV=PV+(C/f)/Math.pow((1+y/f),i+w);
	}
	PV=PV+ M/Math.pow((1+y/f),diffDay);

	return PV;
}

/*根据债券到期日计算首次付息日
EndDate:债券到期日
BuyDate:债券购买日 
PayFreq:年付息平率（次/年）
思路：假设购买年=第一次付息年，根据年付息频率估算付息年所有的付息日；
比较付息日与购买日的天数差，取最小的正整数差得付昔日作为第一次付息日。
*/
function CalcPayDate(limitdate, buydate, PayFreq)
{
	var BuyDate = new Date(Cal_strtodate(buydate));
	var EndDate = new Date(Cal_strtodate(limitdate));
	var PayDiffDays = Math.ceil(365/PayFreq);
	var tmpPayDate=new Array();
	var diff=new Array();
	var i;
	for(i=0; i<PayFreq; i++)
	{
		tmpPayDate[i] = new Date(BuyDate.getFullYear(), EndDate.getMonth(), EndDate.getDate()+new Number((i+1)*PayDiffDays+1));
		diff[i] = (tmpPayDate[i]-BuyDate)/(60*60*24*1000);
	}
	var tmpdiff=365;
	var nearDate=tmpPayDate[0];
	for(i=0; i<PayFreq; i++)
	{
		if(diff[i]<tmpdiff && diff[i]>0)
		{
			tmpdiff=diff[i];
			nearDate = tmpPayDate[i];
		}
	}
	return nearDate;
}


/* 认购收益率计算器
 */
function initRgWinBond(){
	var cal_type = (document.getElementById("cal_type_1").checked) ? 1 : 0;
		cal_type = (document.getElementById("cal_type_2").checked) ? 2 : cal_type;
	var cal_today = new Date();
		cal_today = cal_today.getFullYear() + "-" + (cal_today.getMonth()+1)+ "-" + cal_today.getDate();
	var obj = parentobj = null;
	if (cal_type==0){
		obj = document.getElementById('cal_rate');
		obj.disabled = true;
		obj.value = "不填";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
		obj = document.getElementById('cal_buyday');
		obj.disabled = true;
		obj.value = cal_today;
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
		obj = document.getElementById('cal_freq');
		obj.disabled = true;
		obj.value = "1";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
	}else if(cal_type==1){
		obj = document.getElementById('cal_rate');
		obj.disabled = false;
		obj.value = "";
		obj.parentNode.className = obj.parentNode.className.replace("disable","");
		obj = document.getElementById('cal_buyday');
		obj.disabled = true;
		obj.value = cal_today;
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
		obj = document.getElementById('cal_freq');
		obj.disabled = true;
		obj.value = "1";
		obj.parentNode.className = obj.parentNode.className.replace("disable","") + " disable";
	}else{
		obj = document.getElementById('cal_rate');
		obj.disabled = false;
		obj.value = "";
		obj.parentNode.className = obj.parentNode.className.replace("disable","");
		obj = document.getElementById('cal_buyday');
		obj.disabled = false;
		obj.value = cal_today;
		obj.parentNode.className = obj.parentNode.className.replace("disable","");
		obj = document.getElementById('cal_freq');
		obj.disabled = false;
		obj.value = "1";
		obj.parentNode.className = obj.parentNode.className.replace("disable","");	
	}
	document.getElementById("cal_result").value = "计算得出";
}

function calRgWinBond(){
	var cal_type = (document.getElementById("cal_type_1").checked) ? 1 : 0;
		cal_type = (document.getElementById("cal_type_2").checked) ? 2 : cal_type;
	var cal_cost = document.getElementById("cal_cost").value;
	var cal_price = document.getElementById("cal_price").value;
	var cal_year = document.getElementById("cal_year").value;
	var cal_rate = document.getElementById("cal_rate").value;
	var cal_buyday = document.getElementById("cal_buyday").value;
	var cal_freq = document.getElementById("cal_freq").value;
	
	if (cal_cost=="" || isNaN(cal_cost) || cal_cost<=0){
		alert("请输入正确的债券票面面值!");return false;
	}
	if (cal_price=="" || isNaN(cal_price) || cal_price<=0){
		alert("请输入正确的债券认购价格!");return false;
	}
	if (cal_year=="" || isNaN(cal_year) || cal_year<=0){
		alert("请输入正确的债券期限!");return false;
	}
	if ((cal_type>0) && (cal_rate=="" || isNaN(cal_rate) || cal_rate<=0)){
		alert("请输入正确的票面利率!");return false;
	}
	if ((cal_type>1) && (cal_buyday=="" || !Cal_datevalid(cal_buyday))){
		alert("请输入正确的认购日期!");return false;
	}
	if ((cal_type>1) && (cal_freq=="" || isNaN(cal_freq) || cal_freq<=0)){
		alert("请输入正确的利息支付频率(次/年)!");return false;
	}
	
	/// 债券面额：元（正整数；无默认值）
	var Cost=0;
	///  票面利率： %（正数，保留两位小数；债券种类为贴现，则不显示；无默认值）
	var Rate=0;
	///	认购价格：元（正整数；无默认值）
	var BuyPrice=0;
	///	债券期限：年（正整数）
	var Years=0;
	///	认购日期：年/月/日
	var BuyDate= new Date();
	/// 债券每年的利息支付频率: 　  次，正整数
	var Freq=0;
	/// cal_type  1、贴现债券
	///		     2、到期一次还本付息债券 
	///          3、固定利率附息债券和浮动利率债券
	var w,m;
	var pv,x,s,e,isetp,ret=0;
	var CurrDate=new Date();
			
	//贴现债券
	if (cal_type==0)
	{
		Cost=parseFloat(cal_cost);
		BuyPrice=parseFloat(cal_price);
		Years=parseInt(cal_year);
	 } 
	//到期一次还本付息债券
	 if (cal_type==1)
	 {
		Cost=parseFloat(cal_cost);
		BuyPrice=parseFloat(cal_price);
		Years=parseInt(cal_year);
		Rate=parseFloat(cal_rate)/100;
	}
	//固定利率和浮动利率
	if (cal_type==2)
	{
		Cost=parseFloat(cal_cost);
		BuyPrice=parseFloat(cal_price);
		Years=parseInt(cal_year);
		Rate=parseFloat(cal_rate)/100;
		BuyDate=Cal_strtodate(cal_buyday);
		Freq=parseInt(cal_freq);
		CurrDate = new Date(BuyDate);
		CurrDate.setYear(CurrDate.getYear()+Years);
	}
	
	var Calc=function(x,w,m,Cost,Rate,Freq){
		var y=0;
		for (i=w;i<=w+m-1;i++)
			y=y+(Cost*Rate/Freq)/Math.pow((1+x/Freq),i);
		y=y+(Cost/Math.pow((1+x/Freq),(w+m-1)));
		return y;
	}
	
	switch(cal_type)
	{
		case 0:
			ret=(Cost-BuyPrice*1.0)/(BuyPrice*Years);
			break;
		case 1:
			ret= Math.pow((Cost+Years*Cost*Rate)/BuyPrice,1.0/Years)-1;
			break;
		case 2:
			m=Years*Freq;
			w=1;
			isetp=0.0001;
			s=0.001;
			e=1;
			pv=0;						
			x=(1-isetp)/2;
			while ((Math.abs(pv-BuyPrice)>0.001)&&(Math.abs(e-s)>isetp))
			{
				pv=Calc(x,w,m,Cost,Rate,Freq);
				if (pv==0)
					break;
				if (pv<BuyPrice) 
				{
					e=x;
					x=s+(e-s)/2;
				}
				if (pv>BuyPrice)
				{
					s=x;
					x=s+(e-s)/2;
				}
			}
			ret=x;
			break;
	}
	document.getElementById("cal_result").value = NBround(ret*100,2);
}

/*债券收益率计算器
 */
function calWinbond(type){
	//计算购买收益率
	if (type==0){
		if(!CheckElem(document.getElementById("cal_cost_0"), "债券面值")) return false;
		if(!CheckElem(document.getElementById("cal_buyprice_0"), "买入价格")) return false;
		if(!CheckElem(document.getElementById("cal_day_0"), "到期时间")) return false;
		if(!CheckElem(document.getElementById("cal_rate_0"), "票面年利率")) return false;
		
		var a = parseFloat(document.getElementById("cal_cost_0").value);
		var b = parseFloat(document.getElementById("cal_buyprice_0").value);
		var f = parseFloat(document.getElementById("cal_day_0").value);
		var i = parseFloat(document.getElementById("cal_rate_0").value)/100;
		
		var r = (a+a*i*f/365-b)/(b*f/365);
		document.getElementById("cal_result_0").value = NBround(r*100,2);
		
	//计算出售收益率俄	
	}else if(type==1){
		if(!CheckElem(document.getElementById("cal_cost_1"), "发行价格")) return false;
		if(!CheckElem(document.getElementById("cal_sellprice_1"), "卖出价格")) return false;
		if(!CheckElem(document.getElementById("cal_day_1"), "持有时间")) return false;
		if(!CheckElem(document.getElementById("cal_rate_1"), "票面年利率")) return false;
	
		var t = parseFloat(document.getElementById("cal_cost_1").value);
		var c = parseFloat(document.getElementById("cal_sellprice_1").value);
		var d = parseFloat(document.getElementById("cal_day_1").value);
		var i = parseFloat(document.getElementById("cal_rate_1").value)/100;
	
		var r = (c-t+d*t*i/365)/(t*d/365);
		document.getElementById("cal_result_1").value = NBround(r*100,2);
		
	//计算持有期间收益率
	}else if(type==2){
		if(!CheckElem(document.getElementById("cal_cost_2"), "债券面值")) return false;
		if(!CheckElem(document.getElementById("cal_buyprice_2"), "买入价格")) return false;
		if(!CheckElem(document.getElementById("cal_sellprice_2"), "卖出价格")) return false;
		if(!CheckElem(document.getElementById("cal_day_2"), "持有时间")) return false;
		if(!CheckElem(document.getElementById("cal_rate_2"), "票面年利率")) return false;
		
		var a = parseFloat(document.getElementById("cal_cost_2").value);
		var b = parseFloat(document.getElementById("cal_buyprice_2").value);
		var c = parseFloat(document.getElementById("cal_sellprice_2").value);
		var d = parseFloat(document.getElementById("cal_day_2").value);
		var i = parseFloat(document.getElementById("cal_rate_2").value)/100;
		
		var r = (c-b+a*i*d/365)/(b*d/365);
		document.getElementById("cal_result_2").value = NBround(r*100,2);		
	}
}

//判断公式一
function CheckElem(curObj, msg){
	if(msg==null) msg="";
	if(curObj.value==''){
		alert(msg + "不可为空!");
		curObj.focus();
		curObj.select();
		return false;
	}else if(isNaN(curObj.value)){
		alert(msg + "必须为数字!");
		curObj.focus();
		curObj.select();
		return false;
	}else{
		return true;
	}
}

/*	功能：    校验一个值是否为空
	入口参数：	
	CheckCtl: 要校验的输入框
	disptext: 出错显示的信息
*/
function CheckEmpty(CheckCtl,disptext,page)
{				
	if (Trim(CheckCtl.value)=="" )
	{
		if (page)
		 showguide(page);
		DispMessage(CheckCtl,disptext);	
		return false;
	}
	else
	  return true;
}
function CheckFN3(CheckCtl,disptext,IsCanZero,page,floatcount)
{					
if ( CheckFN(CheckCtl,disptext,page,floatcount) )
 {
	if ( (parseFloat(CheckCtl.value)==0) &&(!IsCanZero) )
		{
			if (page)
				showguide(page);
			DispMessage(CheckCtl,disptext);
			return false;
		}
	else return true;	
 }		
else
 return false;
}
/*功能： 校验一个合法的大于等于0的浮点数
入口参数：	
			CheckCtl: 要校验的输入框
			disptext: 出错显示的信息	
			floatcount: 小数的最高位数（如果没有该参数，则默认为2位）
			如果没有page参数，有floatcunt参数则：把page 置null
			如:	CheckFN(CheckCtl,"出错显示的信息",null,5)				*/
function CheckFN(CheckCtl,disptext,page,floatcount)
{					
	var s=new String(Trim(CheckCtl.value));
	temp=parseFloat(s);
	var result=true;
	if( (isNaN(temp)) || (temp< 0)||(temp!=s) )
	{					
		result=false;
	}	
	else if (temp>maxfn) 
	{
		result=false;
		disptext=overerrormsg;
	}
	else
	{ 	 					
		limitcount=floatcount?floatcount:2;
		var array=s.split(".");
		if (array[1]==null)
		count=-1;
		else
		{
			var str=new String(array[1]);
			count=str.length;
		}
		if (count>limitcount)
		{
			if (page)
				showguide(page);
			alert("小数位数超过"+limitcount+"位"); 
			CheckCtl.select();
			CheckCtl.focus();
			return false;
		}
	 }	
	 if (!result)
	 {
		if (page)
		 showguide(page);
		DispMessage(CheckCtl,disptext);
		return false;
	 }			
		return true;				
}

/*	功能： 校验一个正整数
入口参数：	
CheckCtl: 要校验的输入框
disptext: 出错显示的信息
IsCanZero : 是否可以为零*/
function CheckPN(CheckCtl,disptext,IsCanZero,page) 
{   
   
	var s=new String(Trim(CheckCtl.value));
	var temp=parseInt(s);
	var result=true;
	if (  (isNaN(temp)) || (temp<0) || ( s.indexOf(".")>=0 )||(temp!=s))
	{
		result=false;
	}				
	else if ( (!IsCanZero)&&(temp==0) )
	 {
		result=false;
	 }
	if  (temp>maxpn) 
	{
		result=false;
		disptext=overerrormsg;
	}
	 if (!result)
	 {
		if (page)
		 showguide(page);
		DispMessage(CheckCtl, disptext);
		return false;
	}					
	 return true;
	 
}

/*债券到期收益计算器
 */
function initTimWinBond(){
	var cal_today = new Date();
	cal_today = cal_today.getFullYear() + "-" + (cal_today.getMonth()+1)+ "-" + cal_today.getDate();
	document.getElementById("cal_buyday_0").value = cal_today;
	document.getElementById("cal_sellday_0").value = cal_today;
	document.getElementById("cal_buyday_1").value = cal_today;
	document.getElementById("cal_sellday_1").value = cal_today;
	document.getElementById("cal_buyday_2").value = cal_today;
	document.getElementById("cal_sellday_2").value = cal_today;
	
}
function calTimWinBond(){
	if(document.getElementById("cal_type_0").checked){
		if (!CheckFN3(document.getElementById("cal_cost_0"),"请在[债券单位成本]输入正数",false))
			return false;	       		    
		if (!CheckFN3(document.getElementById("cal_price_0"),"请在[债券单位面值]输入正数",false))
			return false;
		if(!CheckEmpty(document.getElementById("cal_buyday_0"),"[债券购买交割日期]不能为空！"))
			return false;
		if(!CheckEmpty(document.getElementById("cal_sellday_0"),"[债券到期兑付日期]不能为空！"))
			return false;		
		var BuyDate=new Date();
		BuyDate.setTime(Cal_strtodate(document.getElementById("cal_buyday_0").value));				
		var SellDate=new Date();
		SellDate.setTime(Cal_strtodate(document.getElementById("cal_sellday_0").value));			
		if (BuyDate>=SellDate)
		{
			alert("[债券到期兑付日]应当晚于[购买交割日]");
			return false;
		}
		if (document.getElementById("paymod_1").checked)		
		{
			if ( !CheckFN3(document.getElementById("cal_mod1_rate"),"请在[债券票面年利率]输入非负数",true))
				return false;
			if ( !CheckPN(document.getElementById("cal_mod1_year"),"请在[债券偿还期限]输入正整数",false))
				return false;
		}      
		if (document.getElementById("paymod_2").checked)
		{
		if (!CheckFN3(document.getElementById("cal_mod2_rate"),"请在[债券票面年利率]输入非负数",true))
			return false;    
		if (!CheckPN(document.getElementById("cal_mod2_freq"),"请在[利息支付频率]输入正整数",false))
			return false;	       		    	    
		}   	
	}
	if(document.getElementById("cal_type_1").checked)
	 {
		if (!CheckFN3(document.getElementById("cal_cost_1"),"请在[债券单位成本]输入正数",false))
			return false;	       		    
		if(!CheckEmpty(document.getElementById("cal_buyday_1"),"[债券购买交割日期]不能为空！"))
			return false;
		if(!CheckEmpty(document.getElementById("cal_sellday_1"),"[债券到期兑付日期]不能为空！"))
			return false;		
		var BuyDate=new Date();
		BuyDate.setTime(Cal_strtodate(document.getElementById("cal_buyday_1").value));				
		var SellDate=new Date();
		SellDate.setTime(Cal_strtodate(document.getElementById("cal_sellday_1").value));			
		if (BuyDate>=SellDate)
		{
			alert("[债券到期兑付日]应当晚于[购买交割日]");
			return false;
		}		
		if (!CheckFN3(document.getElementById("cal_unitprice_1"),"请在[债券单位面值输入]正数",false))
			return false;		
		if (!CheckFN3(document.getElementById("cal_rate_1"),"请在[债券票面年利率输入]非负数",true))
			return false;
		if (!CheckPN(document.getElementById("cal_year_1"),"请在[债券偿还期限]输入正整数",false))
			return false;
			
	
	}					
	if(document.getElementById("cal_type_2").checked)
	 {
		if (!CheckFN3(document.getElementById("cal_cost_2"),"请在[债券单位成本]输入正数",false))
			return false;	       		    
		if(!CheckEmpty(document.getElementById("cal_buyday_2"),"[债券购买交割日期]不能为空！"))
			return false;
		if(!CheckEmpty(document.getElementById("cal_sellday_2"),"[债券到期兑付日期]不能为空！"))
			return false;		
		var BuyDate=new Date();
		BuyDate.setTime(Cal_strtodate(document.getElementById("cal_buyday_2").value));				
		var SellDate=new Date();
		SellDate.setTime(Cal_strtodate(document.getElementById("cal_sellday_2").value));			
		if (BuyDate>=SellDate)
		{
			alert("[债券到期兑付日]应当晚于[购买交割日]");
			return false;
		}		
		if (!CheckFN3(document.getElementById("cal_unitprice_2"),"请在[债券单位面值]输入正数",false))
			return false;		
		if (!CheckFN3(document.getElementById("cal_rate_2"),"请在债券票面年利率输入非负数",true))
			return false;
		if (!CheckPN(document.getElementById("cal_freq_2"),"请在利息支付频率输入正整数",false))
			return false;	       		    	            
	
	}
	if (document.getElementById("cal_type_0").checked)
	{
		if (document.getElementById("paymod_0").checked)
		{
			//贴现
		   CalcBond11(0);
		}
		if (document.getElementById("paymod_1").checked)
		{
			//一次还本付息
			CalcBond11(1);
		}
		if (document.getElementById("paymod_2").checked)
		{
			//定期支付
			CalcBond11(2);
		}
	}
	if (document.getElementById("cal_type_1").checked)
	{
		//剩余流通期限在一年以上的到期一次还本付息债券
		CalcBond21();
	}
	if (document.getElementById("cal_type_2").checked)
	{
		//不处于最后付息周期的固定利率附息债券和浮动利率债券
		CalcBond31();
	}
  return false;
}

function CalcBond11(Method)
{
	var Year = 0,Freq = 0,UnitPrice = 0;		//int
	var UnitCost,Rate = 0;		//double
	var BuyDate=new Date();
	var SellDate=new Date();
	
	UnitCost = parseFloat(document.getElementById("cal_cost_0").value);
	UnitPrice = parseInt(document.getElementById("cal_price_0").value);
	BuyDate.setTime(Cal_strtodate(document.getElementById("cal_buyday_0").value));
	SellDate.setTime(Cal_strtodate(document.getElementById("cal_sellday_0").value));
	if(Method == 1)
	{
		Rate = parseFloat(document.getElementById("cal_mod1_rate").value)/100;
		Year = parseInt(document.getElementById("cal_mod1_year").value);
	}
	else if(Method == 2)
	{
		Rate = parseFloat(document.getElementById("cal_mod2_rate").value)/100;
		Freq = parseInt(document.getElementById("cal_mod2_freq").value);
	}
	
	
	Excute(UnitCost,BuyDate,SellDate,UnitPrice,Rate,Year,Freq,Method);
}

function CalcBond21()
{
	var Year,UnitPrice;
	var UnitCost,Rate;
	var BuyDate=new Date();
	var SellDate=new Date();
	
	UnitCost = parseFloat(document.getElementById("cal_cost_1").value);
	UnitPrice = parseInt(document.getElementById("cal_unitprice_1").value);
	BuyDate.setTime(Cal_strtodate(document.getElementById("cal_buyday_1").value));
	SellDate.setTime(Cal_strtodate(document.getElementById("cal_sellday_1").value));
	Rate = parseFloat(document.getElementById("cal_rate_1").value)/100;
	Year = parseInt(document.getElementById("cal_year_1").value);

	//alert(UnitCost+"-"+UnitPrice+"-"+BuyDate+"-"+SellDate+"-"+Rate+"-"+Year);
	Excute(UnitCost,BuyDate,SellDate,UnitPrice,Rate,Year,0,3);
}

function CalcBond31()
{
	var Freq,UnitPrice;
	var UnitCost,Rate;
	var BuyDate=new Date();
	var SellDate=new Date();
	
	UnitCost = parseFloat(document.getElementById("cal_cost_2").value);
	UnitPrice = parseInt(document.getElementById("cal_unitprice_2").value);
	BuyDate.setTime(Cal_strtodate(document.getElementById("cal_buyday_2").value));
	SellDate.setTime(Cal_strtodate(document.getElementById("cal_sellday_2").value));
	Rate = parseFloat(document.getElementById("cal_rate_2").value)/100;
	Freq = parseInt(document.getElementById("cal_freq_2").value);

	Excute(UnitCost,BuyDate,SellDate,UnitPrice,Rate,0,Freq,4);
}


function Excute(Cost,BondBuyDate,BondEndDate,EndCost,BondRate,YearTimes,Freq,options)
{
	var w,m,tDays=0;	//int
	var l,pv,x,s,e,isetp;	//double
	var CurrDate=new Date(BondBuyDate.getFullYear(),0,1);
	var BondEndRate;
	
	var Calc = function(x, w, m, EndCost, BondRate, Freq){
		var y=0;
		for (var i=0;i<=m-1;i++)
			y=y+((EndCost*BondRate)/Freq)/Math.pow((1+x/Freq),i+w);
		y=y+(EndCost/Math.pow((1+x/Freq),(w+m-1)));
		
		return y;
	}

	tDays=Cal_DateDiff(BondBuyDate,BondEndDate)+1;
	
	switch(options)
	{
		case 0:
			BondEndRate=(EndCost-Cost)/Cost*365/tDays;
			break;
		case 1:
			BondEndRate=(EndCost+YearTimes*EndCost*BondRate-Cost)/Cost*365/tDays;
			break;
		case 2:
			BondEndRate=((EndCost+EndCost*BondRate/Freq)-Cost)/Cost*365.0/tDays;
			break;
		case 3:
			BondEndRate=Math.pow((EndCost+EndCost*YearTimes*BondRate)/Cost,365.0/tDays)-1;
			break;
		case 4:
			l=tDays*Freq/365;
			m=parseInt(l + 1);
			w= tDays % (365/Freq) / (365/Freq);
			isetp=0.0001;
			s=0.001;
			e=1;
			pv=0;						
			x=(e-s)/2;
			while ((Math.abs(pv-Cost)>0.001)&&(Math.abs(e-s)>isetp))
			{
				pv=Calc(x,w,m,EndCost,BondRate,Freq);
				if (pv==0) break;
				if (pv<Cost) 
				{
					e=x;
					x=(s+e)/2;
				}
				if (pv>Cost)
				{
					s=x;
					x=(s+e)/2;
				}
			}
			BondEndRate=x;
			break;
	}
	document.getElementById("cal_result").value = NBround(BondEndRate*100,2);
}



			