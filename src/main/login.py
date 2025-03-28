import os
import requests
import time
import json
import subprocess
import netTest
from urllib.parse import quote


def check_login_activity():
    return


def get_services(ePortalUrl, queryString):
    services = requests.get(
        ePortalUrl + "InterFace.do?method=getServices&queryString=" + queryString)
    return services.content.decode('utf-8')


def login(ePortalUrl, userId, password, service, queryString, passwordEncrypt):
    login_url = ePortalUrl + "InterFace.do?method=login"
    login_url += "&userId=" + userId
    login_url += "&password=" + password
    login_url += "&service=" + service
    login_url += "&queryString=" + queryString
    login_url += "&operatorPwd="
    login_url += "&operatorUserId="
    login_url += "&validcode="
    login_url += "&passwordEncrypt=" + passwordEncrypt
    login_ = requests.get(login_url)
    return login_.content.decode('utf-8')


def get_info(ePortalUrl, userIndex):
    info_url = ePortalUrl + "InterFace.do?method=getOnlineUserInfo"
    info_url += "&userIndex=" + userIndex
    info_ = requests.get(info_url)
    return info_.content.decode('utf-8')


def login_main(configDict: dict):
    entranceHost = configDict["schoolConfig"]["entranceHost"]
    checkOnline = netTest.checkNetworkActivity(configDict)
    entranceNetworkFlag = netTest.curlMethod(entranceHost)

    if (checkOnline == 1):
        print(">INFO Already linked.")
    elif ((checkOnline == 2) and (entranceNetworkFlag == 2)):
        ePortalUrl_entrance = requests.get(entranceHost)
        ePortalUrl_main = ePortalUrl_entrance.text[32:-12]
        ePortalUrl = ePortalUrl_main[0:25]
        queryString = quote(quote(ePortalUrl_main[35:]))
        services_json = json.loads(get_services(ePortalUrl, queryString))
        services_list_json = json.loads(services_json['services'])
        for i in range(len(services_list_json)):
            if (serviceShowName == services_list_json[i]['serviceShowName']):
                serviceName = quote(
                    quote(services_list_json[i]['serviceName']))
                break
        login_info_json = login(ePortalUrl, userId, password,
                                serviceName, queryString, passwordEncrypt)
        login_info = json.loads(login_info_json)
        print(login_info)
        if (login_info['result'] == "fail"):
            print(">ERROR Login Fail")
        elif (login_info['result'] == "success"):
            print(">INFO Login success")
            userIndex = login_info['userIndex']
            config_data['userIndex'] = userIndex
            os.remove(config_json_file)
            with open(config_json_file, 'w') as file:
                file.write(json.dumps(config_data))

            user_info = json.loads(get_info(ePortalUrl, userIndex))
            with open(info_json_file, 'w') as file:
                file.write(json.dumps(user_info))
    else:
        print(">ERROR Unable to entrance.")
