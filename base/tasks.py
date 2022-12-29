"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Celery Background Task Handler
"""

from celery import Task, shared_task
from celery.contrib.abortable import AbortableTask
from .models import Scan, UserVariant
from winrm.exceptions import *
from requests.exceptions import *
from urllib3.exceptions import *
import winrm, time, random

class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        scan = Scan.objects.get(id=args[0])
        scan.status = 'COMPLETED'
        scan.save()
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

class evilwinrm:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def testConnection(self):
        try:
            session = winrm.Session(self.host, auth=(self.username, self.password))
            session.run_cmd("whoami")
        except (TimeoutError, ConnectTimeoutError, MaxRetryError, ConnectTimeout, ConnectionError, ConnectionRefusedError, NewConnectionError):
            print("WinRM Error> Error occured when establishing a connection!")
            return False
        except AuthenticationError:
            print("WinRM Error> Error with Authentication Credentials!")
            return False
        except:
            print("WinRM Error> Generic Error!")
            return False

    def initializeConnection(self, pk):
        userVariant = UserVariant.objects.get(id=pk)
        session = winrm.Session(self.host, auth=(self.username, self.password))
        print(str(userVariant.payload))

        techniqueIndex = str(userVariant.payload).find(".exe")
        delimiterIndex = str(userVariant.payload).find("&")
        binary = str(userVariant.payload)[0:techniqueIndex+4]

        # if userVariant.highIntegrity == 'Yes':
        #     integrityLevel = " -RunLevel Highest"
        # else:
        #     integrityLevel = ""

        if delimiterIndex == -1:
            remaining = str(userVariant.payload)[techniqueIndex+5:]
            chainPayload = ""
        else:
            remaining = str(userVariant.payload)[techniqueIndex+5:delimiterIndex-1]
            chainRemaining = str(userVariant.payload)[delimiterIndex+2:]
            # chainPayload = f"""$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c {chainRemaining}'
            #                 $user = New-ScheduledTaskPrincipal -UserId "{self.username}" -LogonType Interactive -RunLevel Highest
            #                 $task = New-ScheduledTask -Action $action -Principal $user
            #                 $registeredTask = $task | Register-ScheduledTask -TaskName InteractiveTask -ErrorAction SilentlyContinue
            #                 if ($registeredTask -eq $null) {{ exit 5 }}
            #                 $registeredTask | Start-ScheduledTask
            #                 while ((Get-ScheduledTask -TaskName 'InteractiveTask').State -ne 'Ready') {{
            #                     Start-Sleep -Seconds 1
            #                 }}
            #                 Unregister-ScheduledTask -TaskName InteractiveTask -Confirm:$false"""

            chainPayload = f"""$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c {chainRemaining}'
                            $task = "Build Your Own LOLBins"
                            $registeredTask = Register-ScheduledTask -TaskName $task -Action $action -RunLevel Highest -ErrorAction SilentlyContinue
                            if ($registeredTask -eq $null) {{ 
                                Unregister-ScheduledTask -TaskName $task -Confirm:$false
                                exit 5 
                            }}
                            $registeredTask | Start-ScheduledTask
                            while ((Get-ScheduledTask -TaskName 'InteractiveTask').State -ne 'Ready') {{ Start-Sleep -Seconds 1 }}
                            Unregister-ScheduledTask -TaskName $task -Confirm:$false"""

        glob_list = list(userVariant.Variant.Technique.glob_set.all())
        if len(glob_list) != 0:
            glob = random.choice(glob_list)

        if binary[0:-4] != userVariant.Variant.Technique.name.lower() or len(glob_list) == 0:
            binary = "'" + binary + "'"
        else:
            binary = "Get-ChildItem " + glob.name

        # payloadToRun = f"""$binary = {binary}
        #                 $action = New-ScheduledTaskAction -Execute $binary -Argument '{remaining}'
        #                 $user = New-ScheduledTaskPrincipal -UserId "{self.username}" -LogonType Interactive{integrityLevel}
        #                 $task = New-ScheduledTask -Action $action -Principal $user
        #                 $registeredTask = $task | Register-ScheduledTask -TaskName InteractiveTask -ErrorAction SilentlyContinue
        #                 if ($registeredTask -eq $null) {{ exit 5 }}
        #                 $registeredTask | Start-ScheduledTask
        #                 while ((Get-ScheduledTask -TaskName 'InteractiveTask').State -ne 'Ready') {{
        #                     Start-Sleep -Seconds 1
        #                 }}
        #                 Unregister-ScheduledTask -TaskName InteractiveTask -Confirm:$false"""

        if userVariant.highIntegrity == 'Yes':
            payloadToRun = f"""$binary = {binary}
                $action = New-ScheduledTaskAction -Execute $binary -Argument '{remaining}'
                $task = "Build Your Own LOLBins"
                $registeredTask = Register-ScheduledTask -TaskName $task -Action $action -RunLevel Highest -ErrorAction SilentlyContinue
                if ($registeredTask -eq $null) {{ 
                    Unregister-ScheduledTask -TaskName $task -Confirm:$false
                    exit 5 
                }}
                $registeredTask | Start-ScheduledTask
                while ((Get-ScheduledTask -TaskName 'InteractiveTask').State -ne 'Ready') {{ Start-Sleep -Seconds 1 }}
                Unregister-ScheduledTask -TaskName $task -Confirm:$false"""
        else:
            payloadToRun = f"""$binary = {binary}
                $action = New-ScheduledTaskAction -Execute $binary -Argument '{remaining}'
                $task = "Build Your Own LOLBins"
                $registeredTask = Register-ScheduledTask -TaskName $task -Action $action -ErrorAction SilentlyContinue
                if ($registeredTask -eq $null) {{ 
                    Unregister-ScheduledTask -TaskName $task -Confirm:$false
                    exit 5 
                }}
                $registeredTask | Start-ScheduledTask
                while ((Get-ScheduledTask -TaskName 'InteractiveTask').State -ne 'Ready') {{ Start-Sleep -Seconds 1 }}
                Unregister-ScheduledTask -TaskName $task -Confirm:$false"""

        try:
            print(payloadToRun)
            result = session.run_ps(payloadToRun)
            errorLevel = result.status_code
            print(errorLevel)

            if chainPayload != "":
                print(chainPayload)
                result = session.run_ps(chainPayload)
                errorLevel = errorLevel + result.status_code
                print(errorLevel)
        except WinRMError:
            errorLevel = 5
            print("Ops, something is wrong!")
            pass

        return errorLevel

    def cleanup(self, pk):
        userVariant = UserVariant.objects.get(id=pk)
        session = winrm.Session(self.host, auth=(self.username, self.password))
        print(str(userVariant.cleanup))

        try:
            result = session.run_cmd(str(userVariant.cleanup))
            errorLevel = result.status_code
            print(errorLevel)
            print(result.std_out)
            print(result.std_err)
        except WinRMError:
            errorLevel = 5
            print("Ops, something is wrong!")
            pass

        return errorLevel

