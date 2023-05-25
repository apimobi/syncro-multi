from address import Address
# from rate import *
from aaaApi import AaaApi
import json
from media import Media
import queue
from amenities import Amenities
from rate import *
import math
import re

class Property(object):
    """Property entity"""
    
    def __init__(self, data):
        self.__parseData(data)
        self.medias = []
        self.amenities = []
        self.amenities.clear()
        self.rates = []
        self.rates.clear()

    def __parseData(self, data):
        self.name = self.checkNameLength(data['name'])
        self.fancyName = self.name
        self.slug = data['slug']
        self.shortDescription = re.sub('<br\s*?\/>', '', data['short_description'])
        self.fullDescriptionHtml = re.sub('<br\s*?\/>', '', data['description'])
        self.nbMaxGuest = data['max_occupancy']
        self.nightlyRateSellTtc = data['max_rate']
        self.nbBedroom = math.ceil((int(data['max_occupancy'])/3))
        self.nbBathroom = data['bathrooms']
        self.nbToilet = data['bathrooms']
        self.lat = data['geo']['lat']
        self.lon = data['geo']['lon']
        self.coul = data['ac']
        self.smokersAllowed = data['smoking_allowed']
        self.propertySource = 2
        self.hasInternet = data['internet']
        self.status = "reviewing"
        self.creator = 11799
        self.owner = 11799
        self.manager = 11799
        self.is_forced = True
        self.propertySource = {
            "source" : "TK",
            "externalId" : data['id']
        }
        self.nightlyRateFloorTtc = 0
        self.nightlyRateSellTtc = 0
        self.weeklyRateFloorTtc = 0
        self.weeklyRateSellTtc = 0
        self.monthlyRateFloorTtc = 0
        self.monthlyRateSellTtc = 0
        self.commissionType = "commission_pmc"

        if( isinstance( self.nbBathroom, int ) == False or self.nbBathroom == 0):
            self.nbBathroom = 1
            self.nbToilet = 1


    def setDefaultPrices(self, rates):
        if len(rates) != 0 :
            nightlyRate = rates[0]['weekday_rate']
            if(rates[0]['weekend_rate'] != 0):
                nightlyRate = rates[0]['weekend_rate']

            weeklyRate = rates[0]['weekly_rate']
            if(weeklyRate == 0):
                weeklyRate = nightlyRate*7

            monthlyRate = rates[0]['monthly_rate']
            if(monthlyRate == 0):
                monthlyRate = nightlyRate*28

            self.nightlyRateFloorTtc = nightlyRate
            self.nightlyRateSellTtc = nightlyRate
            self.weeklyRateFloorTtc = weeklyRate
            self.weeklyRateSellTtc = weeklyRate
            self.monthlyRateFloorTtc = monthlyRate
            self.monthlyRateSellTtc = monthlyRate

    def setAddress(self, api, data, countries, cities):
        ad = Address(api ,data, countries, cities)
        self.address = ad.getAddress()

    def checkNameLength(self, name):

        if len(name) < 6:
            name = name+" "+name
            self.checkNameLength(name)

        return name

    def createPropertyMedia(self, api, data, propertyId, logger):
        
        currentThread = []
        currentThread.clear()
        imgId = 0
        self.enclosure_queue = queue.Queue()
        self.medias.clear()

        for i in range(5):
            worker = Media(api, imgId, self.medias, propertyId, self.enclosure_queue, logger)
            worker.setDaemon(True)
            worker.start()
            imgId += 1
        
        for img in data['images']:
            self.enclosure_queue.put(img)
        
        self.enclosure_queue.join()
        for i in range(5):
            self.enclosure_queue.put(None)
        for elt in currentThread:
            elt.join() 

    def createPropertyRoom(self, api, data, propertyId, logger):
        print(">>>> createPropertyRoom "+str(propertyId))
        if len(self.amenities) == 0:
            self.amenities = Amenities(data, api, propertyId, self.medias, logger)
    
    def createPropertyRate(self, api, data, sbPropertyId, logger):
        if len(self.rates) == 0:
            self.rates = PropertyRate(api, data, sbPropertyId, logger).rates    
