from address import Address
# from rate import *
from aaaApi import AaaApi
import json
import math

class Property(object):
    """Property entity"""
    id = 0
    
    def __init__(self, data):
        self.__parseData(data)

    def __parseData(self, data):
        self.name = self.checkNameLength(data['name'])
        self.slug = data['slug']
        self.shortDescription = data['short_description']
        self.fullDescriptionHtml = data['description']
        self.accessInformation = data['directions']
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
        self.creator = 7919
        self.owner = 7919
        self.manager = 7919
        self.is_forced = True
        self.propertySource = {
            "source" : "TK",
            "externalId" : data['id']
        }

    def setAddress(self, api, data, countries, cities):
        ad = Address(api ,data, countries, cities)
        self.address = ad.getAddress()
        print(self.address)

    def checkNameLength(self, name):

        if len(name) < 6:
            name = name+" "+name
            self.checkNameLength(name)

        return name