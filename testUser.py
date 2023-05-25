import json
from aaaApi import AaaApi
import time
import random, string
import sys

def createUser():
    user = {
        "firstName":"ouiiiii",
        "lastName":"okkkkkk",
        "email": randomword(10)+"@gmail.com",
        "phone":"+3361234567"
    }

    result = api.callRequest("/signup", json.dumps(user))
    data = json.loads(result.text);
    print(data)
    return data['data']

def findUser(email):

    result = api.callRequest("/users/search?query="+str(email))
    data = json.loads(result.text);
    print(data)
    return data['data']

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

if __name__ == '__main__':
    
    if len(sys.argv) < 3 :
        print("you need to pass username and password and environment")
        exit()
    env = None    
    if len(sys.argv) == 4:
        env = sys.argv[3]

    api = AaaApi(sys.argv[1], sys.argv[2], env)

    data = createUser()
    time.sleep(10)
    findUser(data['email'])
    


