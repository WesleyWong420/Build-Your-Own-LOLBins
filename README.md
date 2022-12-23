# Build-Your-Own-LOLBins
![Python](https://img.shields.io/badge/python_3.10.9-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

Build Your Own LOLBins (BYOL) is a threat simulation platform used for demonstrating the weaponization and detection
of Living-off-the-Land binaries native to the Windows Operating System. 

## Inspiration
This project is highly inspired by [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) and aims to expand beyond the scope of that by eliminating atomicity in individual test cases and providing flexibility in customization.

## Featues
* LOLBins Chaining
* Self-Cleanup & Auto Destruct
* Commandline Obfuscation
  * Globufscation Wildcards
  * Character Substitution
* Customizable Payloads
* Custom Templates
* APT Procedural Examples
  * Astaroth Infection Chain
  * Lazarus Infection Chain
  * APT 37 STEEP#MAVERICK Persistence Chain
* MITRE ATT&CK Framework Support
* Executive Report
* Exportable Telemetry JSON Data

## Installation
The technical requirements of this project are:
* Python 3.10.9
* Windows 10 64-bit (Victim Virtual Machine)
<br>

**NOTE**: BYOL uses Windows Remote Management (WinRM) to communicate with the remote host.
> To enable WinRM on the victim machine:
```
$ winrm quickconfig
$ winrm set winrm/config/service '@{AllowUnencrypted="true"}'
$ winrm set winrm/config/service/auth '@{Basic="true"}'
$ netsh advfirewall firewall add rule name="WinRM" dir=in localport=5985 protocol=TCP action=allow
$ Set-NetConnectionProfile -NetworkCategory Private
```

## Usage
**NOTE**: BYOL requires admin privileges on the victim machine to enable Interactive Logon Session. 
> Only use Local Admin Account as the user credentials!


**NOTE**: BYOL only deploys command-line based obfuscation to bypass string matching rules, such as those written in Sigma Project. All file-based Proof-of-Concept payloads, e.g. byol.dll, byol.exe, byol.js etc do not have defensive capabilities and will be flagged by AV vendors. 
> Althrough not mandatory, it is recommended to disable any AV solutions before performing a scan simulation!

## Technique Coverage
| LOLBins | Variants | Objectives |
|:-----|:---------:|:-----------|
Certutil.exe | 5 | `Download` `ADS` `Encode` `Decode`
Msiexec.exe | 1 | `Execute`
Regsvr32.exe | 3 | `Execute` `AWL Bypass`
Cmstp.exe | 1 | `Execute`
Esentutl.exe | 2 | `ADS` `Credentials Dumping`
Rdrleakdiag.exe | 1 | `Credentials Dumping`
Makecab.exe | 1 | `Conceal`
Extract32.exe | 1 | `Decode`
Reg.exe | 3 | `AWL Bypass` `UAC Bypass`
Verclsid.exe | 1 | `Execute`
Regedit.exe | 1 | `Upload`
Mavinject.exe | 1 | `Execute`
Bitsadmin.exe | 1 | `Download`
Expand.exe | 2 | `Copy` `ADS`
Cscript.exe | 2 | `Execute`
Rundll32.exe | 7 | `Execute` `Download`
Mshta.exe | 3 | `Execute` `Download`
Wuauclt.exe | 1 | `Execute`
Eventvwr.exe | 1 | `UAC Bypass`
Pcalua.exe | 2 | `Execute`
Wmic.exe | 3 | `Execute`
Cmd.exe | 1 | `Execute`
Powershell.exe | 4 | `Execute`

## To-Do
- [ ] Export Report + JSON
- [X] WinRM Exceptions