#import argparse
import os
import requests
from rucio.clients import AccountClient

GODMODE_ACCOUNTS = { 'root', 'bjwhite', 'illingwo', 'mengel', 'dylee'}

def main():
    # If a bit awkward, use environment variables for configuration as this is planned for use within a container anyway.
    ferry_vo = os.environ['FERRY_VO']
    if ferry_vo is None: raise ValueError
    ferry_url = os.environ['FERRY_URL'] or 'https://ferry.fnal.gov:8445'
    cert_path = os.environ['CERTIFICATE_PATH'] or '/opt/rucio/certs/usercert.pem'
    key_path = os.environ['KEY_PATH'] or '/opt/rucio/keys/new_userkey.pem'
    ca_path = os.environ['CA_PATH'] or '/etc/grid-security/certificates'

    print(f"Beginning synchronization of Rucio users for VO {ferry_vo} with FERRY at: {ferry_url}")
    session = requests.Session()
    session.cert = (cert_path, key_path)
    session.verify = ca_path

    # ADD EXP[PRO|RAW] to GODMODE_ACCOUNTS


if __name__=="__main__":
    main()