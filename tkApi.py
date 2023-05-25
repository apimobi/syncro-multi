
import requests
import json

class TkApi(object):
        
    def __init__(self):
        print("INIT VVVAPI")
        
        self.base_url = "https://vvv.com/api"
        self.headers = {"x-api-key" : "vvv"}
        self.amenities = None


    def loadProperties(self, off, lim):
        
        try:
            r = requests.get(self.base_url+"/properties/?offset="+str(off)+"&limit="+str(lim), headers=self.headers)
            data = json.loads(r.text);

            print(len(data['properties']))
            for pro in data['properties']:
                properties.append(pro['id'])
        except:
            time.sleep(10)
            self.loadProperties(off, lim)

    def getAmenities(self):
        if(amenities == None):
            result = requests.get(self.base_url+"/amenities/", headers=self.headers)
            data = json.loads(result.text);
            self.amenities = data['amenities']
    
    def getPropertyUnavailablities(self, propertyId):
        result = requests.get(self.base_url+"/properties/"+str(propertyId)+"/availabilities", headers=self.headers)
        data = json.loads(result.text);
        if 'busy' in data :
            return data['busy']
        else :
            return None