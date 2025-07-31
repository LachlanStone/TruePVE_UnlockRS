import requests
import urllib3
import json

debug = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO Looking to migrate the pve_vmapi and pve_vmstatus to a seperate module
# TODO Setup a loop funtion for pve scanning of the component


def pve_vmstatus(Endpoint, Port, Node, vmid, token):
    # Set the URL Paramater for the Status of the VM
    url = (
        "https://"
        + Endpoint
        + ":"
        + Port
        + "/api2/json/nodes/"
        + Node
        + "/qemu/"
        + vmid
        + "/status/current"
    )
    # Set the Token for the Authorization Header within the system
    headers = {"Authorization": f"PVEAPIToken={token}"}
    # Disable Certifificate Verifivation
    # r = requests.get(url, verify=False)
    r = requests.get(url, verify=False, headers=headers)
    if r.status_code != 200:
        print("Error, with the API got Status Code:", r.status_code)
        print(r.reason)
        return "error"
    elif r.status_code == 200:
        json_data = json.loads(r.text)
        status = json_data["data"]["status"]
        agent = json_data["data"]["agent"]
        print(agent)
        print(status)

        return status
    else:
        print("Fatel Error")
        return "error"
