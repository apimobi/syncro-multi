import requests
import json
from propertyM import Property
from aaaApi import AaaApi
from amenities import Amenities
from media import Media
import queue
import sys
from rate import *
from threading import Thread
import csv
import time
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

base_url = "https://www.bbb.com/api"
headers = {"x-api-key" : "bbb"}

properties_queue = queue.Queue()
properties = []
propertiesDone = []
sbCities = None

class SbCities():
    """ Cities """

    def __init__(self, api):
        Thread.__init__(self)
        self.cities = []
        self.cities.clear()
        self.api = api
        self.fetchCities()

    def fetchCities(self):
        result = self.api.callRequest("/cities")
        data = json.loads(result.text);
        self.cities = data['data']
    
    def findCity(self, cityName):
         
        for city in self.cities:
            if city['name'] == cityName:
                return city['id']
        
        return None

    def createCity(self, city):
        result = self.api.callRequest("/cities/create", json.dumps(city))    
        dataCity = json.loads(result.text)
        self.cities.append({"id":dataCity['data']['id'], "name":dataCity['data']['name']})
        return dataCity['data']['id']

class MyThread(Thread):
    """ MyThread """
    
    def __init__(self, myQueue, propertiesDone, api):
        Thread.__init__(self)
        self.myQueue = myQueue
        self.propertiesDone = propertiesDone
        self.medias = []
        self.enclosure_queue = queue.Queue()
        self.api = api
        
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while True:
            pId = self.myQueue.get()
            if pId is None:
                break
            self.createElt(pId)

    def createElt(self, propertyId):
        self.medias.clear()
        base_url = "https://www.bbb.com/api"
        
        try :    
            #### check if already exist ####
            check = self.api.callRequest("/properties?source[]=TK&external_id="+str(propertyId))
            if check.status_code == 200:
                print(" +++++ SKIP "+str(propertyId)+" +++++++")
            else:
                
                r = requests.get(base_url+"/properties/"+str(propertyId)+"/", headers = headers)
                data = json.loads(r.text);
                rateRequest = requests.get(base_url+"/properties/"+str(propertyId)+"/rates/", headers = headers)
                tkRates = json.loads(rateRequest.text);

                p = Property(data)
                p.setAddress(api, data, sbCountries, sbCities)
                p.setDefaultPrices(tkRates)

                result = self.api.callRequest("/properties", json.dumps(p.__dict__))
                resultTxt = json.loads(result.text)
                if 'data' in resultTxt and 'id' in resultTxt['data'] :
                    
                    sbPropertyId = json.loads(result.text)['data']['id'];
                    p.id = sbPropertyId

                    #### Medias ####
                    p.createPropertyMedia(self.api, data, propertyId, logger)
                    
                    #### Rooms amenities ####
                    p.createPropertyRoom(self.api, data, sbPropertyId, logger)

                    #### RATES ####
                    p.createPropertyRate(api, tkRates, sbPropertyId, logger)

                    print("!!!!!!!!!!!!END PROPERTY OK!!!!!!!!! "+str(propertyId))
                    self.propertiesDone.append(propertyId)
                else:
                    logPropertiesError(propertyId)
        except Exception as e:
            logger.error(e, exc_info=True)
            print("!!!! ERROR !!!!! "+str(propertyId))
            logPropertiesError(propertyId)
        
        # print(len(self.propertiesDone))
        self.myQueue.task_done()


def logPropertiesError(propertyId):
    
    with open('errors.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([propertyId])

def logPropertiesOk():
    
    with open('propertiesDone.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(propertiesDone)


def deleteContent(fName):
    with open(fName, "w"):
        pass


def getCountries():
    result = api.callRequest("/countries")
    data = json.loads(result.text);
    return data['data']


def getAmenities():
    if(amenities == None):
        result = requests.get(base_url+"/amenities/", headers=headers)
        data = json.loads(result.text);
        self.amenities = data['amenities']



def loadProperties(off, lim):
    
    print('------------ from '+str(off)+" to "+str(lim))
    try:
        r = requests.get(base_url+"/properties/?offset="+str(off)+"&limit="+str(lim), headers=headers)
        data = json.loads(r.text);

        print(len(data['properties']))
        for pro in data['properties']:
            properties.append(pro['id'])
    except:
        time.sleep(10)
        loadProperties(off, lim)        

def processProperties(api):
        
    currentThread = []
    currentThread.clear()
    print(" >>>> processProperties")
    properties_queue = queue.Queue()
    print(properties)
    for i in range(5):
        worker = MyThread(properties_queue, propertiesDone, api) 
        worker.setDaemon(True)
        worker.start()
        currentThread.append(worker)
    
    for elt in properties:
        properties_queue.put(elt)
    
    print ('*** QUEUE ON BOARD *******')
    print(list(properties_queue.queue))
    print ('*** Main thread waiting')
    properties_queue.join()
    print ('------------- QUEUE Done ---------------')

    for i in range(5):
        properties_queue.put(None)
    for elt in currentThread:
        elt.join()    


if __name__ == '__main__':
    
    if len(sys.argv) < 3 :
        print("you need to pass username and password and environment")
        exit()
    env = None    
    if len(sys.argv) == 4:
        env = sys.argv[3]

    deleteContent('propertiesDone.csv')
    deleteContent('errors.csv')
    deleteContent('error.log')
    api = AaaApi(sys.argv[1], sys.argv[2], logger, env)
    sbCountries = getCountries()
    sbCities = SbCities(api)

    i = 0
    offset = 0
    limit = 100
    last = 8000
    
    while offset < last :    
        
        print(" offset :"+str(offset))
        print(" limit :"+str(limit))
        properties.clear()
        
        loadProperties(offset, limit)

        # properties.clear()
        # properties = [9005]

        if len(properties) == 0:
            logPropertiesOk()
            print(" ---- No more properties ----- ")
            break


        processProperties(api)

        offset += 100
    
    # getProperty(9636)
