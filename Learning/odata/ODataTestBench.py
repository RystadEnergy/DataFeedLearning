import sys
import os
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

## Important Set Up Steps:
## Input your credentials and product on the attached config file.
## Use the appropiate function and set up the specific table if needed

def getODataResponse(table):
    my_session = requests.Session()
    my_session.auth = HTTPBasicAuth('<<username>>', '<<password>>')
    url = 'https://odata.rystadenergy.com/Ucube/'+table
    if(my_session.get(url).status_code==200):
        response = my_session.get(url).json()
        return response

def main():
    
    _logger = logging.getLogger(__name__)

    REQUIRED_PROPERTIES = [
        'url',
        'product',
        'username',
        'password'
    ]
    class OdataSession:

        def __init__(self):
            with open(os.path.join(sys.path[0], "config.json"), 'r') as f:
                login_properties = json.loads(f.read())

            provided_keys = set(login_properties.keys())
            required_keys = set(REQUIRED_PROPERTIES)
            missing_keys = list(required_keys - provided_keys)
            self.login_properties = login_properties
        
        def getODataResponse(self, retry_attempts=5, table=''):
            url = self.login_properties['url']
            product = self.login_properties['product']
            username = self.login_properties['username']
            password = self.login_properties['password']   

            my_session = requests.Session()
            my_session.auth = HTTPBasicAuth(username, password)
            url = url +'/' + product + '/'+table
            response = my_session.get(url)
            if(response.status_code==200):
                jsonresponse = response.json()
                ##print(response)
                formattedjson = json.dumps(jsonresponse, indent=2)
                print(formattedjson)

    #Main Code CallUps
    logging.basicConfig(level=logging.ERROR)
    session = OdataSession()
    ##Get List of Tables
    OdataSession.getODataResponse(self=session, retry_attempts=0)
    ##If you want to Print a Table use this instead (Change the parameter for the desired table)
    ##OdataSession.getODataResponse(self=session, retry_attempts=0,table='Asset')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write('Python script failed with error: {0}'.format(str(e)))    
        sys.exit(1)