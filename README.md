# TruePVE UnlockRS

TruePVE UnlockRS is a Python-based automation tool designed to streamline the process of managing virtual machines (VMs) on Proxmox VE (PVE) that depend on an encrypted ZFS dataset hosted on a TrueNAS instance. The tool automatically starts the TrueNAS VM, unlocks the specified dataset, and then boots up dependent VMs in a predefined order.

## Features

-   **Automated Startup Sequence:** Automatically starts the TrueNAS VM on the PVE server.
-   **ZFS Dataset Unlocking:** Connects to the TrueNAS instance to unlock an encrypted ZFS dataset.
-   **Sequential VM Boot-Up:** Starts specified groups of VMs in a configurable order after the dataset is unlocked.
-   **Configuration-Driven:** All settings, including credentials and VM groups, are managed through a central `Config.yml` file.
-   **System Checks:** Verifies the availability of PVE and TrueNAS services before proceeding.
-   **Concurrent VM Startup:** Supports starting multiple VMs concurrently within a boot group to speed up the process.

## Requirements

-   Python 3.x
-   The Python packages listed in `requirements.txt`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

For detailed configuration instructions, please see the [CONFIG.md](CONFIG.md) file.

## Usage

1.  **Complete the Configuration**: Fill out the `Config.yml` file with your specific PVE and TrueNAS details.
2.  **Run the Application**: Execute the `main.py` script to start the automation process.

    ```bash
    python3 /home/tetio/DevOps/TruePVE_UnlockRS/unlockrs/main.py
    ```

The script will then perform the following actions:
1.  Load the configuration.
2.  Check if the PVE and TrueNAS systems are online.
3.  Start the TrueNAS VM if it is not already running.
4.  Unlock the specified TrueNAS dataset.
5.  Start the VMs in the defined boot groups.

## Project Structure

-   `unlockrs/main.py`: The main entry point of the application.
-   `unlockrs/TrueNas/unlock.py`: Handles the connection to TrueNAS and the dataset unlocking process.
-   `unlockrs/pve/`: Contains modules for interacting with the Proxmox VE API (`start.py`, `status.py`).
-   `unlockrs/systemcheck.py`: Provides network port checking functionality.
-   `unlockrs/yaml_conf.py`: Manages loading and parsing the `Config.yml` file.
-   `Config.yml`: The central configuration file for all application settings.
-   `requirements.txt`: A list of Python dependencies for the project.
