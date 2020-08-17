#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paramiko
import re;
import time;
import os;
import sqlite3;

ip, port = "10.240.61.150", 22;
login = "admin";
passwd = "xxx";

client = paramiko.SSHClient();
client.load_system_host_keys();
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()); #wyjątki w klucuz

client.connect(ip, port, login, passwd);

while True:
	time.sleep(3); #wykonuj co sekunde
	cmd = "interface monitor-traffic ether1 once"; #command jaki ma być wysłany do mikrotika

	stdin, stdout, stderr = client.exec_command(cmd); #wyzbieraj dane
	
	lines = stdout.readlines(); #umieść w List<>
	
	
	varRx = str(lines[2].replace(' ','').replace('rx-bits-per-second:','').replace('\n', '').replace('\r', '')).rstrip('kbps').rstrip('Mbps').rstrip('...') # konkretna linijka Rx
	varTx = str(lines[8].replace(' ','').replace('tx-bits-per-second:','').replace('\n', '').replace('\r', '')).rstrip('kbps').rstrip('Mbps').rstrip('...') # konkretna linijka Tx

		
	os.system('cls'); #wymaż terminal (dla przejżystości :V)
	
	if(not "Mbps" in str(lines[2])):
		varRx = float(varRx)/1000; #przekonwertuj na Mb/s
		varRx = round(varRx,2); #zaokrąglij do dwóch miejsc po przecinku
		
	if(not "Mbps" in str(lines[8])):
		varTx = float(varTx)/1000; #przekonwertuj na Mb/s
		varTx = round(varTx,2); #zaokrąglij do dwóch miejsc po przecinku
		
	print("Upload: " + str(varRx) + "Mb/s") #usuń spacje i rx-bits-per-second:
	print("Download: " + str(varTx) + "Mb/s") #usuń spacje i rx-bits-per-second:
	
	
client.close();