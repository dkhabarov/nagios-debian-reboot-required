#!/usr/bin/env python
#-*- coding: utf8 -*-


default_snmp_oid = ".1.3.6.1.4.1.2021.7894.1"
default_snmp_community = "publicSRV"
default_snmp_version = 2
default_snmp_port = 161
default_snmp_timeout = 1000000 # micro-seconds before retry
status = {'OK' : 0 , 'WARNING' : 1, 'CRITICAL' : 2 , 'UNKNOWN' : 3}

import argparse
import sys
try:
    import netsnmp
except ImportError:
	print "netsnmp module is missing! Try install it:"
	print "If you use Debian/Ubuntu - run: \"apt-get install libsnmp-python\""
	print "If you use Gentoo - run: \"USE=\"python\" emerge net-analyzer/net-snmp\""
	print "If you use CentOS - run \"yum -y install net-snmp-python\""
	exit(status["UNKNOWN"])


cliparser = argparse.ArgumentParser()
cliparser.add_argument('-H', '--host', metavar='ADDR', dest='serveraddr', help='domain name or ip address', required=True, type=str)
cliparser.add_argument('-p', '--port', metavar='PORT', dest='serverport', help='Port', default=default_snmp_port, type=int)
cliparser.add_argument('--timeout', metavar='VALUE', dest='snmptimeout', help='snmp timeout in microseconds', default=default_snmp_timeout, type=int)
cliparser.add_argument('--oid', metavar='VALUE', dest='snmpoid', help='SNMP OID', default=default_snmp_oid, type=str)
cliparser.add_argument('-C', '--community', metavar='VALUE', dest='snmpcommunity', default=default_snmp_community, type=str)
cliargs = cliparser.parse_args()

def main():
	state = status['UNKNOWN']
	try:
		res = netsnmp.snmpwalk(cliargs.snmpoid,
				Version = default_snmp_version,
				DestHost = cliargs.serveraddr, 
				Community = cliargs.snmpcommunity,
				RemotePort = cliargs.serverport,
				Timeout = cliargs.snmptimeout,
				)
		if len(res) == 0:
			info = 'Could not get data from host'
			state - status['UNKNOWN']
		else:
			info = res[len(res)-1]
			state = res[len(res)-2]
	except Exception as e:
		info = str(e)
	print(info)
	if type(state) != int:
		sys.exit(int(state))
	else:
		sys.exit(status['UNKNOWN'])
if __name__ == "__main__":
	main()

