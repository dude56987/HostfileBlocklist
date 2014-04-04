HostfileBlocklist
=================

Automaticly update your hosts file using online blocklists. Configurable via config files or the GUI.

####Unstable Packages for Ubuntu and Linux Mint

HostfileBlocklist Package

https://github.com/dude56987/HostfileBlocklist/blob/master/hostfileblocklist_UNSTABLE.deb

HostfileBlocklist-GUI Package

https://github.com/dude56987/HostfileBlocklist/blob/master/hostfileblocklist-gui_UNSTABLE.deb

####For Windows Users
1. Install Python if it is not already installed on your system. (https://www.python.org/download/releases/2.7.6/)
2. Download the source zip file. (https://github.com/dude56987/HostfileBlocklist/archive/master.zip)
3. Extract it anywhere.
4. Right click hostfileBlocklistWindowsLauncher.exe and run it as an administrator.

####Additional Documentation
* Online sources are not "trusted", all downloaded lists are striped of domain names and redirected to a ip address defined by the user(0.0.0.0 by default).
* Almost everything I could think of is modifiable with the config files.
* Backup of downloaded files is stored.
* Sites are collected permantly in "/etc/hostfileBlocklist/previousHostfile.host".