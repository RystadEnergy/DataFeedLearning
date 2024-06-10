import sys
import os
import json
import logging
import snowflake.connector

## Important Set Up Steps:
## Input your credentials and account details on the attached config file.
## Change the query for what applies to your analysis.

def main():
    
    _logger = logging.getLogger(__name__)

    REQUIRED_PROPERTIES = [
        'snowflake_user',
        'snowflake_password',
        'snowflake_database',
        'snowflake_schema',
        'snowflake_account'
    ]
    class SnowFlakeSession:

        def __init__(self):
            with open(os.path.join(sys.path[0], "config.json"), 'r') as f:
                login_properties = json.loads(f.read())

            provided_keys = set(login_properties.keys())
            required_keys = set(REQUIRED_PROPERTIES)
            missing_keys = list(required_keys - provided_keys)
            self.login_properties = login_properties
        
        def run_snowflake_query(self, retry_attempts=5):
            try:
                conn = snowflake.connector.connect(
                                user=self.login_properties['snowflake_user'],
                                password=self.login_properties['snowflake_password'],
                                account=self.login_properties['snowflake_account']
                                )

                # Create cursor
                cur = conn.cursor()

                # Execute SQL statement
                _logger.info("Operation Started.")   
                # Change your query here:
                cur.execute("SELECT TOP 10 * FROM \"DATAFEED\".\"UCUBE\".\"ASSET\"")
                for register in cur:
                    print(register)
                _logger.info("Operation Finished")
                         
            except Exception as e:
                if retry_attempts > 0:
                    _logger.warning(f'Connection error: {e}, retrying... new attempts left: {retry_attempts - 1}')
                    self.update_tables(retry_attempts=retry_attempts - 1)
                else:
                    _logger.error(f'Connection error: {e}, max retry attempts reached, aborting')
                    raise Exception(e)

    #Main Code CallUps
    logging.basicConfig(level=logging.ERROR)
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    session = SnowFlakeSession()
    SnowFlakeSession.run_snowflake_query(self=session, retry_attempts=0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write('Python script failed with error: {0}'.format(str(e)))    
        sys.exit(1)