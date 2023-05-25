from aaaApi import AaaApi
import json
import math
import datetime


class Rate(object):
    """Rate"""

    def __init__(self, data, propertyId, id, newDate):
        self.name = 'property_'+str(propertyId)+"_"+str(id)
        if newDate :
            self.dateFrom = newDate
        else :
            self.dateFrom = data['start_date']   
        self.dateTo = data['end_date']
        self.minimumStay = data['min_stay']
        self.property = propertyId
        self.isFlexibleArrival=True
        self.isSaturdayArrival=False
        self.isSundayArrival=False
        self.isInstantBooking=False
        self.createRate(data)
        self.propertyRateGuests = []
        self.propertyRateGuests.clear()

    def createRate(self, data):
        
        self.nightlyRate = data['weekday_rate']
        if(data['weekend_rate'] != 0):
            self.nightlyRate = data['weekend_rate']

        self.weeklyRate = data['weekly_rate']
        if(self.weeklyRate == 0):
            self.weeklyRate = math.ceil(self.nightlyRate*7)

        self.monthlyRate = data['monthly_rate']
        if(self.monthlyRate == 0):
            self.monthlyRate = math.ceil(self.nightlyRate*28)
        
        self.commission=0
        self.nightlyRateSell=self.nightlyRate
        self.weeklyRateSell=self.weeklyRate
        self.monthlyRateSell=self.monthlyRate
    
    
    def addRateGuest(self, data):
        
        nightlyRate = data['weekday_rate']
        if(data['weekend_rate'] != 0):
            nightlyRate = data['weekend_rate']

        weeklyRate = data['weekly_rate']
        if(weeklyRate == 0):
            weeklyRate = nightlyRate*7

        monthlyRate = data['monthly_rate']
        if(monthlyRate == 0):
            monthlyRate = nightlyRate*28
        
        self.propertyRateGuests.append(
        {
            "guests":data['persons'],
            "bedrooms":data['bedrooms'],
            "nightlyRate":nightlyRate,
            "weeklyRate":weeklyRate,
            "monthlyRate":monthlyRate,
            "commission": 0,
            "nightlyRateSell":nightlyRate,
            "weeklyRateSell":weeklyRate,
            "monthlyRateSell":monthlyRate
        })

    

class PropertyRate(object):
    """Property rate"""

    def __init__(self, api, data, propertyId, logger):
        self.api = api
        self.logger = logger
        self.rates = []
        self.rates.clear()
        self.__parseData(data, propertyId)
        
        try :
            self.createRates()
        except Exception as e:
            self.logger.error(e, exc_info=True)
        
    def __parseData(self, data, propertyId):
        
        rate = None
        currentDateFrom = None
        currentDateTo = None
        i = 0
        for tkRate in data:
            if(tkRate['start_date'] != currentDateFrom):
                
                if rate :
                    self.rates.append(rate)
                
                # check if there is delta between 2 rates :'(
                newDate = None
                if currentDateFrom != None :    
                    date1 = datetime.datetime.strptime(currentDateTo, "%Y-%m-%d")
                    date1 = date1 + datetime.timedelta(days=1)
                    date2 = datetime.datetime.strptime(tkRate['start_date'], "%Y-%m-%d")
                    
                    if date1.strftime('%Y-%m-%d') != date2.strftime('%Y-%m-%d'):
                        newDate = date1.strftime('%Y-%m-%d')
                
                currentDateFrom = tkRate['start_date']
                currentDateTo = tkRate['end_date']
                rate = Rate(tkRate, propertyId, i, newDate)
                i += 1
            
            rate.addRateGuest(tkRate)

        self.rates.append(rate)

    def  createRates(self):
        for rate in self.rates:
            if rate :
                result = self.api.callRequest("/properties/rates/create", json.dumps(rate.__dict__))
