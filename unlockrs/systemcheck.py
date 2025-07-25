import socket
import asyncio
import ipaddress

async def port_check(endpoint="none", port="none"):
    assert endpoint != "none"
    assert port != "none"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2.0)
    result = sock.connect_ex((endpoint, int(port)))
    if result == 0:
        return "online"
    if result != 0:
        return "offline"
    else:
        print("Fatel Error")
    sock.close()
    return result