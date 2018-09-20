
import Session
from Tool import Tool as Base
from Tool import ToolCategory

# TODO
# http-domino-enum-passwords.nse, http-fetch.nse, http-google-malware.nse, http-grep.nse, http-open-proxy.nse, http-robtex-reverse-ip.nse, http-robtex-shared-ns.nse, http-trace.nse
# http-vuln-cve2011-3192.nse

class NmapBase(Base):
    def __init__(self):
        return super().__init__(self._name, self._category, self._desc, self._example, self._cmd, self._args, self._parserName)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def setPort(self, port):
        self._port = port

    def run(self, **args):
        self._cmd = self._cmd.replace('${port}', self._port)
        if self._category == ToolCategory.Enumeration:
            self._cmd += ' -oX ${working_dir}/intel/' + self._name + '.xml'
        elif self._category == ToolCategory.VulnerabilityScanner:
            self._cmd += ' -oX ${working_dir}/intel/' + self._name + '.xml'
        elif self._category == ToolCategory.Reporting:
            self._cmd += ' -oX ${working_dir}/report/' + self._name + '.xml'
        elif self._category == ToolCategory.Exploit:
            self._cmd += ' -oX ${working_dir}/exploits/' + self._name + '.xml'
            
        self._category = str(self._category)
        super().run(custom_outfile = False)
        return

class NmapStealth(NmapBase):
    def __init__(self):
        self._desc = 'A combination of options used to make this as stealthly as possible.  This is meant to scan a single IP, but you can probably use it for the entire network.'
        self._name = 'NmapStealth'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap ${target} --data-length 36 -f -S ${arg1} -e eth0 -T paranoid'
        self._example = self._cmd
        self._port = '2202'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Enter an IP we want to show up as (10.0.0.1): ', end = '')
        maskIp = input()
        if maskIp == None or maskIp == '':
            maskIp = '10.0.0.1'

        self._cmd = self._cmd.replace('${arg1}', maskIp)

        super().run()
        return

class NmapAcars(NmapBase):
    def __init__(self):
        self._desc = 'Retrieves information from a listening acarsd daemon. Acarsd decodes ACARS (Aircraft Communication Addressing and Reporting System) data in ' + \
                     'real time.  The information retrieved by this script includes the daemon version, API version, administrator e-mail address and listening frequency.'
        self._name = 'NmapAcars'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} -script=acarsd-info ${target}'
        self._example = self._cmd
        self._port = '2202'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapAfp(NmapBase):
    def __init__(self):
        self._desc = 'Multiple ATP tools Apple Filing Protocol (AFP).'
        self._name = 'NmapAfp'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=afp-brute,afp-ls,afp-path-vuln,afp-serverinfo,afp-showmount ${target}'
        self._example = self._cmd
        self._port = '548'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return
        
