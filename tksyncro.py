from flask import Flask, request
from flask_restful import Resource, Api
import json
from flask_jsonpify import jsonify
from aaaApi import AaaApi
from tkApi import TkApi
import logging
import sys
import os


app = Flask(__name__)
api = Api(app)
logging.basicConfig(filename='syncro_error.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
env = "aws"

class Properties(Resource):
    def get(self, pid):
        result = sbApi.callRequest("/properties/"+str(pid))
        data = json.loads(result.text)
        return jsonify(data)
    
class PropertiesSyncro(Resource):

    def get(self, pid):
        bookings = tkApi.getPropertyUnavailablities(pid)
        data = sbApi.callRequest("/properties?source[]=TK&external_id="+str(pid))
        if bookings and data.status_code == 200:
            # print (data.text['data'])
            sbId = json.loads(data.text)['data'][0]['id']
            result = self.updateUnavailablities(pid, sbId, bookings)
            return jsonify(result)

    def updateUnavailablities(self, pid, sbId, bookings):

        writepath = 'bookings/unavailablities-'+str(pid)+'.json'
        fileExists = os.path.exists(writepath)
        
        if fileExists :
            with open(writepath) as unavailablities:
                data = json.load(unavailablities)
                actualList = data['busy']
        else :
            actualList = []
        
        i = 0
        newList = []
        for elt in bookings:
            if elt['id'] not in actualList and elt["status"] == "confirmed":
                booking = {
                    "dateFrom" : elt['start_date'],
                    "dateTo" : elt['end_date'],
                    "property" : sbId
                    # "description" : "TK booking "+str(pid)+" id : "+str(elt['id'])
                }
                
                result = sbApi.callRequest("/properties/unavailability", json.dumps(booking))
                
                if result.status_code == 200 :
                    actualList.append(elt['id'])
                    newList.append(booking)

        data = {
            "busy":actualList
        }

        with open(writepath, 'w') as unavailablities:
            json.dump(data, unavailablities)
        
        return {'bookings': newList}


api.add_resource(Properties, '/properties/<pid>')
api.add_resource(PropertiesSyncro, '/properties/<pid>/syncro')


if __name__ == '__main__':
     
    if len(sys.argv) < 3 :
        print("you need to pass username and password and environment")
        exit()
        env = None
    
    if len(sys.argv) == 4:
        env = sys.argv[3]

    sbApi = AaaApi(sys.argv[1], sys.argv[2], logger, env)
    tkApi = TkApi()
     
    app.debug = True
    app.run()