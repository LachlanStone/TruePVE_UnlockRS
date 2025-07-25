from time import sleep
import websockets
import json

nd = "NotDefined"
token = "NotDefined"  # This is temp until i define it in code under the def later


async def unlock_dataset(endpoint, dataset, passphrase, force=False, username=nd, password=nd):
    # Define what variables need to be configured for the appliaction to funtion
    # TODO: Implement actual websocket connection and authentication
    print(f"Attempting to connect to TrueNAS at ws://{endpoint}/websocket")
    # WebSocket Comunication Component that is being used
    async with websockets.connect(f"ws://{endpoint}/websocket") as ws:
        # Connect to the WebSocket
        await ws.send(json.dumps({"msg": "connect", "version": "1", "support": ["1"]}))
        await ws.recv()
        # print(await ws.recv())

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
            # print(await ws.recv())
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

        # TODO Get the state from above as result with ID then call the jobs queue on truenas and get the state of the job after save 10 second
        # Get the state of the dataset after we unlock it
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
        # Safely access job details to avoid errors if the job succeeds
        # Extract the Response Infomation from the result
        job = response.get("result", [{}])[0]
        job_id = job.get("id")
        job_state = job.get("state")
        # Check the Status of the Dataset
        # Fail Forward as the response, can be the data is allready unlocked
        if job_state == "FAILED" and job.get("exc_info"):
            # The error message is at index 1 of the first list inside 'extra'
            error_message = job["exc_info"]["extra"][0][1]
            # Fail Forward - As the DataSet is allready unlocked
            if error_message == f"{dataset} dataset is not locked":
                print(
                    f"Polling Job ID: {job_id}, DatatSet: {dataset}, Status: Storage already unlocked"
                )
                await ws.close()
                return "Success"
            # Fail due to error not a error on the machine
            else:
                print("Fatel Error")
                await ws.close()
                exit()
        # DataSet was unlocked and is healthy
        elif job_state == "success":
            print(f"Polling Job ID: {job_id}, DatatSet: {dataset}, Status Storage unlocked")
            await ws.close()
            return "Success"
