#!/usr/bin/env python3

import os, glob, socket, requests, time, json, subprocess
import re
from functools import reduce

SCRIPTS_DIR = "/path/to/dir"


def print_header():
    print("Host\t\tIP\t\tPing(ms)\tLocation/ Postal\t\t\t\tCoords\t\tHost\t\tOrg\t\tTotal time used(ms)")

out = []
def print_row(*row):
    global out

    row = "{}. host: {},  ip: {},  ping(ms): {},  location: {}- {},  lat_lng: {},  host: {},  org: {}, total_time_to_compute: {}".format(*row)
    out.append(row)
    print(row)

def finalize():
    global out
    print("The final data is: ")
    sort = sorted(out, key=lambda x:x[2])
    print(sort[0], sort[-1])

    with open("speedtest.txt", "w") as z:
        for row in sort:
            z.write(str(row))
            z.write("\n")

os.chdir(SCRIPTS_DIR)

ping_re_script = re.compile(r"time=(\d+\.*\d+) ms.*")
#print_header()

index = 0

for f in glob.glob("*.tcp443.ovpn"):
    try:
        host = '.'.join(f.split(".")[:3])
    #    print(host); continue

        begin_time = time.time()

        ip = socket.gethostbyname(host)
        
        location = requests.get("http://ipinfo.io/{}".format(ip)).text
        location = json.loads(location)

        if 'postal' in location:
            postal = location['postal']
        else:
            postal = ""
        
        provider = location['org']
        lat_lng = location['loc']
        hostname = location['hostname']

        location = "{}, {}, {}".format(location['city'], location['region'], location['country'])
        
        # print("Parsing data for {}({})".format(host, ip))

        _p = subprocess.Popen(['/bin/ping', "-c 4", "{}".format(ip)], stdout = subprocess.PIPE)
        _p_resp = _p.communicate()[0]
        _p_resp = ping_re_script.findall(_p_resp.decode("UTF-8"))
        ping_resp = reduce(lambda x, y: float(x)+float(y), _p_resp) / len(_p_resp)
        ping_resp = int(ping_resp)

        end_time = time.time()
        time_diff = int((end_time - begin_time) * 1000)
       

        index += 1
        print_row(index, host, ip, ping_resp, location, postal, lat_lng, hostname, provider, time_diff)

        if(index > 3000): break
    except Exception:
        print("Can not parse for {}".format(f))
finalize()
