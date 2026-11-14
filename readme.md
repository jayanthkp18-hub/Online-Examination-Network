# Online Examination Network using TCP Socket Programming and SDN

## 1. Project Overview

This project implements a multi-user online examination application using **TCP Socket Programming** and **Software-Defined Networking (SDN)**.

The project uses:

- **Python TCP Sockets** for communication between the examination server and student clients.
- **Multithreading** to handle multiple student connections.
- **Mininet** to emulate the network topology.
- **Open vSwitch (OVS)** to provide software-based switching.
- **OS-Ken** as the SDN controller.
- **OpenFlow 1.3** for communication between the controller and the switch.

### Network Topology

| Node | Role | IP Address |
|---|---|---|
| h1 | Examination Server | 10.0.0.1 |
| h2 | Student 1 | 10.0.0.2 |
| h3 | Student 2 | 10.0.0.3 |
| s1 | Open vSwitch | — |

The examination server runs on `h1`, while student clients connect from `h2` and `h3`.

---

## 2. Prerequisites

The project is designed to run on Ubuntu.

Ensure that the following software is installed:

- Python 3
- Python virtual environment support
- Mininet
- Open vSwitch
- iperf3 (for network performance testing)

---

## 3. Initial Installation and Setup

These steps are required only during the initial setup.

### Step 1: Update package repositories

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install required system packages

```bash
sudo apt install -y python3 python3-pip python3-venv mininet openvswitch-switch iperf3
```

### Step 3: Start Open vSwitch

```bash
sudo systemctl enable --now openvswitch-switch
```

Verify that Open vSwitch is running:

```bash
sudo systemctl status openvswitch-switch
```

### Step 4: Navigate to the project directory

```bash
cd ~/online-exam
```

### Step 5: Create a Python virtual environment

```bash
python3 -m venv venv
```

### Step 6: Activate the virtual environment

```bash
source venv/bin/activate
```

### Step 7: Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install os-ken
```

Verify the OS-Ken installation:

```bash
osken-manager --version
```

**Note:** The virtual environment is used to run the OS-Ken controller. Mininet and Open vSwitch are installed as system packages.

---

## 4. Running the Project

Once the initial installation is complete, follow the steps below to start the examination network.

**Important:** Use four separate terminal windows. Start the SDN controller before starting the Mininet topology.

### Terminal 1: Start the OS-Ken SDN Controller

Navigate to the project directory:

```bash
cd ~/online-exam
```

Activate the Python virtual environment:

```bash
source venv/bin/activate
```

Start the OS-Ken controller:

```bash
osken-manager --ofp-tcp-listen-port 6653 controller.py
```

This starts the SDN controller and makes it listen on TCP port `6653` for OpenFlow connections.

Keep this terminal running.

### Terminal 2: Start the Mininet Topology

Navigate to the project directory:

```bash
cd ~/online-exam
```

Start the topology:

```bash
sudo python3 topology.py
```

This creates the Mininet network and starts the Mininet command-line interface.

#### Verify the network configuration

Display the connected virtual network devices:

```text
sh ovs-vsctl show
```

Check connectivity between all hosts:

```text
pingall
```

A successful result should show:

```text
0% dropped
```

#### Verify OpenFlow rules

Display the OpenFlow 1.3 flow entries installed on the switch:

```text
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

This displays the flow rules installed on switch `s1`.

#### Start the examination server

Run the server on host `h1`:

```text
h1 python3 server.py &
```

Verify that the server is listening on port `5000`:

```text
h1 ss -lntp | grep 5000
```

The server should be listening on:

```text
0.0.0.0:5000
```

Keep the Mininet terminal running.

### Terminal 3: Start Student 1

Open a new terminal and execute:

```bash
sudo mnexec -a $(pgrep -f 'mininet:h2' | head -1) python3 ~/online-exam/client.py
```

This executes the student client inside Mininet host `h2`.

Student 1 can now connect to the examination server and attempt the examination.

### Terminal 4: Start Student 2

Open another terminal and execute:

```bash
sudo mnexec -a $(pgrep -f 'mininet:h3' | head -1) python3 ~/online-exam/client.py
```

This executes the student client inside Mininet host `h3`.

Student 2 can now connect to the examination server and attempt the examination.

**Note:** Run the two student clients in separate terminals. They can connect independently to the multithreaded examination server.

---

## 5. Important Verification Commands

Run these commands inside the Mininet CLI to inspect the network.

| Command | Purpose |
|---|---|
| `sh ovs-vsctl show` | Displays the OVS configuration and controller connection |
| `pingall` | Tests connectivity between all Mininet hosts |
| `dump` | Displays host and switch information, including process IDs |
| `sh ovs-ofctl -O OpenFlow13 show s1` | Displays switch and port information |
| `sh ovs-ofctl -O OpenFlow13 dump-flows s1` | Displays installed OpenFlow rules |
| `sh ovs-ofctl -O OpenFlow13 dump-ports s1` | Displays switch port statistics |
| `h1 ss -lntp \| grep 5000` | Checks whether the examination server is listening |

---

## 6. Stopping the Project

Follow this order to shut down the project safely.

### Step 1: Stop the student clients

Press `Ctrl + C` in the student client terminals.

### Step 2: Exit Mininet

In Terminal 2, enter:

```text
exit
```

### Step 3: Stop the SDN controller

In Terminal 1, press:

```text
Ctrl + C
```

### Step 4: Clean up Mininet

Open a normal Ubuntu terminal and execute:

```bash
sudo mn -c
```

This cleans up the Mininet network and removes leftover virtual network configurations.

---

## 7. Troubleshooting

### Issue 1: Unable to contact remote controller

If Mininet displays:

```text
Unable to contact remote controller at 127.0.0.1:6653
```

Make sure that:

1. The OS-Ken controller is running in Terminal 1.
2. The controller is listening on port `6653`.
3. The controller was started before the Mininet topology.

### Issue 2: Pingall shows packet loss

Run:

```text
sh ovs-vsctl show
```

Check whether the controller is connected.

Verify the installed flow rules:

```text
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

If necessary, stop the project and restart the controller before starting Mininet.

### Issue 3: Student client cannot connect

Check whether the examination server is running:

```text
h1 ss -lntp | grep 5000
```

Also verify network connectivity:

```text
pingall
```

Ensure that the student clients are executed inside their respective Mininet hosts.

### Issue 4: Student client cannot find the Mininet host

Check the available Mininet processes:

```bash
pgrep -af 'mininet:h'
```

Make sure the Mininet topology is running before launching the student clients.

---

## 8. Project Execution Summary

The overall execution sequence is:

1. Install the system packages and Python dependencies.
2. Start the OS-Ken SDN controller.
3. Start the Mininet topology.
4. Verify network connectivity using `pingall`.
5. Verify the OpenFlow rules installed on the switch.
6. Start the examination server on `h1`.
7. Launch Student 1 from `h2`.
8. Launch Student 2 from `h3`.
9. Complete the examination and observe the results on the server.

**The project demonstrates TCP-based examination communication integrated with an SDN-controlled Mininet network using OpenFlow 1.3.**