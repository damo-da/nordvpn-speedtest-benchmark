# NordVPN server benchmarker

This script can be used to find the best NordVPN servers(The one which has the least ping time). 


## Data collected from the servers
* Ping response time (using `ping.exe` on Windows or `ping` utility for macOS and Linux)
* IP address
* City, Region, Country, Postal/ZIP code
* Latitude-Longitude

## Instructions
1. Download all configurations from [Here](https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip)
2. Extract the `.zip` file to a folder
3. Modify `SCRIPTS_DIR` in best\_server.py to this ovpn_tcp folder (Example /home/francis/nordvpn/ovpn_tcp)
4. `python best_server.py`
5. You can see the output in your terminal
6. A file named `speedtest.txt` will also be saved on your `SCRIPTS_DIR`.

## Dependencies
* Python (Tested with Python3)
* `requests` module for python