@shared_task(bind=True, base=AbortableTask)
def RunScan(self, pk):
    currentScan = Scan.objects.get(id=pk)
    connection = evilwinrm(currentScan.ip, currentScan.username, currentScan.password)

    if (connection.testConnection() != False):
        for simulation in currentScan.simulation_set.all():
            variant_list = list(simulation.UserVariant.all())
            for userVariant in simulation.UserVariant.all():
                if self.is_aborted():
                    return 'Task Stopped!'

                pos = variant_list.index(userVariant)
                print("Pos: " + str(pos))

                previousID = variant_list[pos - 1].id
                previousVariant = UserVariant.objects.get(id=previousID)

                if userVariant.chainPrevious == 'Yes' and (previousVariant.detected == True or previousVariant.detected == None):
                    userVariant.detected = None
                    userVariant.save()
                    print("Passed: " + str(userVariant.payload))
                else:
                    payloadErrorCode = connection.initializeConnection(userVariant.pk)
                    cleanupErrorCode = None
                    time.sleep(1.0)

                    if userVariant.cleanup and not userVariant.cleanup is None:
                        cleanupErrorCode = connection.cleanup(userVariant.pk)
                        time.sleep(1.0)

                    if payloadErrorCode != 0:
                        userVariant.detected = True
                        print("Variant Fail!")
                    else:
                        if cleanupErrorCode is None or cleanupErrorCode == 0:
                            userVariant.detected = False
                            print("Variant Success!")
                        else:
                            userVariant.detected = True
                            print("Variant Fail!")

                userVariant.save()
    
        currentScan.status = 'COMPLETED' 
    else:
        currentScan.status = 'ERROR'

    currentScan.save()