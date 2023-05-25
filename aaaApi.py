import requests
import pymysql
import requests
import json
from datetime import datetime, timedelta


class AaaApi(object):
    """AAA API"""
    local = 'http://xxx.local/app_dev.php'
    preprod = 'http://xxx.com'
    api2_url = 'http://xxx.local/app_dev.php'
    aws = 'https://aws.xxx.com'
    api2_client_id = 'xxx'
    api2_client_secret = 'xxx'
    username = ""
    password = ""
    token = ""
    headers = None
    cities = None
    refreshToken = ""
    expireDate = None

    def __init__(self, usr, pwd, logger, environment = None):
        print("INIT")
        
        self.username = usr
        self.password = pwd
        self.logger = logger

        if environment == "preproduction" :
            self.api2_url = self.preprod
        
        if environment == "aws" :
            self.api2_url = self.aws
        
        with open('credentials.json') as credentials:
            data = json.load(credentials)
            print(data['access_token'])
            if data['access_token'] == "" :
                self.getTokenByUserPwd()
            else :
                self.token = data['access_token']
                self.refreshToken = data['refresh_token']
        

    def getTokenByUserPwd(self):
        print('*****getTokenByUserPwd***********')
        result = requests.post(self.api2_url+"/oauth/v2/token", data = {
            "grant_type": "password",
            "client_id": self.api2_client_id,
            "client_secret": self.api2_client_secret,
            "username": "",
            "password": "",
            "scope": "backoffice"
        })
        data = json.loads(result.text);
        self.token = data['access_token']
        self.refreshToken = data['refresh_token']
        self.expireDate =  datetime.now() + timedelta(seconds=int(data['expires_in']))
        self.headers = { "Authorization" : "Bearer "+self.token }
        now = datetime.now()
        self.__saveToken()

    def getTokenByRefreshToken(self):
        print('*****getTokenByRefreshToken***********')
        result = requests.post(self.api2_url+"/oauth/v2/token", data = {
            "client_id": self.api2_client_id,
            "client_secret": self.api2_client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refreshToken
        })
        data = json.loads(result.text);
        
        if result.status_code == 400:
            self.getTokenByUserPwd()
        else :
            self.token = data['access_token']
            self.refreshToken = data['refresh_token']
            self.headers = { "Authorization" : "Bearer "+self.token }
            self.expireDate =  datetime.now() + timedelta(seconds=int(data['expires_in']))
            self.__saveToken()
            
    def __saveToken(self):
        data = {
            "access_token" : self.token,
            "refresh_token" : self.refreshToken,
            "expires_in" :""
        }
        with open('credentials.json', 'w') as credentials:
            json.dump(data, credentials)


    def callRequest(self, url, data = None):
        headers = { "Authorization":"Bearer "+self.token, 'Content-Type':'application/json', 'Accept-Language':'en_US' }
        if data :
            result = requests.post(self.api2_url+url, headers = headers, data=data)
        else :
            result = requests.get(self.api2_url+url, headers = headers) 
        
        if result.status_code == 401 :
            print('***** 401 ******')
            if self.token == "" :
                self.getTokenByUserPwd()
            else :
                self.getTokenByRefreshToken()

            return self.callRequest(url, data)
        elif result.status_code != 200 and result.status_code != 204 :
            self.logger.error("ERROR "+str(result.status_code))
            self.logger.error(result.text)
            return result
        else :
            return result

        print('OUPS Something bad happens')