class NmapAjp(NmapBase):
    def __init__(self):
        self._desc = 'Multiple AJP tools (Apache JServ Protocol).'
        self._name = 'NmapAjp'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=ajp-auth,ajp-brute,ajp-headers,ajp-methods,ajp-request ${target}'
        self._example = self._cmd
        self._port = '8009'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapAllseeingeye(NmapBase):
    def __init__(self):
        self._desc = 'The All-Seeing Eye service can listen on a UDP port separate from the main game server port (usually game port + 123). On receiving a packet ' + \
                     'with the payload "s", it replies with various game server status info.'
        self._name = 'NmapAllseeingeye'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -script=allseeingeye-info ${target}'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapAmqp(NmapBase):
    def __init__(self):
        self._desc = 'AMQP (advanced message queuing protocol) server.'
        self._name = 'NmapAmqp'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=amqp-info ${target}'
        self._example = self._cmd
        self._port = '5672'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapIdentd(NmapBase):
    def __init__(self):
        self._desc = ''
        self._name = 'NmapIdentd'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=auth-spoof ${target}'
        self._example = self._cmd
        self._port = '113'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapBackorifice(NmapBase):
    def __init__(self):
        self._desc = 'Backorifice is not done, do it manually, you will need a port list.'
        self._name = 'NmapBackorifice'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'NOT DONE'
        self._example = 'nmap -p ${port} -script=backorifice-brute ${target}'
        self._port = '31337'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapBACNet(NmapBase):
    def __init__(self):
        self._desc = 'BACNet Devices'
        self._name = 'NmapBACNet'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=bacnet-info ${target}'
        self._example = self._cmd
        self._port = '47808'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapBitcoin(NmapBase):
    def __init__(self):
        self._desc = 'Bitcoin'
        self._name = 'NmapBitcoin'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=bitcoin-getaddr,bitcoin-info,bitcoinrpc-info ${target}'
        self._example = self._cmd
        self._port = '8333,8332'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapBittorrent(NmapBase):
    def __init__(self):
        self._desc = 'Bittorrent is not done, do it manually, you will need a port list.'
        self._name = 'NmapBittorrent'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'NOT DONE'
        self._example = 'nmap -script=bittorrent-discovery ${target}'
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapBjnp(NmapBase):
    def __init__(self):
        self._desc = 'BJNP protocol is known to be supported by network based Canon devices.'
        self._name = 'NmapBjnp'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -script=bjnp-discover ${target}'
        self._example = self._cmd
        self._port = '8611,8612'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDiscoverScripts(NmapBase):
    def __init__(self):
        self._desc = 'More enumeration scripts.'
        self._name = 'NmapDiscoverScripts'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=broadcast-avahi-dos,broadcast-bjnp-discover,broadcast-db2-discover,broadcast-dhcp-discover,broadcast-dns-service-discovery,' + \
                    'broadcast-dropbox-listener,broadcast-hid-discoveryd,broadcast-igmp-discovery,broadcast-jenkins-discover,broadcast-listener,broadcast-ms-sql-discover,' + \
                    'broadcast-netbios-master-browser,broadcast-networker-discover,broadcast-novell-locate,broadcast-ospf2-discover,broadcast-pc-anywhere,' + \
                    'broadcast-pc-duo,broadcast-pim-discovery,broadcast-pppoe-discover,broadcast-rip-discover,broadcast-ripng-discover,broadcast-sonicwall-discover,' + \
                    'broadcast-sybase-asa-discover,broadcast-tellstick-discover,broadcast-upnp-info,broadcast-versant-locate,broadcast-wpad-discover,' + \
                    'broadcast-wsdd-discover,broadcast-xdmcp-discover ${target}'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        session.runThreadedCmd('nmap -6 --script broadcast-dhcp6-discover -oX ${working_dir}/discovery_report.out', 'Nmap-broadcast-dhcp6-discover')
        super().run()
        return

