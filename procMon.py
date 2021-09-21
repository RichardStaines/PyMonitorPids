import psutil
import datetime
import inspect


def get_method_name():
    frame = inspect.currentframe()
    caller_frame = caller_frame = inspect.getouterframes(frame)[1][0]
    caller_name = inspect.getframeinfo(caller_frame).function
    # print (caller_name)
    return caller_name


def get_process_list(firstCall):
    name = get_method_name()
    print (f'\n{name}')
    headers = ['pid', 'name', 'cpu_percent']
    procs = list()
    for proc in psutil.process_iter():
        try:
            if (firstCall):
                pInfoDict = proc.as_dict(attrs=headers)
            pInfoDict = proc.as_dict(attrs=headers)
            # Get process name & pid from process object.

            cpu_percent = pInfoDict['cpu_percent']
            processDetails = pInfoDict['pid'], pInfoDict['name'], cpu_percent
            if cpu_percent > 0:
                procs.append(processDetails)
                printListAsCsv (processDetails, True)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return procs


def getTS():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")


def printListAsCsv(items, includeTime=False):
    csvLine = ",".join([str(x) for x in items])
    if includeTime:
        csvLine = getTS() + ',' + csvLine
    print(csvLine)


if __name__ == '__main__':
    firstCall = True
    colHeaders = ['timestamp', 'pid', 'name', 'cpu']
    printListAsCsv (colHeaders)
    while True:
        procList = get_process_list(firstCall)
        firstCall = False
