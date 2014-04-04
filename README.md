HostfileBlocklist
=================

Automatically update your hosts file using online blocklists. Configurable via config files or the GUI.

####The Latest Stable Release can be found at the link below

NOTE: The GUI package requires the main package as a dependency.<br>
https://github.com/dude56987/HostfileBlocklist/releases/tag/v0.5

####Unstable Packages for Ubuntu and Linux Mint
HostfileBlocklist Package<br>
https://github.com/dude56987/HostfileBlocklist/blob/master/hostfileblocklist_UNSTABLE.deb?raw=true

HostfileBlocklist-GUI Package<br>
https://github.com/dude56987/HostfileBlocklist/blob/master/hostfileblocklist-gui_UNSTABLE.deb?raw=true
####For Windows Users
1. Install Python if it is not already installed on your system. (https://www.python.org/download/releases/2.7.6/)
2. Download the source zip file. (https://github.com/dude56987/HostfileBlocklist/archive/master.zip)
3. Extract it anywhere.
4. Right click hostfileBlocklistWindowsLauncher.exe and run it as an administrator.

####Additional Documentation
* Online sources are not "trusted", all downloaded lists are striped of domain names and redirected to a ip address defined by the user(0.0.0.0 by default).
* Almost everything I could think of is modifiable with the config files.
* Backup of downloaded files is stored.
* Sites are collected permanently in "/etc/hostfileBlocklist/previousHostfile.host".
