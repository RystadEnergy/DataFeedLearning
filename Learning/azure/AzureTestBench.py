import sys
import os
import json
import logging
import pyodbc
import pandas as pd

## Important Set Up Steps:
## Input your credentials on the attached config file.
## Change the query for what applies to your analysis.

def main():
    
    _logger = logging.getLogger(__name__)

    REQUIRED_PROPERTIES = [
        'azure_server',
        'azure_database',
        'azure_username',
        'azure_password',
        'azure_driver'
    ]
    class AzureSession:

        def __init__(self):
            with open(os.path.join(sys.path[0], "config.json"), 'r') as f:
                login_properties = json.loads(f.read())

            provided_keys = set(login_properties.keys())
            required_keys = set(REQUIRED_PROPERTIES)
            missing_keys = list(required_keys - provided_keys)
            self.login_properties = login_properties
        
        def run_azure_query(self, retry_attempts=5):
            server = self.login_properties['azure_server']
            database = self.login_properties['azure_database']
            username = self.login_properties['azure_username']
            password = self.login_properties['azure_password']   
            driver= self.login_properties['azure_driver']

            with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
                with conn.cursor() as cursor:
                    # Change your query here
                    cursor.execute("SELECT TOP 10 * FROM [UCUBE].[ASSET]")
                    data = cursor.fetchall()
                    dataframe = pd.DataFrame(data)
                    print(dataframe)

    #Main Code CallUps
    logging.basicConfig(level=logging.ERROR)
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    session = AzureSession()
    AzureSession.run_azure_query(self=session, retry_attempts=0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write('Python script failed with error: {0}'.format(str(e)))    
        sys.exit(1)