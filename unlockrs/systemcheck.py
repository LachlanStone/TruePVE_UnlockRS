import socket

async def port_check(endpoint="none", port="none"):
    assert endpoint != "none"
    assert port != "none"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2.0)
    for i in range(5):
        result = sock.connect_ex((endpoint, int(port)))
        if result == 0:
            sock.close()
            return "online"
        if i == 4 and result != 0:
            sock.close()
            print("System is Offline")
            exit()
        if result != 0:
            sock.close()
            exit()
        else:
            sock.close()
            print("Fatel Error")
            exit()
    sock.close()
    return result