# Documentation
This documentation outlines all the basic tutorials for getting started with Build Your Own LOLBins (BYOL).

## Table of Contents
- [Getting Started](#Getting%20Started)
- [Scan](#Scan)
    - [Creating Scan](#Creating%20Scan)
        + [Adding Simulation](#Adding%20Simulation)
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
    a. **IP Address**: Ensure that the target machine has Internet connection to download payloads from the repo.
    b. **Username**: Use a Local Administrator account to enable Interactive Logon session. 
    c. **Password** 
3. Select `Create Scan`