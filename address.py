import json

class Address(object):
    """ Address """
    api = None
    city = 0
    country = 0
    countries = None
    cities = None
    zipcode = 1

    def __init__(self, api, data, countries, cities):
        self.api = api
        self.countries = countries
        self.cities = cities
        self.__parseData(data)

    def __parseData(self, data):
        geo = data['geo']
        address = data['address']
        self.address1 = address['address1']+" "+address['address2']
        self.city_str = address['city']
        self.state = address['state']
        self.zipcode = address['zipcode']
        self.lat = geo['lat']
        self.lon = geo['lon']
        self.findAddress(geo)

        if self.zipcode == "":
            self.zipcode = 1

        if self.country == 0 :
            self.country = 1

        if self.address1.strip() == "" :
            self.address1 = "unknown address"
        
        if self.city == 0:
            self.city = 1    


    def findAddress(self, geo):
        
        if geo['lat'] == 0 or geo['lon'] == 0:
            return None

        result = self.api.callRequest("/addresses/find/"+str(geo['lat'])+"/"+str(geo['lon']))
        
        if result.status_code == 204:
            return None
        
        data = json.loads(result.text)

        if "route" in data:
            self.address1 = data['route']

        if "street_number" in data:
            self.address1 = data['street_number']+" "+self.address1

        if "country" in data:
            self.country = self.findCountry(data['country'])

        self.findCity(data)

        if "postal_code" in data:
            self.zipcode = data['postal_code']

    def findCountry(self, country_str):

        for country in self.countries:
            if country['country_name'] == country_str:
                return country['id']

        return 1
    
    def findCity(self, data):
        
        
        if "locality" in data:
            self.city_str = data['locality']
        elif "administrative_area_level_1" in data:
            self.city_str = data['administrative_area_level_1']

        if self.city_str != "":
            if( self.cities.findCity(self.city_str) ):
                self.city = self.cities.findCity(self.city_str)
        
        if self.city == 0 and self.city_str != "" and self.country != 0:
            # print('------ create City-------')
            newCity = {
                "name" : self.city_str,
                "slug" : self.city_str,
                "countryId" : self.country,
                "isRestricted" : 0
            }
            self.city = self.cities.createCity(newCity)
    
    def getAddress(self):

        return {
            "latitude": self.lat,
            "longitude": self.lon,
            "address": self.address1,  
            "zipcode": self.zipcode,
            "city" : self.city,
            "country" : self.country
        }