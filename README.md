# NordVPN server benchmarker

This script can be used to find the best NordVPN servers(The one which has the least ping time). 


## Data collected from the servers
* Ping response time (using `ping.exe` on Windows or `ping` utility for macOS and Linux)
* IP address
* City, Region, Country, Postal/ZIP code
* Latitude-Longitude

## Instructions
1. Download all configurations from [https://nordvpn.com/api/files/zip](https://nordvpn.com/api/files/zip)
2. Extract the `.zip` file to a folder and grab the path.
3. Modify `SCRIPTS_DIR` in best\_server.py to this path.
4. `python best_server.py`
5. You can see the output in your terminal
6. A file named `speedtest.txt` will also be saved on your `SCRIPTS_DIR`.

## Dependencies
* Python (Tested with Python3)
* `requests` module for python
