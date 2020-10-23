import json
import requests
import os

from time import sleep

BASE_URL = 'http://10.0.0.1/cgi-bin'
API = {
    'login': BASE_URL + '/api/v3/system/login',
    'lan': BASE_URL + '/api/v3/interface/lan/id',
    'apply': BASE_URL + '/api/v3/system/apply',
    'apply_status': BASE_URL + '/api/v3/system/apply/status'
}
headers = {'content-type': 'application/json'}


def auth(username, password):
    """
    Takes a username and password, returns an authentication token
    """
    data = {'data': {'username': username, 'password': password}}
    response = requests.post(API['login'], data=json.dumps(data),
                             headers=headers, verify=False)
    if response.status_code == 200:
        token = json.loads(response.content.decode('utf-8'))['data']['Token']
        headers['Authorization'] = 'Token ' + token
        return True

    return False


def update_ipv4(ipv4_settings):
    """
    Takes in a dict with ipv4 settings, and updates it to the AP
    """
    response = requests.put(API['lan'], data=json.dumps(ipv4_settings),
                            headers=headers, verify=False)
    if response.status_code == 204:
        return True
    return False


def get_ipv4():
    """
    Gets the ipv4 settings from the AP
    """
    response = requests.get(API['lan'], headers=headers, verify=False)
    if response.status_code == 200:
        ipv4_settings = json.loads(response.content.decode('utf-8'))
        return ipv4_settings
    return None


def apply_changes():
    """
    Applies any saved changes to the AP
    """
    response = requests.post(API['apply'], headers=headers, verify=False)
    if response.status_code == 200:
        success = json.loads(response.content.decode('utf-8'))['data']['success']
        return success
    return None


def has_changes():
    """
    Verifies whether or not there are saved changes that are not applied
    """
    response = requests.get(API['apply_status'], headers=headers, verify=False)
    if response.status_code == 200:
        has_update = json.loads(response.content.decode('utf-8'))['data']['has_update']
        return has_update
    return None


def verify_changes():
    """
    Verifies if the ipv4 settings were changed using ping
    """
    response = os.system('ping -c 1 ' + new_ip)
    if response == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    username = 'admin'
    password = 'admin'

    new_ip = '10.0.0.10'

    auth(username, password)
    ipv4_settings = get_ipv4()

    if ipv4_settings is not None:
        ipv4_settings['data']['ip_address'] = new_ip
        update_ipv4(ipv4_settings)

    if has_changes():
        apply_changes()
        print('Device is restarting...')
        sleep(40)  # measurements indicate that the device takes about 36 seconds to restart.

    if verify_changes():
        print('New access point IPv4 is ' + new_ip)
    else:
        print('Couldn\'t change access point IPv4 settings.')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