class NmapEigrp(NmapBase):
    def __init__(self):
        self._desc = 'Performs network discovery and routing information gathering through Cisco\'s Enhanced Interior Gateway Routing Protocol (EIGRP).'
        self._name = 'NmapEigrp'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=broadcast-eigrp-discovery ${target}'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCccam(NmapBase):
    def __init__(self):
        self._desc = 'Detects the CCcam service (software for sharing subscription TV among multiple receivers).'
        self._name = 'NmapCccam'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} ${target} --script=cccam-version'
        self._example = self._cmd
        self._port = '12000'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCics(NmapBase):
    def __init__(self):
        self._desc = 'CICS transaction ID enumerator for IBM mainframes.'
        self._name = 'NmapCics'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap --script=cics-enum,script=cics-info,cics-user-brute,cics-user-enum -p ${port} ${target} -oX ${working_dir}/cics_report.out'
        self._example = self._cmd
        self._port = '23'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCitrixWeb(NmapBase):
    def __init__(self):
        self._desc = 'Citrix PN Web Agent.'
        self._name = 'NmapCitrixWeb'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=citrix-enum-apps-xml,citrix-enum-servers-xml -p ${port} ${target} -oX ${working_dir}/citrix_web_report.out'
        self._example = self._cmd
        self._port = '80,443,8080'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCitrixIca(NmapBase):
    def __init__(self):
        self._desc = 'Citrix ICA Agent.'
        self._name = 'NmapCitrixIca'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=citrix-enum-servers,citrix-enum-apps -p ${port} ${target} -oX ${working_dir}/citrix_ica_report.out'
        self._example = self._cmd
        self._port = '1604'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapClam(NmapBase):
    def __init__(self):
        self._desc = 'Clam AV server.'
        self._name = 'NmapClam'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -sV --script=clamav-exec ${target} -oX ${working_dir}/clam_av_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCoap(NmapBase):
    def __init__(self):
        self._desc = 'Dumps list of available resources from CoAP endpoints.'
        self._name = 'NmapCoap'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p U:${port} -sU --script=coap-resources ${target} -oX ${working_dir}/coap_report.out'
        self._example = self._cmd
        self._port = '5683'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCouchDb(NmapBase):
    def __init__(self):
        self._desc = 'Couch DB.'
        self._name = 'NmapCouchDb'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=couchdb-databases,couchdb-stats ${target} -oX ${working_dir}/couchdb_report.out'
        self._example = self._cmd
        self._port = '5984'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCredSummary(NmapBase):
    def __init__(self):
        self._desc = 'Lists all discovered credentials.'
        self._name = 'NmapCredSummary'
        self._category = ToolCategory.Reporting
        self._cmd = 'nmap --script=creds-summary ${target} -oX ${working_dir}/cred_summary_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCups(NmapBase):
    def __init__(self):
        self._desc = 'Lists printers managed by the CUPS printing service. Lists currently queued print jobs of the remote CUPS service grouped by printer.'
        self._name = 'NmapCups'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=cups-info,cups-queue-info ${target} -oX ${working_dir}/cups_report.out'
        self._example = self._cmd
        self._port = '631'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapCvs(NmapBase):
    def __init__(self):
        self._desc = 'CVS server.'
        self._name = 'NmapCvs'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} --script=cvs-brute-repository,cvs-brute ${target} -oX ${working_dir}/cvs_report.out'
        self._example = self._cmd
        self._port = '2401'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDb2(NmapBase):
    def __init__(self):
        self._desc = 'IBM DB2 server.'
        self._name = 'NmapDb2'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=db2-das-info ${target} -oX ${working_dir}/db2_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDelugeRpc(NmapBase):
    def __init__(self):
        self._desc = 'Performs brute force password auditing against the DelugeRPC daemon.'
        self._name = 'NmapDelugeRpc'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} --script=deluge-rpc-brute ${target} -oX ${working_dir}/deluge_report.out'
        self._example = self._cmd
        self._port = '58846'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDhcp(NmapBase):
    def __init__(self):
        self._desc = 'Sends a DHCPINFORM request to a host on UDP port 67 to obtain all the local configuration parameters without allocating a new address.'
        self._name = 'NmapDhcp'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -sU -p ${port} --script=dhcp-discover ${target} -oX ${working_dir}/dhcp_report.out'
        self._example = self._cmd
        self._port = '67'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDistccd(NmapBase):
    def __init__(self):
        self._desc = 'Detects and exploits a remote code execution vulnerability in the distributed compiler daemon distcc. The vulnerability was disclosed in 2002, but is still\r\n' + \
                     'present in modern implementation due to poor configuration of the service.'
        self._name = 'NmapDistccd'
        self._category = ToolCategory.Exploit
        self._cmd = 'nmap -p ${port} ${target} --script distcc-exec --script-args="distcc-exec.cmd=\'id\'" -oX ${working_dir}/distccd_report.out'
        self._example = self._cmd
        self._port = '3632'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDnsEnum(NmapBase):
    def __init__(self):
        self._desc = 'DNS enumeration.'
        self._name = 'NmapDnsEnum'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} -sn ${target} --script=dns-blacklist,dns-nsid,dns-recursion,dns-service-discovery -oX ${working_dir}/dns_enum_report.out'
        self._example = self._cmd
        self._port = '53'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDnsVul(NmapBase):
    def __init__(self):
        self._desc = 'DNS vulnerability scanning.'
        self._name = 'NmapDnsVul'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} -sU ${target} --script=dns-fuzz,dns-brute,dns-random-srcport,script=dns-random-txid -oX ${working_dir}/dns_vul_report.out'
        self._example = self._cmd
        self._port = '53'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDocker(NmapBase):
    def __init__(self):
        self._desc = 'Docker enum.'
        self._name = 'NmapDocker'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap ${target} --script=docker-version -oX ${working_dir}/docker_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDominoUsers(NmapBase):
    # hasLotusNotesUser
    def __init__(self):
        self._desc = 'Attempts to discover valid IBM Lotus Domino users and download their ID files by exploiting the CVE-2006-5835 vulnerability.'
        self._name = 'NmapDominoUsers'
        self._category = ToolCategory.Exploit
        self._cmd = 'nmap -p ${port} ${target} --script=domino-enum-users -oX ${working_dir}/domino_user_report.out'
        self._example = self._cmd
        self._port = '1352'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDominoConsole(NmapBase):
    def __init__(self):
        self._desc = 'Runs a console command on the Lotus Domino Console using the given authentication credentials (see also: domcon-brute)\r\n' + \
                     'Performs brute force password auditing against the Lotus Domino Console.'
        self._name = 'NmapDominoUsers'
        self._category = ToolCategory.Exploit
        self._cmd = 'nmap -p ${port} ${target} --script=domcon-brute,domcon-cmd --script-args domcon-cmd.cmd="show server" -oX ${working_dir}/domino_console_report.out'
        self._example = self._cmd
        self._port = '2050'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapIphoto(NmapBase):
    def __init__(self):
        self._desc = 'Performs brute force password auditing against an iPhoto Library.'
        self._name = 'NmapIphoto'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} ${target} --script=dpap-brute -oX ${working_dir}/iphoto_console_report.out'
        self._example = self._cmd
        self._port = '8770'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapDrda(NmapBase):
    def __init__(self):
        self._desc = 'Attempts to extract information from database servers supporting the DRDA protocol.\r\n' + \
                     'Performs password guessing against databases supporting the IBM DB2 protocol such as Informix, DB2 and Derby.'
        self._name = 'NmapDrda'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} ${target} --script=drda-info,drda-brute -oX ${working_dir}/drda_report.out'
        self._example = self._cmd
        self._port = '50000'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapMultihomed(NmapBase):
    def __init__(self):
        self._desc = 'Attempts to discover multihomed systems by analysing and comparing information collected by other scripts. The information analyzed\r\n' + \
                     'currently includes, SSL certificates, SSH host keys, MAC addresses, and Netbios server names.'
        self._name = 'NmapMultihomed'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -PN -p445,443 --script=duplicates,nbstat,ssl-cert -oX ${working_dir}/multihomed_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapEnip(NmapBase):
    def __init__(self):
        self._desc = 'This NSE script is used to send a EtherNet/IP packet to a remote device that has TCP 44818 open.'
        self._name = 'NmapEnip'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -sU  -p 44818 --script=enip-info ${target} -oX ${working_dir}/enip_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFinger(NmapBase):
    def __init__(self):
        self._desc = 'Attempts to retrieve a list of usernames using the finger service.'
        self._name = 'NmapFinger'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=finger,fingerprint-strings ${target} -oX ${working_dir}/finger_report.out'
        self._example = self._cmd
        self._port = '79'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFirewalk(NmapBase):
    def __init__(self):
        self._desc = 'Firewalk that bitch.'
        self._name = 'NmapFirewalk'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap --script=firewalk --traceroute ${target} -oX ${working_dir}/firewalk_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFirewall(NmapBase):
    def __init__(self):
        self._desc = 'Other firewall stuff (be sure to firewalk it).'
        self._name = 'NmapFirewall'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap --script=firewall-bypass ${target} -oX ${working_dir}/firewall_bypass_report.out'
        self._example = self._cmd
        self._port = ''
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFume(NmapBase):
    def __init__(self):
        self._desc = 'Retrieves information from Flume master HTTP pages.'
        self._name = 'NmapFume'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=flume-master-info ${target} -oX ${working_dir}/fume_report.out'
        self._example = self._cmd
        self._port = '35871'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFox(NmapBase):
    def __init__(self):
        self._desc = 'Tridium Niagara Fox is a protocol used within Building Automation Systems.'
        self._name = 'NmapFox'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=fox-info ${target} -oX ${working_dir}/fox_report.out'
        self._example = self._cmd
        self._port = '1911'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFreelancer(NmapBase):
    def __init__(self):
        self._desc = 'Detects the Freelancer game server (FLServer.exe) service by sending a status query UDP probe.'
        self._name = 'NmapFreelancer'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=freelancer-info ${target} -oX ${working_dir}/freelancer_report.out'
        self._example = self._cmd
        self._port = '2302'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapFtp(NmapBase):
    def __init__(self):
        self._desc = 'FTP stuff.'
        self._name = 'NmapFtp'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} --script=ftp-anon,ftp-brute,ftp-libopie,ftp-proftpd-backdoor,ftp-syst,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 ${target} -oX ${working_dir}/ftp_report.out'
        self._example = self._cmd
        self._port = '21,990'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapHddTemp(NmapBase):
    def __init__(self):
        self._desc = 'Reads hard disk information (such as brand, model, and sometimes temperature) from a listening hddtemp service.'
        self._name = 'NmapHddTemp'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} -sV --script=hddtemp-info ${target} -oX ${working_dir}/hddtemp_report.out'
        self._example = self._cmd
        self._port = '7634'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapHnap(NmapBase):
    def __init__(self):
        self._desc = 'Retrieve hardwares details and configuration information utilizing HNAP, the "Home Network Administration Protocol".'
        self._name = 'NmapHnap'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} -sV --script=hnap-info ${target} -oX ${working_dir}/hnap_report.out'
        self._example = self._cmd
        self._port = '80,8080'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapHttpAnalytics(NmapBase):
    def __init__(self):
        self._desc = 'Analytic scripts for HTTP servers, and web sites.'
        self._name = 'NmapHttpAnalytics'
        self._category = ToolCategory.Forensics
        self._cmd = 'nmap -p ${port} http-affiliate-id.nse --script-args http-affiliate-id.url-path=${arg1} ${target} -oX ${working_dir}/http_anal_report.out'
        self._example = self._cmd
        self._port = '80,8080'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Enter the web site URL you want to analize: ', end = '')
        url = input()
        self._cmd = self._cmd.replace('${arg1}', url)
        super().run()
        return

