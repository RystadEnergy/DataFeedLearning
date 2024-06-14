import paramiko
import logging
import os
import json
import sys

## Important Set Up Steps:
## Input your credentials and server on the attached config file.
## Set up the appropiate paths for download

def main():

    _logger = logging.getLogger(__name__)

    REQUIRED_PROPERTIES = [
        'sftp_user',
        'sftp_password',
        'sftp_host',
        'sftp_port'
    ]

    class SftpSession:

        def __init__(self, config_json_path):
            with open(config_json_path, 'r') as f:
                login_properties = json.loads(f.read())

            provided_keys = set(login_properties.keys())
            required_keys = set(REQUIRED_PROPERTIES)
            missing_keys = list(required_keys - provided_keys)
            self.login_properties = login_properties

        def download_file(self, remote_file_path, local_file_path, retry_attempts=5):
            # Define server and login credentials
            hostname = self.login_properties['sftp_host']   
            port = self.login_properties['sftp_port']   
            username = self.login_properties['sftp_user']   
            password = self.login_properties['sftp_password']   

            # Create an SSH client
            client = paramiko.SSHClient()
            # Automatically add the server's host key
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                # Connect to the server
                client.connect(hostname, port=port, username=username, password=password)
                print("Connection established")

                # Create an SFTP session from the SSH connection
                sftp = client.open_sftp()

                # Download the file
                sftp.get(remote_file_path, local_file_path)
                print(f"File '{remote_file_path}' downloaded to '{local_file_path}'")

                # Close the SFTP session
                sftp.close()
            except Exception as e:
                (f"Failed to connect to the server or download the file: {e}")
            finally:
                # Close the SSH connection
                client.close()
                print("Connection closed")

    logging.basicConfig(level=logging.ERROR)
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    session = SftpSession(os.path.join(curr_dir, 'config.json'))
    # Define the remote file path and the local file path      
    remote_file_path = 'UCube/asset.csv'
    local_file_path = os.path.join(os.getcwd(), 'Asset.csv')
    session.download_file(remote_file_path, local_file_path)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write('Python script failed with error: {0}'.format(str(e)))    
        sys.exit(1)