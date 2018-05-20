import requests
import json

def get_acl(host):
    url_acl = "https://{}/api/objects/extendedacls/INSIDE_IN/aces".format(host)
    acl = requests.get(url_acl,
                       verify=False,
                       auth=log_pwd)
    return acl

def del_acl(host, obj):
    url_acl = "https://{}/api/objects/extendedacls/INSIDE_IN/aces/{}".format(host, obj)
    acl = requests.delete(url_acl,
                          verify=False,
                          auth=log_pwd)

def post_acl(host, payload):
    url_acl = "https://{}/api/objects/extendedacls/INSIDE_IN/aces".format(host)
    url_acl = requests.post(url_acl,
                            verify=False,
                            auth=log_pwd,
                            data=json.dumps(payload),
                            headers={'Content-Type': 'application/json'})

def change_acl():
    acl_asa1 = get_acl(asa1).json()
    acl_asa2 = get_acl(asa2).json()
    if acl_asa2 != {'messages': [{'level': 'Error', 'code': 'RESOURCE-NOT-FOUND', 'details': 'RESOURCE-NOT-FOUND'}]}:
        for ace in acl_asa2.get("items"):
            objectId = ace.get("objectId")
            del_acl(asa2, objectId)

    for ace in acl_asa1.get("items"):
        post_acl(asa2, ace)