class NmapHttpEnum(NmapBase):
    def __init__(self):
        self._desc = 'Enum HTTP.'
        self._name = 'NmapHttpEnum'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=http-apache-server-status,http-aspnet-debug,http-auth-finder,http-avaya-ipoffice-users,' + \
                    'http-backup-finder,http-barracuda-dir-traversal,http-cakephp-version,http-chrono,http-cisco-anyconnect,http-comments-displayer,' + \
                    'http-config-backup,http-cookie-flags,http-date,http-devframework,http-drupal-enum,http-enum,http-errors,http-exif-spider,' + \
                    'http-generator,http-git,http-gitweb-projects-enum,http-grep,http-headers,http-internal-ip-disclosure,http-malware-host,http-mcmp,' + \
                    'http-open-redirect,http-php-version,http-qnap-nas-info,http-referer-checker,http-robots.txt,http-sitemap-generator,http-svn-enum,' + \
                    'http-svn-info,http-trane-info,http-virustotal,http-waf-detect,http-waf-fingerprint,http-wordpress-enum,http-wordpress-users,' + \
                    'http-xssed ' + \
                    '${target} -oX ${working_dir}/http_enum_report.out'
        self._example = self._cmd
        self._port = '80,8080,443'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapHttpExploit(NmapBase):
    def __init__(self):
        self._desc = 'Runs exploit scripts for the HTTP server.'
        self._name = 'NmapHttpExploit'
        self._category = ToolCategory.Exploit
        self._cmd = 'nmap -p ${port} -sV --script=http-adobe-coldfusion-apsa1301,http-awstatstotals-exec,http-axis2-dir-traversal,http-dlink-backdoor,' + \
                    'http-drupal-enum-users,formpaths,http-phpmyadmin-dir-traversal,http-tplink-dir-traversal,http-traceroute,http-vuln-cve2006-3392,' + \
                    'http-vuln-cve2009-3960,http-vuln-cve2010-2861,http-vuln-cve2014-3704,http-vuln-cve2014-8877,http-vuln-cve2015-1427' + \
                    '${target} -oX ${working_dir}/http_exploit_report.out'
        self._example = self._cmd
        self._port = '80,8080,443'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapHttpVul(NmapBase):
    def __init__(self):
        self._desc = 'Vulnerability scripts for the HTTP server.'
        self._name = 'NmapHttpVul'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} --script=http-bigip-cookie,http-brute,http-cross-domain-policy,http-csrf,http-default-accounts,http-dombased-xss,' + \
                    'http-form-brute,http-form-fuzzer,http-frontpage-login,http-huawei-hg5xx-vuln,http-iis-short-name-brute,http-iis-webdav-vuln,http-joomla-brute,' + \
                    'http-jsonp-detection,http-litespeed-sourcecode-download,http-majordomo2-dir-traversal,http-method-tamper,http-passwd,http-phpself-xss,' + \
                    'http-proxy-brute,http-rfi-spider,http-security-headers,http-shellshock,http-sql-injection,http-stored-xss,http-unsafe-output-escaping,' + \
                    'http-vuln-cve2010-0738,http-vuln-cve2011-3368,http-vuln-cve2012-1823,http-vuln-cve2013-0156,http-vuln-cve2013-6786,http-vuln-cve2013-7091,' + \
                    'http-vuln-cve2014-2126,http-vuln-cve2014-2127,http-vuln-cve2014-2128,http-vuln-cve2014-2129,http-vuln-cve2015-1635,http-vuln-cve2017-1001000,' + \
                    'http-vuln-cve2017-5638,http-vuln-cve2017-5689,http-vuln-cve2017-8917,http-vuln-misfortune-cookie,http-vuln-wnr1000-creds,http-webdav-scan,' + \
                    'http-wordpress-brute ' + \
                    '${target} -oX ${working_dir}/http_vul_report.out'
        self._example = self._cmd
        self._port = '80,8080,443'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapVlcStreamer(NmapBase):
    def __init__(self):
        self._desc = 'Connects to a VLC Streamer helper service and lists directory contents. The VLC Streamer helper service is used by the iOS VLC Streamer application to\r\n' + \
                     'enable streaming of multimedia content from the remote server to the device.'
        self._name = 'NmapVlcStreamer'
        self._category = ToolCategory.Enumeration
        self._cmd = 'nmap -p ${port} --script=http-vlcstreamer-ls ${target} -oX ${working_dir}/vlc_report.out'
        self._example = self._cmd
        self._port = '54340'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapVmware(NmapBase):
    def __init__(self):
        self._desc = 'Checks for a path-traversal vulnerability in VMWare ESX, ESXi, and Server (CVE-2009-3733).'
        self._name = 'NmapVmware'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} --script=http-vmware-path-vuln ${target} -oX ${working_dir}/vmware_report.out'
        self._example = self._cmd
        self._port = '80,443,8222,8333'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        super().run()
        return

class NmapMsSqlBrute(NmapBase):
    def __init__(self):
        self._desc = 'MS SQL stuff.'
        self._name = 'NmapMsSqlBrute'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'nmap -p ${port} --script=ms-sql-brute --script-args mssql.instance-all,userdb=${arg1},passdb=${arg2} ${target} -oX ${working_dir}/mssql_report.out'
        self._example = self._cmd
        self._port = '1433'
        self._args = ''
        self._parserName = ''
        return super().__init__()

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Enter port (1433): ', end = '')
        port = input()
        if port == None or port == '':
            self._port = '1433'
        else:
            self._port = port

        print('Enter username list: ', end = '')
        users = input()

        print('Enter password list: ', end = '')
        passwords = input()

        self._cmd = self._cmd.replace('${arg1}', users)
        self._cmd = self._cmd.replace('${arg2}', passwords)

        super().run()
        return

