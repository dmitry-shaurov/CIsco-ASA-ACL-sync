import urllib3
import requests
import json


asa1 = "10.78.104.3"
asa2 = "10.78.104.4"
log_pwd = ('shaurov', 'shaurov')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##############################
### NETWORK OBJECTS GROUPS ###
##############################
def get_networkobjectgroups(host):
    url_networkobjectgroups = "https://{}/api/objects/networkobjectgroups".format(host)
    networkobjectgroups = requests.get(url_networkobjectgroups,
                                  verify=False,
                                  auth=log_pwd)
    return networkobjectgroups

def delete_networkobjectgroups(host, obj):
    url_networkobjectgroups = "https://{}/api/objects/networkobjectgroups/{}".format(host, obj)
    networkobjectgroups = requests.delete(url_networkobjectgroups,
                                     verify=False,
                                     auth=log_pwd)

def post_networkobjectgroups(host, payload):
    """
    Every HTTP POST request must include a JSON body (an attribute)
    https://www.cisco.com/c/dam/en/us/td/docs/security/asa/api/asapedia_rest_api_132.pdf
    """

    url_networkobjectgroups = "https://{}/api/objects/networkobjectgroups".format(host)
    networkobjectgroups = requests.post(url_networkobjectgroups,
                                  verify=False,
                                  auth=log_pwd,
                                  data=json.dumps(payload),
                                  headers={'Content-Type': 'application/json'})

def change_networkobjectgroups():
    networkobjectgroups_asa1 = get_networkobjectgroups(asa1).json()
    networkobjectgroups_asa2 = get_networkobjectgroups(asa2).json()
    networkobjectgroups_asa1_list = []
    networkobjectgroups_asa2_list = []

    for i in networkobjectgroups_asa1.get("items"):
        networkobjectgroups_asa1_list.append(i.get("name"))
    for i in networkobjectgroups_asa2.get("items"):
        networkobjectgroups_asa2_list.append(i.get("name"))
    # Does ASA2 have got enough networkobjectgroups? Let's add some!
    for name in networkobjectgroups_asa1_list:
        if name not in networkobjectgroups_asa2_list:
            for obj in networkobjectgroups_asa1.get("items"):
                if obj.get("name") == name:
                    post_networkobjectgroups(asa2, obj)
                    print("networkobjectgroups <<<{}>>> has been successfully added to the asa2".format(name))
    # Does ASA2 have any extra networkobjectgroups? Let's delete them!
    for name in networkobjectgroups_asa2_list:
        if name not in networkobjectgroups_asa1_list:
            delete_networkobjectgroups(asa2, name)
            print("networkobjectgroups <<<{}>>> has been successfully deleted from the asa2".format(name))

change_networkobjectgroups()
