import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pve_vmpost(Endpoint, Port, Node, vmid, api_command="nd", token="nd"):
    # Match the API Command to the API Component, that we will call
    assert api_command != "nd"
    assert token != "nd"
    match api_command:
        case "start":
            api_command_url = "/status/start"
        case "stop":
            api_command_url = "/status/stop"
        case "restart":
            api_command_url = "/status/restart"
        case "shutdown":
            api_command_url = "/status/shutdown"
        case _:
            print("Error")
            return("Error")
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
        return "error"
    elif r.status_code == 200:
        return api_command
    else:
        print("Fatel Error")
        return "error"
