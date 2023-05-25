import requests
import json
from property import Property
from aaaApi import AaaApi
from amenities import Amenities
from media import Media
import queue
import sys
from rate import *

base_url = "https://www.bbb.com/api"
headers = {"x-api-key" : "bbb"}

amenities = None
sbCountries = None
sbCities = None
api = None
num_fetch_threads = 10
enclosure_queue = queue.Queue()
properties = []
medias = []

def getCountries():
    result = api.callRequest("/countries")
    data = json.loads(result.text);
    return data['data']

def getCities():
    result = api.callRequest("/cities")
    data = json.loads(result.text);
    return data['data']
    

def getAmenities():
    if(amenities == None):
        result = requests.get(base_url+"/amenities/", headers=headers)
        data = json.loads(result.text);
        self.amenities = data['amenities']



def loadProperties(off, lim):
    
    print('from '+str(off)+" to "+str(lim))
    r = requests.get(base_url+"/properties/?offset="+str(off)+"&limit="+str(lim), headers=headers)
    data = json.loads(r.text);

    print(len(data['properties']))
    for pro in data['properties']:
        properties.append(pro['id'])


def addProperties():
    for property in properties:
        Property.create(name=property['name'])

def getProperty(propertyId):
    print("---------------------")
    print("----------getProperty-----------")
    print("---------------------")
    print(propertyId)
    medias.clear()
    r = requests.get(base_url+"/properties/"+str(propertyId)+"/", headers=headers)
    data = json.loads(r.text)
    
    p = Property(data)
    p.setAddress(api, data, sbCountries, sbCities)

    result = api.callRequest("/properties", json.dumps(p.__dict__))
    try :
        sbPropertyId = json.loads(result.text)['data']['id'];
        p.id = sbPropertyId
    except :
        print("!!! Error on property "+str(propertyId)+" "+str(result.text))
        return None

    ### Medias ####
    createPropertyMedia(data, medias, propertyId)
    
    #### Rooms amenities ####
    createPropertyRoom(data, sbPropertyId, medias)

    #### RATES ####
    r = requests.get(base_url+"/properties/"+str(propertyId)+"/rates/", headers=headers)
    data = json.loads(r.text);
    rates = PropertyRate(api, data, sbPropertyId).rates

    return p.id

def createPropertyMedia(data, medias, propertyId):
    
    threads = {}
    imgId = 0
    enclosure_queue = queue.Queue()
    # tmp = [ data['image'] ]

    for i in range(num_fetch_threads):
        worker = Media(api, imgId, medias, propertyId, enclosure_queue) 
        worker.setDaemon(True)
        worker.start()
        imgId += 1
    
    for img in data['images']:
        enclosure_queue.put(img)
    
    print ('*** Main thread waiting')
    enclosure_queue.join()
    print ('*** Done')

def createPropertyRoom(data, propertyId, medias):
    amenity = Amenities(data, api, propertyId, medias)


if __name__ == '__main__':
    
    if len(sys.argv) < 3 :
        print("you need to pass username and password and environment")
        exit()
    env = None    
    if len(sys.argv) == 4:
        env = sys.argv[3]

    api = AaaApi(sys.argv[1], sys.argv[2], env)
    sbCountries = getCountries()
    sbCities = getCities()

    i = 0
    offset = 0
    limit = 200
    last = 7158
    
    while offset < last :    
        
        properties.clear()
        loadProperties(offset, limit)
        print(len(properties))

        for elt in properties:
            id = getProperty(elt)
            print ("DONE for "+str(id))
        
        offset += 200

        if (offset + limit) > last :
            limit = last - offset

        if offset > last:
            break 
