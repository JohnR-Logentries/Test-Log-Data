#!/usr/bin/env python
import random
import socket
import time
import sys
import datetime

webToken1 = '<INSERT-LOG-TOKEN>'


webMessage = [
'{"time": "TIMESTAMP", "requestID": "1122345", "hostname": "Server2", "containerID": "10", "request": "/home", "query": "searchterm1", "method": "GET", "status": "200", "userAgent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201", "referer": "-", "response_time": "100"}',
'{"time": "TIMESTAMP", "requestID": "1122345", "hostname": "Server2", "containerID": "12", "request": "/home", "DBlookup": "custom", "response_time": "13"}',
'{"time": "TIMESTAMP", "requestID": "1122345", "hostname": "Server2", "containerID": "12", "request": "/home", "DBlookup": "SQL", "response_time": "13"}',
'{"time": "TIMESTAMP", "requestID": "1122345", "hostname": "Server2", "containerID": "13", "request": "/home", "response_time": "1"}',
'{"time": "TIMESTAMP", "requestID": "1122346", "hostname": "Server2", "containerID": "10", "request": "/jump/app1", "query": "searchterm1", "method": "GET", "status": "200", "userAgent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201", "referer": "-", "response_time": "110"}',
'{"time": "TIMESTAMP", "requestID": "1122346", "hostname": "Server2", "containerID": "12", "request": "/jump/app1", "DBlookup": "custom", "response_time": "50"}',
'{"time": "TIMESTAMP", "requestID": "1122346", "hostname": "Server2", "containerID": "12", "request": "/jump/app1", "DBlookup": "SQL", "response_time": "50"}',
'{"time": "TIMESTAMP", "requestID": "1122346", "hostname": "Server2", "containerID": "14", "request": "/jump/app1", "response_time": "1"}',
'{"time": "TIMESTAMP", "requestID": "1122347", "hostname": "Server2", "containerID": "10", "request": "login", "method": "GET", "status": "200", "userAgent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201", "referer": "-", "response_time": "165"}',
]


def send_messages(passedNum):
  		
    w1 = str(webMessage[passedNum])

    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    n_w1 = w1

    if "TIMESTAMP" in w1:
        n_w1 = n_w1.replace("TIMESTAMP", timeStamp)

    HOST = 'api.logentries.com'
    PORT = 10000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

#    if webMessage.index(w1) > 10:
    s.sendall('%s %s\n' % (webToken1, n_w1))
#   elif webMessage.index(w1) > 5:
#       s.sendall('%s %s\n' % (webToken1, n_w1))
#   else:
#       s.sendall('%s %s\n' % (webToken1, n_w1))


    s.close()


def main():
	while True:
		this_time = random.randint(1, 2)
		time.sleep(this_time)
		send_messages(0)
		time.sleep(this_time)
		send_messages(1)
		time.sleep(this_time)
		send_messages(2)
		time.sleep(this_time)
		send_messages(3)
		time.sleep(this_time)
		send_messages(4)
		time.sleep(this_time)
		send_messages(5)
		time.sleep(this_time)
		send_messages(6)
		time.sleep(this_time)
		send_messages(7)
		time.sleep(this_time)
		print this_time
	    
if __name__ == "__main__":
    main()

