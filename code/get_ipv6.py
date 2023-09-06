import os
import re


def getIPv6Address(position: int = 1):
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    temp_ip = result[position - 1][0]
    with open('temp_ip.txt', 'w') as f:
        f.write('[%s]' % temp_ip)
    return temp_ip

def httpIPv6Address(ip: str, port: str):
    return "http://[%s]:%s" % (ip, port)