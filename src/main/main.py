import time
import json
from urllib.parse import quote
import login
import prettytable

configJsonFile = 'config.json'
info_json_file = 'info.json'


def countDelayTime(loopTime: list) -> int:
    k = [3600, 60, 1, 5]
    delayTime = k[3]
    for i in range(len(loopTime)):
        delayTime += k[i]*loopTime[i]
    return delayTime


def timeContrast(timeNow: time.struct_time, openTime: str, closeTime: str) -> bool:
    openTime = openTime.split(",")
    closeTime = closeTime.split(",")
    if openTime.split(",")[0] == "-1":
        left = True
    elif (countDelayTime([timeNow.tm_hour, timeNow.tm_min, timeNow.tm_sec]) >= countDelayTime(openTime)):
        left = True
    else:
        left = False
    if closeTime.split(",")[0] == "-1":
        right = True
    elif (countDelayTime([timeNow.tm_hour, timeNow.tm_min, timeNow.tm_sec]) < countDelayTime(closeTime)):
        right = True
    else:
        right = False
    if (left and right):
        return True
    else:
        return False


def main():
    # init
    print('------ Login Begin ------')
    with open(configJsonFile, 'r') as file:
        configDict = json.load(file)

    # print Config
    print('--- Config ---')
    table = prettytable(['type', 'key', 'value'])
    for type in configDict.keys():
        for key in configDict[type].keys():
            table.add_row([type, key, configDict[type][key]])
    print(table)

    # var
    global checkUnderControl
    global checkInOnlineTime
    # global checkLogin
    # global checkOnline
    loopTime = configDict["runConfig"]["loopTime"].split(",")
    delayTime = countDelayTime(loopTime)

    # main
    while (True):
        timeNow = time.localtime()

        # Checking if under network control& in online time
        if (configDict["runConfig"]["holidayMode"] == 1):
            checkUnderControl = False
            checkInOnlineTime = True
        else:
            checkUnderControl = True
            for timeTableItem in configDict["schoolConfig"]["timeTable"]:
                if timeNow.tm_wday in timeTableItem["wday"]:
                    checkInOnlineTime = timeContrast(
                        timeNow, timeTableItem["open"], timeTableItem["close"])

        # If in the online time, try login
        if checkInOnlineTime:
            try:
                checkLogin, checkOnline = login.login_main(configDict)
                if checkLogin:
                    print(">INFO: Success Login")
                if checkOnline:
                    print(">INFO: Success Online")
            except Exception as e:
                print(e)

        #
        if (configDict["runConfig"]["handleStart"] == 1):
            if not checkInOnlineTime:
                print(">WARN: Out of Online Time, exit with handleStart=1")
            exit
        elif (configDict["runConfig"]["handleStart"] == 2):
            print(">WARN: Run once, exit with handleStart=2")
            exit
        else:
            print(f">INFO: Delay {delayTime} seconds.")
            time.sleep(delayTime)


# Programe inplaces
if __name__ == "__main__":
    main()
