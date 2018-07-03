# Extract ovpn_tcp from https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
#!/usr/bin/env python3
import os, glob, socket, requests, time, json, subprocess
import re
from functools import reduce


SCRIPTS_DIR = "/path/to/dir"

class bcolors:
    HEADER = '\033[95m' if os.name is 'poslx' else ''
    OKBLUE = '\033[94m' if os.name is 'poslx' else ''
    OKGREEN = '\033[92m' if os.name is 'poslx' else ''
    WARNING = '\033[93m' if os.name is 'poslx' else ''
    FAIL = '\033[91m' if os.name is 'poslx' else ''
    ENDC = '\033[0m' if os.name is 'poslx' else ''
    BOLD = '\033[1m' if os.name is 'poslx' else ''
    UNDERLINE = '\033[4m' if os.name is 'poslx' else ''

out = []
index = 0
os.chdir(SCRIPTS_DIR)
ping_re_script = re.compile(r"time=(\d+\.*\d*)\s?ms.*")
hosts = glob.glob("*.tcp.ovpn")

def print_row(*row):
    global out

    print_str = ("{}. host: "+bcolors.OKBLUE+"{}"+bcolors.ENDC+",  ip: "+bcolors.OKBLUE+\
            "{}"+bcolors.ENDC+",  ping(ms): "+bcolors.HEADER+"{}"+bcolors.ENDC+\
            ",  location: {}- {},  lat_lng: {}, total_time_to_compute: {}ms").format(*row)
    out.append({"row":row, "print_str":print_str})
    print(print_str)

def finalize():
    global out
    print("--------------------\n------------------")
    print("The fastest server is: ")
    out.sort(key=lambda x:x['row'][3])

    if len(out) == 0:
        print(bcolors.FAIL,"NO HOST FOUND. IS YOUR INTERNET EVEN WORKING?", bcolors.ENDC)
        return

    print(out[0]['print_str'])
    print("-----------------------------")

    with open("speedtest.txt", "w") as z:
        for row in out:
            z.write(row['print_str'])
            z.write("\n")




print("{} configs found".format(len(hosts)))

for f in hosts:
    try:
        host = f.replace(".tcp.ovpn", "")

        begin_time = time.time()

        ip = socket.gethostbyname(host)

        location = requests.get("http://ipinfo.io/{}".format(ip)).text
        location = json.loads(location)

        if 'postal' in location:
            postal = location['postal']
        else:
            postal = ""

        lat_lng = location['loc']

        location = "{}, {}, {}".format(location['city'], location['region'], location['country'])

        if os.name is 'nt': # windows
            cmd = "ping.exe {}".format(ip)
        else: # otherwise, we assume POSIX
            cmd = "ping -c 4 -i 0.2 {}".format(ip) # -i for cross-request time 

        _p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        _p_resp = _p.communicate()[0]
        _p_resp = ping_re_script.findall(_p_resp.decode("UTF-8"))

        if len(_p_resp) == 0: 
            raise socket.gaierror;

        ping_resp = reduce(lambda x, y: float(x)+float(y), _p_resp) / len(_p_resp)
        ping_resp = int(ping_resp)

        end_time = time.time()
        time_diff = int((end_time - begin_time) * 1000)


        if(index > 3000): break
        index += 1
        print_row(index, host, ip, ping_resp, location, postal, lat_lng, time_diff)
    except socket.gaierror:
        print(bcolors.WARNING,"host not found: {}".format(host), bcolors.ENDC)
    except Exception as e:
        print("Can not parse for {}".format(host), e)
    except KeyboardInterrupt as e:
        print("Keyboard interrupt, finalizing now.", e)
        break
finalize()
