# NordVPN server benchmarker

This script can be used to find the best NordVPN servers(The one which has the least ping time). 


## Data collected from the servers
* Ping response time(using `\bin\ping`)
* Hostname, IP address
* Location -- City, Region, Country, Postal/ZIP code, Latitude-Longitude
* Organization to which the IP belongs
* real hostname of the IP(reverse DNS hostname)

## Instructions
1. Download all configs from [https://nordvpn.com/api/files/zip](https://nordvpn.com/api/files/zip)
2. Extract them to a folder and grab the path
3. MODIFY `SCRIPTS_DIR` in best\_server.py to your new path
4. execute `./best_server.py`
5. You can see the output in your terminal and it will also be saved in a file in the `SCRIPTS_DIR` path with name of `speedtest.txt`.

##Dependencies
* Python3
* `requests` module for python
