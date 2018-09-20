#!/bin/bash

echo ""
echo "=========================================================================="
echo "= Pentest Attack Machine Setup                                           ="
echo "= Based on the setup from The Hacker Playbook                            ="
echo "=========================================================================="
echo ""

# Prepare tools folder
echo "[+] Creating tools folder in /opt"
mkdir /opt/tools/
echo ""

# Setting up metasploit with postgresql
echo "[+] Setting up metasploit with postgresql"
service postgresql start
service metasploit start
echo ""

# Adding postgresql and metasploit services rc.d defaults
echo "[+] Adding postgresql and metasploit to rc.d defaults"
update-rc.d -f postgresql defaults
update-rc.d -f metasploit defaults
echo ""

# Discover Scripts - Passive reconnaissance
echo "[+] Installing Discover Scripts"
cd /opt/tools/
git clone https://github.com/leebaird/discover.git
cd /opt/tools/discover/
/opt/tools/discover/setup.sh
echo ""

# SMBexec - Grab hashes out of the Domain Controller and reverse shells
# Step 1: Select option 1
# Step 2: Select option 4
# Step 3: Select option 5
echo "[+] Installing SMBexec"
cd /tmp/
git clone https://github.com/pentestgeek/smbexec.git
cd /tmp/smbexec/
echo "[+] Select option 1"
/tmp/smbexec/install.sh
echo "[*] Where did you install SMBexec?: "
read smbexecpath
$smbexecpath/smbexec/install.sh
echo ""

# Veil - Create Python based Meterpreter executable
echo "[+] Installing Veil Framework"
cd /opt/tools/
git clone https://github.com/Veil-Framework/Veil-Evasion.git Veil
cd /opt/tools/Veil/setup
/opt/tools/Veil/setup/setup.sh
echo ""

# WCE (Windows Credential Editor) - Pulls passwords from memory
echo "[+] Downloading and installing WCE (Windows Credential Editor)"
mkdir /opt/tools/wce/
cd /tmp/
wget http://www.ampliasecurity.com/research/wce_v1_41beta_universal.zip
unzip -d /opt/tools/wce/ wce_v1_41beta_universal.zip
rm -f wce_v1_41beta_universal.zip
echo ""

# Mimikatz - Pulls passwords from memory
echo "[+] Installing Mimikatz"
mkdir /opt/tools/mimikatz/
cd /tmp/
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.0.0-alpha-20150122/mimikatz_trunk.zip
unzip -d /opt/tools/mimikatz/ mimikatz_trunk.zip
rm -f mimikatz_trunk.zip
echo ""

# PeepingTom - Website snapshots
echo "[+] Installing PeepingTom"
cd /opt/tools/
git clone https://bitbucket.org/LaNMaSteR53/peepingtom.git
cd /opt/tools/peepingtom/
wget https://gist.githubusercontent.com/nopslider/5984316/raw/423b02c53d225fe8dfb4e2df9a20bc800cc78e2c/gnmap.pl
echo ""

# Download appropriate PhantomJS package
if $(uname -m | grep '64'); then
    wget http://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-x86_64.tar.bz2
    tar xf phantomjs-1.9.2-linux-x86_64.tar.bz2
    cp /opt/tools/peepingtom/phantomjs-1.9.2-linux-x86_64/bin/phantomjs .
else
    wget http://phantomjs.googlecode.com/files/phantomjs-1.9.2-linux-i686.tar.bz2
    tar xf phantomjs-1.9.2-linux-i686.tar.bz2
    cp /opt/tools/peepingtom/phantomjs-1.9.2-linux-i686/bin/phantomjs .
fi
echo ""

# Nmap script - Quicker scanning and smarter identification
echo "[+] Installing nmap scripts"
cd /usr/share/nmap/scripts/
wget https://raw.githubusercontent.com/hdm/scan-tools/master/nse/banner-plus.nse
echo ""

# PowerSploit - Scripts for post exploitation
echo "[+] Installing PowerSploit"
cd /opt/tools/
git clone https://github.com/mattifestation/PowerSploit.git
cd /opt/tools/PowerSploit/
wget https://raw.githubusercontent.com/obscuresec/random/master/StartListener.py
wget https://raw.githubusercontent.com/darkoperator/powershell_scripts/master/ps_encoder.py
echo ""

# Responder - Used to gain NTLM challenge/response
echo "[+] Installing Responder"
cd /opt/tools/
git clone https://github.com/SpiderLabs/Responder.git
echo ""

# SET (Social Engineering Toolkit) - Pre-installed on Kali Linux
echo "[+] Installing SET (Social Engineering Toolkit)"
cd /opt/tools/
git clone https://github.com/trustedsec/social-engineer-toolkit.git set
cd /opt/tools/set/
/opt/tools/set/setup.py install
echo ""

# Bypassuac - Used to bypass UAC in post exploitation
# → https://www.trustedsec.com/downloads/
echo "[+] Installing Bypass UAC"
cd /tmp/
wget https://www.trustedsec.com/files/bypassuac.zip
unzip bypassuac.zip
cp bypassuac/bypassuac.rb /opt/metasploit/apps/pro/msf3/scripts/meterpreter/
mv bypassuac/uac/ /opt/metasploit/apps/pro/msf3/data/exploits/
rm -Rf bypassuac
echo ""

# BeEF - cross-site scripting framework
# â†’ http://beefproject.com/
echo "[+] Installing BeEF"
apt-get install beef-xss
echo ""

# PEDA - Python Exploit Development Assistance for GDB
# â†’ Repository: https://github.com/longld/peda
echo "[+] Installing PEDA"
git clone https://github.com/longld/peda.git /opt/peda
echo "source /opt/peda/peda.py" >> ~/.gdbinit
echo ""

# The End
echo "[+] All tools installed successfully!"
echo "[+] ~~~ Happy Hacking! ~~~"
echo ""
