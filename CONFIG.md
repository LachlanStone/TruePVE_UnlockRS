## Configuration

The application is configured using the `Config.yml` file. Below is a detailed explanation of the configuration options.

```yaml
TrueNas:
  Endpoint: <TrueNAS_IP_or_Hostname>
  Port: <TrueNAS_Web_UI_Port>
  vmid: <PVE_VMID_for_TrueNAS>
  DataSet:
    Name: <ZFS_Dataset_Name>
    PassPhrase: <Dataset_Passphrase>
  Auth:
    Username: <TrueNAS_Username>
    Password: <TrueNAS_Password>

PVE:
  Endpoint: <PVE_IP_or_Hostname>
  Port: <PVE_API_Port>
  Node: <PVE_Node_Name>
  Token: <PVE_API_Token>

VMBootLoop:
  BootGroup1:
    StartDelay: <Delay_in_seconds_between_starting_each_VM>
    GroupStart: <Number_of_VMs_to_start_concurrently>
    VirtualMachines:
      - <VMID1>
      - <VMID2>
  BootGroup2:
    StartDelay: 10
    GroupStart: 1
    VirtualMachines:
      - <VMID3>
```

### Configuration Details

-   **TrueNas**:
    -   `Endpoint`: The IP address or hostname of your TrueNAS instance.
    -   `Port`: The port for the TrueNAS web interface (usually 80 or 443).
    -   `vmid`: The VM ID of the TrueNAS instance on your PVE server.
    -   `DataSet`:
        -   `Name`: The name of the ZFS dataset to unlock.
        -   `PassPhrase`: The passphrase for the encrypted dataset.
    -   `Auth`:
        -   `Username` & `Password`: Credentials for authenticating with the TrueNAS API.

-   **PVE**:
    -   `Endpoint`: The IP address or hostname of your PVE server.
    -   `Port`: The PVE API port (usually 8006).
    -   `Node`: The name of the PVE node where the VMs are located.
    -   `Token`: A valid PVE API token for authentication.

-   **VMBootLoop**:
    -   Define one or more boot groups (e.g., `BootGroup1`, `BootGroup2`).
    -   `StartDelay`: The delay in seconds between starting each VM in the group.
    -   `GroupStart`: The number of VMs to start concurrently.
    -   `VirtualMachines`: A list of VM IDs to be started in this group.
