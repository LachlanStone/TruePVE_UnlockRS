import time
import asyncio

async def port_check(endpoint="none", port="none", duration=15, delay=2):
    assert endpoint != "none"
    assert port != "none"
    print(f"Checking system {endpoint}:{port}")
    tmax = time.time() + duration
    i = 1
    while time.time() < tmax:
        try:
            _reader, writer = await asyncio.wait_for(asyncio.open_connection(endpoint, port), timeout=5)
            writer.close()
            await writer.wait_closed()
            print(f"System {endpoint}:{port} is online")
            return "online"
        except:
            if delay:
                await asyncio.sleep(delay)
                print(f"Attempt {i} failed to connect")
                i += 1
    print(f"System {endpoint}:{port} is offline")
    return "offline"