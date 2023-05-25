from aaaApi import AaaApi
import json
from PIL import Image
import requests
import base64
from threading import Thread, RLock
import time

class Media(Thread):
    """ Media """
    api = None
    url = None
    propertyId = None
    enclosure_queue = None

    def __init__(self, api, id, medias, propertyId, enclosure_queue, logger):
        Thread.__init__(self)
        self.api = api
        self.id = id
        self.medias = medias
        self.propertyId = propertyId
        self.enclosure_queue = enclosure_queue
        self.logger = logger
        
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while True:
            url = self.enclosure_queue.get()
            if url is None:
                break

            try :
                self.createMedia(url)
            except Exception as e:
                self.logger.error(e, exc_info=True)
                print("!!!! ERROR !!!!!"+str(url))

            self.enclosure_queue.task_done()       

    def createMedia(self, url):
        r = requests.get(url)
        
        if r.status_code != 200 or 'image' not in r.headers.get('content-type') :
            f = open('errors_img.log', 'a')
            f.write('ERRRRRR - %s' % r.headers.get('content-type'))
            f.close()
        else :
            img = r.content
            img64 = str(base64.b64encode(img).decode("utf-8"))
            pictureType = "picture"
            if self.id == 0 and len(self.medias) == 0:
                pictureType = "banner"
            
            imgDate = {
                "title":"bbb_"+str(self.propertyId)+"_"+str(self.id),
                "type":pictureType,
                "image_type":"property",
                "file":img64
            }

            result = self.api.callRequest("/medias", json.dumps(imgDate))
            data = json.loads(result.text)

            if 'data' in data and 'id' in data['data'] :
                self.medias.append({ "media" : data['data']['id'] })
        
        