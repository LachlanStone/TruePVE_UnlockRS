from time import sleep
import websockets
import json
import ssl

nd = "NotDefined"
token = "NotDefined"  # This is temp until i define it in code under the def later


async def unlock_dataset(
    endpoint, dataset, passphrase, force=False, username=nd, password=nd
):
    uri = f"wss://{endpoint}/websocket"
    # Define what variables need to be configured for the appliaction to funtion
    print(f"Attempting to connect to TrueNAS at {uri}")
    # WebSocket Comunication Component that is being used
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(uri=uri, ssl=context) as ws:
        # Connect to the WebSocket
        await ws.send(json.dumps({"msg": "connect", "version": "1", "support": ["1"]}))
# Confirming the websocket answer to wait longer here
        await ws.recv()

        # Confirm method for authentication with the websocket API
        if username != nd and password != nd:
            # Authenticate with WebSocket via UserPass
            await ws.send(
                json.dumps(
                    {
                        "msg": "method",
                        "id": "1",
                        "method": "auth.login",
                        "params": [username, password],
                    }
                )
            )
            await ws.recv()
        elif token != nd:
            print("Token Connection is not setup yet")
            exit()
        else:
            print(
                """Fatel Error: Exiting Application
            User and Password or Token is not defined
            One of the above options has to be defined"""
            )

        # Error Checking for the WebSocket has connected
        await ws.send(json.dumps({"msg": "method", "id": "2", "method": "core.ping"}))
        status = json.loads(await ws.recv())["result"]
        assert status == "pong"  # Confirm that
        # dataset = "PVEScale_HDD"  # ← replace with your actual dataset
        args = json.dumps(
            {
                "msg": "method",
                "id": "3",
                "method": "pool.dataset.unlock",
                "params": [
                    dataset,
                    {
                        "force": force,
                        "recursive": False,
                        "toggle_attachments": True,
                        "datasets": [{"name": dataset, "passphrase": passphrase}],
                    },
                ],
            }
        )
        await ws.send(args)
        id = json.loads(await ws.recv())["result"]
        # Get the state of the dataset after we unlock it
        ## If the unlock is still running then check again every i + time
        for i in range(1,20):
            args = json.dumps(
                {
                    "msg": "method",
                    "id": "4",
                    "method": "core.get_jobs",
                    "params": [[["id", "=", id]]],
                }
            )
            await ws.send(args)
            response = json.loads(await ws.recv())
            # print(response)
            # Safely access job details to avoid errors if the job succeeds
            # Extract the Response Infomation from the result
            job = response.get("result", [{}])[0]
            job_id = job.get("id")
            job_state = job.get("state")
            # Check if the Unlock is still running
            if job_state == "RUNNING" or job_state == "nd":
                sleep(i)
            elif job_state == "SUCCESS" or job_state == "FAILED":
                break
            elif i == 19:
                print("Fatel Error")
                await(ws.close)
            else:
                print("Fatel Error")
                print(job_state)
                await(ws.close)

        # Check the Status of the Dataset
        # Fail Forward as the response, can be the data is allready unlocked
        job_event = None
        try:
            if job.get("result") and job["result"].get("failed"):
                if dataset in job["result"]["failed"]:
                    job_event = job["result"]["failed"][dataset].get("error")
        except AttributeError:
            pass # Handle cases where 'failed' or 'result' might be None
        if job_event == "Invalid Key":
            print("Invalid PassPhase Key Provided")
            return ("error")
        elif job_state == "FAILED" and job.get("exc_info"):           
            # Check if 'exc_info' and 'extra' exist before accessing
            if not job.get("exc_info") or not job["exc_info"].get("extra"):
                print("Fatel Error: Missing 'exc_info' or 'extra' in job details.")
                print (job.get("exc_info"))
                await ws.close()
                exit()
            error_message = job["exc_info"]["extra"][0][1]
            # Fail Forward - As the DataSet is allready unlocked
            if error_message == f"{dataset} dataset is not locked":
                print(
                    f"Polling Job ID: {job_id}, DatatSet: {dataset}, Status: Storage already unlocked"
                )
                await ws.close()
                return "already"
            # Fail due to error not a error on the machine
            else:
                print("Fatel Error")
                await ws.close()
                return("error")
        # DataSet was unlocked and is healthy
        elif job_state == "RUNNING" or job_state == "SUCCESS":
            print(
                f"Polling Job ID: {job_id}, DatatSet: {dataset}, Status Storage unlocked"
            )
            await ws.close()
            return "unlocked"
