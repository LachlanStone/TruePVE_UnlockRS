import requests
import urllib3
from unlockrs.main import TrueNas_VMID

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pve_vmpost(Endpoint, Port, Node, vmid, api_command, token):
    # DEF Variables
    # Match the API Command to the API Component, that we will call
    match api_command:
        case "start":
            api_command_url = "/status/start"
        case "stop":
            api_command_url = "/status/stop"
    # Set the URL Paramater for API Command being sent
    url = (
        "https://"
        + Endpoint
        + ":"
        + Port
        + "/api2/json/nodes/"
        + Node
        + "/qemu/"
        + vmid
        + api_command_url
    )
    # Set the Token for the Authorization Header within the system
    headers = {"Authorization": f"PVEAPIToken={token}"}
    # Code Starts Here
    r = requests.post(url, verify=False, headers=headers)
    if r.status_code != 200:
        print("Error, with the API got Status Code:", r.status_code)
        print(r.reason)
        exit()
    elif r.status_code == 200:
        print("Success")
        return api_command
    else:
        print("Fatel Error")
        exit()
