# Documentation
This documentation outlines all the basic tutorials for getting started with Build Your Own LOLBins (BYOL).

## Table of Contents
- [Getting Started](#Getting%20Started)
- [Scan](#Scan)
    - [Creating Scan](#Creating%20Scan)
        + [Adding Simulation](#Adding%20Simulation)
        + [Editing Simulation Payloads](#Editing%20Simulation%20Payloads)
    + [Launching Scan](#Launching%20Scan)
        + [Scan Status](#Scan%20Status)
- [Template](#Template)
    - [Cloning Scan](#Cloning%20Scan)
    - [Creating Scan](#Creating%20Scan)
- [Library](#Library)
- [Report](#Report)
- [Admin Management](#Admin%20Management)

## Getting Started
To access the portal, use one of the following user accounts when prompted for login. The `admin` user has been granted privileged rights for [Admin Management](#Admin%20Management), and contains several scan history for ease of access. To build a scan from scratch, use the `user` account instead.

| Username | Password | Role          |
|:--------:|:--------:|:-------------:|
| admin    | admin    | Administrator |
| user     | user     | Default User  |

## Scan
All created and completed scans can be found in the **Scan Dashboard** under the **Scan** tab. Scans are sorted in descending order based on the latest update time.

### Creating Scan
1. Click on <img style="vertical-align: middle;" src="https://img.shields.io/badge/-%2B%20%20Create%20Scan-%2371c6dd">
2. Enter details for the Windows 10 target machine:
    * **IP Address**: Ensure that the target machine has Internet connection to download payloads from the repo.
    * **Username**: Use a Local Administrator account to enable Interactive Logon session. 
    * **Password**: User credentials for authentication.
3. Select <img style="vertical-align: middle;" src="https://img.shields.io/badge/-%20Create%20Scan-%2371c6dd">

### Adding Simulation
1. Click on <img style="vertical-align: middle;" src="https://img.shields.io/badge/-%20Add%20Simulation-%23696d97"> from the bottom.
2. Modify the newly added simulation by clicking the 🖊 button:
    * **Simulation Name**: Provide a new simulation name.
    * **Add Attacker Objective**: Select a technique from the library.
3. Select <img style="vertical-align: middle;" src="https://img.shields.io/badge/-%20Update%20Simulation-%2371c6dd">

### Editing Simulation Payloads
1. Expand the offcanvas by clicking on the objective box.
2. Modify the technique by clicking the 🖊 button beside of `SIMULATION DETAILS`:
    * **Payload**: Main payload for threat simulation. Must include `.exe` as the extension for LOLBins for globufscation to work.
    * (Optional) **Cleanup**: Command to wipe leftover artificats. Also used as verification to lower false positive rate. Optional but highly encouraged to include. 
    * (Optional) **Chain To Previous**: When enabled, the current technique will execute if the previous one succedeed. Disabled by default, only enable if the payload has dependencies from the previous technique.
    * (Optional) **High Integrity Process**: Run the payload under High Integrity context. Disabled by default, only enable for privileged actions such as Credentials Dumping and Process Injection.
3. Select <img style="vertical-align: middle;" src="https://img.shields.io/badge/-%20Update%20Details-%2371c6dd">