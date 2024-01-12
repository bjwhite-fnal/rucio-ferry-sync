#import argparse
import os
import requests
from urllib.parse import urljoin
from rucio.client.accountclient import AccountClient

GODMODE_ACCOUNTS = { 'root', 'bjwhite', 'illingwo', 'mengel', 'dylee' }

def main():
    # If a bit awkward, use environment variables for configuration as this is planned for use within a container anyway.
    ferry_vo = os.getenv('FERRY_VO')
    if ferry_vo is None: raise ValueError
    ferry_url = os.getenv('FERRY_URL', 'https://ferry.fnal.gov:8445')
    cert_path = os.getenv('CERTIFICATE_PATH', '/opt/rucio/certs/usercert.pem')
    key_path = os.getenv('KEY_PATH', '/opt/rucio/keys/new_userkey.pem')
    ca_path = os.getenv('CA_PATH', '/etc/grid-security/certificates')

    print(f"Beginning synchronization of Rucio users for VO {ferry_vo} with FERRY at: {ferry_url}")
    session = requests.Session()
    session.cert = (cert_path, key_path)
    session.verify = ca_path

    # ADD EXP[PRO|RAW] to GODMODE_ACCOUNTS
    raw_account = f'{ferry_vo.lower()}raw'
    pro_account = f'{ferry_vo.lower()}pro'
    exp_users = { raw_account, pro_account }
    GODMODE_ACCOUNTS.update(exp_users)

    ferry_info = get_ferry_data(session, ferry_url, ferry_vo)
    import pprint
    pprint.pprint(ferry_info)

def get_ferry_data(session, ferry_url, ferry_vo):
    # Returns: { <username>: { 'dn': [DN list], 'fqan': [FQAN list] } }
    role_map = {}
    users = {}

    # unitname does not always neccesarily match resourcename, so match up with the right one
    result = session.get(urljoin(ferry_url, 'getAffiliationUnitComputeResources'), params={'unitname': ferry_vo})
    result_data = result.json()
    for resource in result_data['ferry_output']:
       if resource['resourcetype'] == 'Interactive':
           resourcename = resource['resourcename']
           break
    else:
       # do our best
       resourcename = ferry_vo

    # Get the mapping of FQAN -> target unix user account
    result = session.get(urljoin(ferry_url, 'getVORoleMapFile'), params={'resourcename': resourcename})
    roles = result.json()
    if 'ferry_status' in roles and roles['ferry_status'] == 'failure':
        raise Exception('Error accessing Ferry: %s' % roles['ferry_error'])
    for r in roles['ferry_output']:
        if r['username']:
            role_map[r['fqan']] = r['username']

    # Get the user -> fqan mapping and token_uuid.
    # For each username users[username][fqan] = [ list of users FQANs ]
    result = session.get(urljoin(ferry_url, 'getAffiliationMembersRoles'), params={'unitname': ferry_vo})
    user_roles = result.json()
    for r in user_roles['ferry_output'][ferry_vo]:
        r_username = r['username']
        #userinfo_lookup_res = session.get(urljoin(ferry_url, 'getUserInfo'), params={'username': r_username})
        #token_lookup_json = userinfo_lookup_res.json()
        #if token_lookup_json['ferry_output']['status'] == True:
	    #token_uuid = token_lookup_json['ferry_output']['vopersonid']
        #    # Hack the token so that it can be used with SAM, I could have done this in one line, but am being explict (bjwhite, 20220901)
        #    token_uuid = 'token:' + token_uuid
        #else:
	    #token_uuid = None 
        users.setdefault(r_username, { 'fqan': [] })['fqan'].append(r['fqan'])
        #users[r_username]['token_uuid'] = token_uuid

    # Get mapping of username -> distinguished name
    # In the full users mapping, add the DNs for existent users
    result = session.get(urljoin(ferry_url, 'getGridMapFileByVO'), params={'unitname': ferry_vo})
    dn_mapping = result.json()
    for d in dn_mapping['ferry_output'][ferry_vo]:
        try:
            users[d['username']].setdefault('dn', []).append(d['dn'])
        except KeyError:
            pass

    # Make sure all users in the final mapping have a DN
    missing_dn = users.keys() - set(u for u,i in list(users.items()) if 'dn' in i)
    if missing_dn:
        print('The following users have no DNs. Deleting them from the processing.: %s' % ', '.join(missing_dn))
        for missing_dn_user in missing_dn:
            del users[missing_dn_user]

    return users

if __name__=="__main__":
    main()