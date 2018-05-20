import requests
import json

def get_networkobjects(host):
    url_networkobjects = "https://{}/api/objects/networkobjects".format(host)
    networkobjects = requests.get(url_networkobjects,
                                  verify=False,
                                  auth=log_pwd)
    return networkobjects

def delete_networkobjects(host, obj):
    url_networkobjects = "https://{}/api/objects/networkobjects/{}".format(host, obj)
    networkobjects = requests.delete(url_networkobjects,
                                     verify=False,
                                     auth=log_pwd)

def post_networkobjects(host, payload):
    """
    Every HTTP POST request must include a JSON body (an attribute)
    https://www.cisco.com/c/dam/en/us/td/docs/security/asa/api/asapedia_rest_api_132.pdf
    """

    url_networkobjects = "https://{}/api/objects/networkobjects".format(host)
    networkobjects = requests.post(url_networkobjects,
                                  verify=False,
                                  auth=log_pwd,
                                  data=json.dumps(payload),
                                  headers={'Content-Type': 'application/json'})

def change_networkobjects():
    networkobjects_asa1 = get_networkobjects(asa1).json()
    networkobjects_asa2 = get_networkobjects(asa2).json()
    networkobjects_asa1_list = []
    networkobjects_asa2_list = []

    for i in networkobjects_asa1.get("items"):
        networkobjects_asa1_list.append(i.get("name"))
    for i in networkobjects_asa2.get("items"):
        networkobjects_asa2_list.append(i.get("name"))
    # Does ASA2 have got enough networkobjects? Let's add some!
    for name in networkobjects_asa1_list:
        if name not in networkobjects_asa2_list:
            for obj in networkobjects_asa1.get("items"):
                if obj.get("name") == name:
                    post_networkobjects(asa2, obj)
    # Does ASA2 have any extra networkobject? Let's delete them!
    for name in networkobjects_asa2_list:
        if name not in networkobjects_asa1_list:
            delete_networkobjects(asa2, name)
