#!/usr/bin/env python
#-*- coding: utf8 -*-

from os.path import isfile

def main():
	if isfile('/var/run/reboot-required'):
		print 'System reboot required'
		exit(1)
	else:
		print 'System not required in reboot'
		exit(0)

if __name__ == '__main__':
	main()

