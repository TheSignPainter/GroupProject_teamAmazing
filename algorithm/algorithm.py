import csv
import numpy as np
from  datetime import date

class Bond():
    def __init__(self, yieldToMaturity=0.01, parValue=100, buyDate=date(2008, 12, 15), buyPrice = 100, startDate=date(1996, 12, 15) ,maturity=date(2018, 12, 15), frequency=1, ir = 0.03, epsilon = 0.000001):
        self.yieldToMaturity = float(yieldToMaturity)
        self.parValue = float(parValue)
        self.buyDate = buyDate
        self.buyPrice = float(buyPrice)
        self.startDate = startDate
        self.maturity = maturity
        self.frequency = frequency
        self.ir = float(ir)
        self.epsilon = epsilon
        self.pv_clean = float(0)
        self.pv_dirty = float(0)
        self.coupon = float(self.ir * self.parValue) / frequency
        # 默认只有年付和半年付
        if frequency == 1:
            self.payDate = [[startDate.month, startDate.day]]
        elif frequency == 2:
            self.payDate = [[startDate.month, startDate.day], [(startDate.month+6)%12, startDate.day]]
            if self.payDate[1][0] == 0:
                self.payDate[1][0] == 12
            # paytime排序
            if self.payDate[0][0] > self.payDate[1][0]:
                self.payDate[0], self.payDate[1] = self.payDate[1], self.payDate[0]
        self.remainingPayTimes = self.computePayTimes()
        self.daysPastLastPay, self.daysToNextPay = self.computeDaysToPay()
        self.pv_clean, self.pv_dirty = self.presentValue() 
        self.pv_dirty_ = self.presentValue2()
        self.duration, self.modifiedD = self.computeDuration()
        self.convexity = self.computeConvexity()
        self.computed_YTM = self.computeYTM()
        
    def computePayTimes(self):
        if self.frequency == 1:
            if self.buyDate < date(self.buyDate.year, self.payDate[0][0], self.payDate[0][1]):
                return self.maturity.year - self.buyDate.year + 1
            else:
                return self.maturity.year - self.buyDate.year
        elif self.frequency == 2:
            flag1 = (self.buyDate - date(self.buyDate.year, self.payDate[0][0], self.payDate[0][1])).days
            flag2 = (self.buyDate - date(self.buyDate.year, self.payDate[1][0], self.payDate[1][1])).days
            if flag1 > 0 and flag2 > 0:
                if self.maturity.month == self.payDate[0][0]:
                    return (self.maturity.year - self.buyDate.year - 1) * 2 + 1
                elif self.maturity.month == self.payDate[1][0]:
                    return (self.maturity.year - self.buyDate.year - 1) * 2 + 2
                else:
                    print("maturity date dose not match with start date and pay frequency")
            elif flag1 > 0 and flag2 < 0:
                if self.maturity.month == self.payDate[0][0]:
                    return (self.maturity.year - self.buyDate.year - 1) * 2 + 2
                elif self.maturity.month == self.payDate[1][0]:
                    return (self.maturity.year - self.buyDate.year - 1) * 2 + 3
                else:
                    print("maturity date dose not match with start date and pay frequency")
            elif flag1 < 0 and flag2 < 0:
                if self.maturity.month == self.payDate[0][0]:
                    return (self.maturity.year - self.buyDate.year - 1) * 2 + 3
                elif self.maturity.month == self.payDate[1][0]:
                    return (self.maturity.year - self.buyDate.year - 1) * 2 + 4
                else:
                    print("maturity date dose not match with start date and pay frequency")
            else:
                print("weird results")
                    
    def computeDaysToPay(self):
        if self.frequency == 1:
            if self.buyDate < date(self.buyDate.year, self.payDate[0][0], self.payDate[0][1]):
                return (self.buyDate - date(self.buyDate.year-1, self.payDate[0][0], self.payDate[0][1])).days, (date(self.buyDate.year, self.payDate[0][0], self.payDate[0][1]) - self.buyDate).days
            else:
                return (self.buyDate - date(self.buyDate.year, self.payDate[0][0], self.payDate[0][1])).days, (date(self.buyDate.year+1, self.payDate[0][0], self.payDate[0][1]) - self.buyDate).days
        if self.frequency == 2:
            flag1 = (self.buyDate - date(self.buyDate.year, self.payDate[0][0], self.payDate[0][1])).days
            flag2 = (self.buyDate - date(self.buyDate.year, self.payDate[1][0], self.payDate[1][1])).days
            if flag1 > 0 and flag2 > 0:
                return flag2, (date(self.buyDate.year+1, self.payDate[0][0], self.payDate[0][1]) - self.buyDate).days
            elif flag1 >0 and flag2 < 0:
                return flag1, abs(flag2)
            elif flag1 < 0 and flag2 < 0:
                return (self.buyDate - date(self.buyDate.year-1, self.payDate[1][0], self.payDate[1][1])).days, abs(flag1)
            else:
                print("weird results")
    
    def presentValue(self):
        pv_clean = float(0)
        pv_dirty = float(0)
        w = float(self.daysToNextPay) / (self.daysPastLastPay + self.daysToNextPay)
        for i in range(self.remainingPayTimes):
            pv_dirty += float(self.coupon) / ((1 + self.yieldToMaturity/self.frequency) ** (i+w))
        pv_dirty += float(self.parValue) / ((1 + self.yieldToMaturity/self.frequency) ** (self.remainingPayTimes-1+w))
        pv_clean = pv_dirty - float(self.coupon) * self.daysPastLastPay / (self.daysPastLastPay + self.daysToNextPay)
        return pv_clean, pv_dirty
    
    def presentValue2(self):
        pv_dirty = float(0)
        pv_dirty = float(self.coupon) * (1 -  (1 + self.yieldToMaturity/self.frequency)**(-1*self.remainingPayTimes)) / (self.yieldToMaturity/self.frequency) + self.parValue / ((1+self.yieldToMaturity/self.frequency)**(self.remainingPayTimes))
        return pv_dirty
    
    def presentValue3(self, ytm):
        pv = float(0)
        w = float(self.daysToNextPay) / (self.daysPastLastPay + self.daysToNextPay)
        for i in range(self.remainingPayTimes):
            pv += float(self.coupon) / ((1 + ytm/self.frequency) ** (i+w))
        pv += float(self.parValue) / ((1 + ytm/self.frequency) ** (self.remainingPayTimes-1+w))
        return pv
    
    def computeDuration(self):
        d, modifiedD = 0, 0 
        w = float(self.daysToNextPay) / (self.daysPastLastPay + self.daysToNextPay)
        for i in range(self.remainingPayTimes):
            d += (float(i+w) / self.frequency) * float(self.coupon) / ((1 + self.yieldToMaturity/self.frequency) ** (i+1)) / self.pv_dirty_
        d += (float(self.remainingPayTimes-1+w) / self.frequency) * float(self.parValue) / ((1 + self.yieldToMaturity/self.frequency) ** (self.remainingPayTimes)) / self.pv_dirty_
        return d, d / (1 + self.yieldToMaturity/self.frequency) 
    
    def computeConvexity(self):
        c = 0
        w = float(self.daysToNextPay) / (self.daysPastLastPay + self.daysToNextPay)
        for i in range(self.remainingPayTimes):
            c += (float(i+w) * float(i+w+1) / self.frequency) * float(self.coupon) / ((1 + self.yieldToMaturity/self.frequency) ** (i+1)) / self.pv_dirty_
        c += (float(self.remainingPayTimes-1+w) *  float(self.remainingPayTimes+w) / self.frequency) * float(self.parValue) / ((1 + self.yieldToMaturity/self.frequency) ** (self.remainingPayTimes)) / self.pv_dirty_
        return c / (1 + self.yieldToMaturity/self.frequency)**2/self.frequency
    
    def computeYTM(self):
        w = float(self.daysToNextPay) / (self.daysPastLastPay + self.daysToNextPay)
        a = 0.2
        b = 0.0001
        while abs(a - b) > self.epsilon:
            if self.presentValue3((a+b)/2) > self.buyPrice:
                b = (a+b)/2
            else:
                a = (a+b)/2
        return a