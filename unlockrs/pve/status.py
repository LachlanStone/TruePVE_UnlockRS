import requests
import urllib3
import json

debug = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO Looking to migrate the pve_vmapi and pve_vmstatus to a seperate module
# TODO Setup a loop funtion for pve scanning of the component


def pve_typecheck(Endpoint, Port, Node, vmid, token):
    # Set the URL Paramater for the Status of the VM
    headers = {"Authorization": f"PVEAPIToken={token}"}
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
    # Disable Certifificate Verifivation
    # r = requests.get(url, verify=False)
    r = requests.get(url, verify=False, headers=headers)
    json_data = json.loads(r.text)
    try:
        message = json_data["message"]
        if "does not exist" in message:
            status, vmname, type = pve_lxcstatus(Endpoint, Port, Node, vmid, headers)
            agent = "true"
            return status, agent, vmname, type
    except KeyError:
        pass  # If 'message' key doesn't exist, it's likely a successful response
    if r.status_code == 200:
        status = json_data["data"]["status"]
        agent = json_data["data"]["agent"]
        vmname = json_data["data"]["name"]
        type = "qemu"
        return status, agent, vmname, type
    elif r.status_code != 200:
        print("Error, with the API got Status Code:", r.status_code)
        print(r.reason)
        return "error" "error" "error"
    else:
        print("Fatel Error")
        return "error" "error" "error"

def pve_lxcstatus(Endpoint, Port, Node, vmid, headers):
    url = (
        "https://"
        + Endpoint
        + ":"
        + Port
        + "/api2/json/nodes/"
        + Node
        + "/lxc/"
        + vmid
        + "/status/current"
    )
    r = requests.get(url, verify=False, headers=headers)
    json_data = json.loads(r.text)
    status = json_data["data"]["status"]
    vmname = json_data["data"]["name"]
    type = json_data["data"]["type"]
    return status, vmname, type
