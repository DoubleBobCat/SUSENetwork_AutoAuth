import subprocess


def pingMethod(ip: str):
    try:
        result = subprocess.run(
            ['ping', '-c', '4', ip],
            capture_output=True, text=True, timeout=10
        )
        return 1
    except subprocess.TimeoutExpired:
        return 2
    except Exception as e:
        return 0


def curlMethod(host: str):
    try:
        output = subprocess.check_output("curl "+host, shell=True)
        if output.decode('utf-8')[0:15] == '<!DOCTYPE html>':
            return 1
        elif output.decode('utf-8')[0:31] == '<script>top.self.location.href=':
            return 2
        else:
            return 0
    except subprocess.CalledProcessError:
        return 0


def checkNetworkActivity(Config: dict):
    if Config["method"] == 1:
        return pingMethod(Config["ip"])
    elif Config["method"] == 2:
        return curlMethod(Config["host"])
    elif Config["method"] == 3:
        return (
            (pingMethod(Config["ip"]) == 1)
            or
            (curlMethod(Config["host"]) == 1)
        )
    else:
        return 0
