import requests
import urllib3
import json
from unlockrs.main import TrueNas_VMID

debug = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#TODO Looking to migrate the pve_vmapi and pve_vmstatus to a seperate module
#TODO Setup a loop funtion for pve scanning of the component

def pve_vmstatus(Endpoint, Port, Node, vmid, token):
# Set the URL Paramater for the Status of the VM
    url = "https://" + Endpoint + ":" + Port + "/api2/json/nodes/" + Node + "/qemu/" + vmid + "/status/current"
# Set the Token for the Authorization Header within the system
    params = {
        "Authorization": f"PVEAPIToken={token}"
    }
    # Disable Certifificate Verifivation
    # r = requests.get(url, verify=False)
    r= requests.get(url, verify=False, headers=params)
    if r.status_code != 200:
        print("Error, with the API got Status Code:", r.status_code)
        print(r.reason)
        exit()
    elif r.status_code == 200:
        json_data = json.loads(r.text)
        # print(json_data["data"]["status"])
        status = json_data["data"]["status"]
        return status    
    else:
        print("Fatel Error")
        exit()

def pve_vmapi(Endpoint, Port, Node, vmid, api_command, token):
# DEF Variables
    # Match the API Command to the API Component, that we will call
    match api_command:
        case "start":
            api_command_url = "/status/start"
        case "stop":
            api_command_url = "/status/stop"
    # Set the URL Paramater for API Command being sent
    url = "https://" + Endpoint + ":" + Port + "/api2/json/nodes/" + Node + "/qemu/" + vmid + api_command_url
    # Set the Token for the Authorization Header within the system
    params = {
        "Authorization": f"PVEAPIToken={token}"
    }
    # Code Starts Here
    r= requests.post(url, verify=False, headers=params)
    if r.status_code != 200:
        print("Error, with the API got Status Code:", r.status_code)
        print(r.reason)
        exit()
    elif r.status_code == 200:
        print("Success")
        for i in range(5):
            status= pve_vmstatus(Endpoint, Port, Node, vmid, token)
            if status == "running":
                print("System Running")
                print(i)
                return 
            elif i == 4 and vmid == TrueNas_VMID and status =="stopped":
                print(f"ERROR |  TrueNas Virtual Machine with ID:{vmid} failed to start")
                exit()
            elif i == 4 and status == "stopped":
                print(f"ERROR | Virtual Machine with ID:{vmid} failed to start")
                return
            elif i == 4:
                print("Fatel Error")
                exit()
    else:
        print("Fatel Error")
        exit()