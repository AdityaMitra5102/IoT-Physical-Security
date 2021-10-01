Operating system: Ubuntu 21.04LTS

Update OS, Install python3, pip3
Install dependencies with
```
pip3 install -r requirements.txt
```
To setup arduino operations, run

```
sudo adduser $USER dialout
```
Make both scripts executable with
```
sudo chmod +x script.sh
sudo chmod +x script2.sh
```
Run this script on startup

Press Alt+F2 to open Run and enter
```
gnome-session-properties
```
Add script2.sh to startup programs here
