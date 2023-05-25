import requests
import json
from property import Property
from aaaApi import AaaApi
from amenities import Amenities
from media import Media
import queue
import sys
from rate import *
from threading import Thread

base_url = "https://xxxxxxxx/query"

amenities = None
sbCountries = None
sbCities = None
api = None
num_fetch_threads = 50
enclosure_queue = queue.Queue()
properties = []
headers = {'Content-Type':'application/json'}


class MyThread(Thread):
    """ MyThread """
    
    myQueue = None

    def __init__(self, myQueue, properties):
        Thread.__init__(self)
        self.myQueue = myQueue
        self.properties = properties
        
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        print('start property')
        while True:
            data = self.myQueue.get()
            try:
                self.createElt(data)
            except:
                self.myQueue.task_done()

    def createElt(self, data):

        query = """
            mutation (
            $portfolio: String,
            $shortCode:String!,
            $name:String!,
            $approxLatitude:Float!,
            $approxLongitude:Float!,
            $bedrooms:Int,
            $bathrooms:Int!,
            $sleeps:Int
            $description:String!
                )
            {
                homeNew(
                    portfolio: $portfolio,
                    shortCode: $shortCode,
                    marketingPrice: 1000,
                    name: $name,
                    locationId :1,
                    currencyIsocode : "EUR"
                    approxLatitude:  $approxLatitude,
                    approxLongitude: $approxLongitude,
                    bedrooms: {
                        min: 1,
                        max: $bedrooms
                    },
                    bathrooms: $bathrooms,
                    sleeps : {
                        min : 1,
                        max : $sleeps
                    }
                    )
                { ok }
                homeDescriptionSet(
                    shortCode: $shortCode,
                    descriptionType: DESCRIPTION,
                    text: $description,
                    contentType: MARKDOWN
                ) { ok }
            }
        """

        parameters = {
            "portfolio":"sb",
            "shortCode": "SB-NEW-"+str(data['id']),
            "name": data['name'],
            "approxLatitude" : data['address']['latitude'],
            "approxLongitude" : data['address']['longitude'],
            "bedrooms": data['nb_bedroom'],
            "bathrooms": data['nb_bathroom'],
            "sleeps": data['nb_max_guest'],
            "description": data['full_description_html']
        }
    
        r = requests.post(base_url, headers=headers, json={ "query": query, "variables" : json.dumps(parameters)} )
        print(r.text)
        print("*****END PROPERTY OK*****")
        self.properties.append(data['id'])
        self.myQueue.task_done()


def loadProperties(off, lim):
    result = api.callRequest("/properties?offset="+str(off)+"&limit="+str(lim)+"sources[]=SB&statuses[]=validated")
    data = json.loads(result.text)

    return data


def processProperties(data, properties):
    
    print(" >>>> processProperties")
    enclosure_queue = queue.Queue()

    for i in range(10):
        worker = MyThread(enclosure_queue, properties) 
        worker.setDaemon(True)
        worker.start()
    
    for prop in data['data']:
        print(prop['id'])
        enclosure_queue.put(prop)
    
    print ('*** Main thread waiting')
    enclosure_queue.join()
    print ('*** Done')


if __name__ == '__main__':
    
    if len(sys.argv) < 3 :
        print("you need to pass username and password and environment")
        exit()
    env = None    
    if len(sys.argv) == 4:
        env = sys.argv[3]

    api = AaaApi(sys.argv[1], sys.argv[2], env)
    properties.clear()
    data = loadProperties(0, 400)
    processProperties(data, properties)
