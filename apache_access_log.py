#!/usr/bin/env python
''' Generate Apache Access Logs and send them indefinitely to Logentries'''
import random
import socket
import time
import datetime

# Input your Logentries tokens below.   For just one token use ['token1']
WEBTOKENS = ['token1', 'token2']

def apache_access(tokens):
    ''' Define the log content to generate from '''
    webMessage = [
	   '{ "time":"[TIMESTAMP +0000]", "remoteIP":"REMOTEIP", "host":"Server 1", "request":"REQUEST", "query":"", "method":"GET", "status":"STATUS", "duration":"DURATION", "bytes":"BYTES", "userAgent":"USERAGENT", "referer":"-" }',
	   '{ "time":"[TIMESTAMP +0000]", "remoteIP":"REMOTEIP", "host":"Server 2", "request":"REQUEST", "query":"", "method":"GET", "status":"STATUS", "duration":"DURATION", "bytes":"BYTES", "userAgent":"USERAGENT", "referer":"-" }',
	   '{ "time":"[TIMESTAMP +0000]", "remoteIP":"REMOTEIP", "host":"Server 3", "request":"REQUEST", "query":"", "method":"GET", "status":"STATUS", "duration":"DURATION", "bytes":"BYTES", "userAgent":"USERAGENT", "referer":"-" }',
	   '{ "time":"[TIMESTAMP +0000]", "remoteIP":"REMOTEIP", "host":"Server 4", "request":"REQUEST", "query":"", "method":"GET", "status":"STATUS", "duration":"DURATION", "bytes":"BYTES", "userAgent":"USERAGENT", "referer":"-" }'
    ]

    requestList = [
	   '/account',
	   '/home',
	   '/docs',
	   '/account',
	   '/order'
    ]

    userAgent = [
	   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
	   'Mozilla/5.0 (Windows NT 7.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
	   'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'
    ]

    ipOctet1 = ['127', '212']
    ipOctet2 = ['66', '18']
    ipOctet3 = ['87', '244']
    ipOctet4 = ['47', '192']


    def send_messages():
        ''' Generate log events and send to Logentries '''
        w1 = str(random.choice(webMessage))

        randomIP = "%s.%s.%s.%s" % (random.choice(ipOctet1), random.choice(ipOctet2), 
                                    random.choice(ipOctet3), random.choice(ipOctet4))
        randomStatus = random.randrange(100)
        randomUserAgent = str(random.choice(userAgent))
        timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        randomRequest = str(random.choice(requestList))
        randomDuration = random.randrange(100, 4000, 1)
        randomBytes = random.randrange(300, 2000, 1)

        n_w1 = w1

        if "REMOTEIP" in w1:
            n_w1 = n_w1.replace("REMOTEIP", randomIP)
        if "REQUEST" in w1:
            n_w1 = n_w1.replace("REQUEST", randomRequest)
        if "Server 1" in w1  or "Server 2" in w1 or "Server 3" in w1:
            if 0 <= randomStatus <= 87:
                n_w1 = n_w1.replace("STATUS", str(200))
            if randomStatus == 88:
                n_w1 = n_w1.replace("STATUS", str(301))
            if 89 <= randomStatus <= 91:
                n_w1 = n_w1.replace("STATUS", str(403))
            if 92 <= randomStatus <= 96:
                n_w1 = n_w1.replace("STATUS", str(404))
            if 97 <= randomStatus <= 98:
                n_w1 = n_w1.replace("STATUS", str(500))
            if randomStatus == 99:
                n_w1 = n_w1.replace("STATUS", str(502))
        if "Server 4" in w1:
            if 0 <= randomStatus <= 80:
                n_w1 = n_w1.replace("STATUS", str(200))
            if randomStatus == 81:
                n_w1 = n_w1.replace("STATUS", str(301))
            if 82 <= randomStatus <= 84:
                n_w1 = n_w1.replace("STATUS", str(403))
            if 85 <= randomStatus <= 89:
                n_w1 = n_w1.replace("STATUS", str(404))
            if 90 <= randomStatus <= 98:
                n_w1 = n_w1.replace("STATUS", str(500))
            if randomStatus == 99:
                n_w1 = n_w1.replace("STATUS", str(502))
        if "USERAGENT" in w1:
            n_w1 = n_w1.replace("USERAGENT", randomUserAgent)
        if "TIMESTAMP" in w1:
            n_w1 = n_w1.replace("TIMESTAMP", timeStamp)
        if "BYTES" in w1:
            n_w1 = n_w1.replace("BYTES", str(randomBytes))
        if "DURATION" in w1:
            n_w1 = n_w1.replace("DURATION", str(randomDuration))

        print n_w1
        HOST = 'api.logentries.com'
        PORT = 10000

        for token in tokens:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT)) 

            s.sendall('%s %s\n' % (token, n_w1))
            s.close()
    send_messages()


def main():
    ''' Run indefinitely '''
    while True:
        this_time = random.randint(5, 10)
        print this_time
        time.sleep(this_time)
        apache_access(WEBTOKENS)


if __name__ == "__main__":
    main()
