#!/usr/bin/python
''' Generate Ubuntu Secure Logs and send them indefinitely to Logentries '''
import random
import socket
import time
import datetime

# Input your Logentries tokens below.   For just one token use ['token1']
WEBTOKENS = ['token1', 'token2']

def ubuntu_secure(tokens):
    ''' Ubuntu Secure '''
    #timestamp
    now = datetime.datetime.now().strftime("%b %d %H:%M:%S ")
    i = 0
    def message():
        ''' Generate and send Ubuntu Secure log data '''
        #list
        n = random.randrange(1000, 20000)
        sshd = "sshd[%d] "%n
        Stat = ['Received disconnect ', 'Invalid user ', 'Connection closed ',
                'Did not receive identification string ', 'Read from socket ',
                'Connection reset by peer ',
                'reverse mapping checking getaddrinfo for 61.30.65.218.broad.xy.jx.dynamic.163data.com.cn [218.65.30.61] failed - POSSIBLE BREAK-IN ATTEMPT! ']
        AuthSat = ['fatal', 'failed', 'input_userauth_request']
        User = ['admin', 'a', 'applmgr', 'amssys', 'ankur', 'openerp', 'jenkins', 'db2admin',
                'db2inst1', 'db2fenc1', 'rajesh', 'rajesh', 'hadoop', 'sanjay', 'redmine', 'odoo',
                'oracle', 'git', 'liu', 'lihui', 'ftpuser', 'webadmin', 'webuser', 'db2das1',
                'tomcat', 'vidya', 'minecraft', 'mysql', 'postgres', 'support', 'ubnt', 'pi']
        Status = str(random.choice(Stat))
        usr = str(random.choice(User))
        host = "ip-172-30-2-64 "
		#generate IP
        ip = str(random.randint(200, 300)) + "." + str(random.randint(200, 300)) + "." + str(random.randint(200, 300)) + "." + str(random.randint(200, 300))
        msg = "%sfrom " % Status
        if Status == 'Invalid user ':
            msg = Status + usr + " from "
            msg2 = msg + ip
        if Status == 'Read from socket':
            msg2 = 'fatal:Read from socket failed: Connection reset by peer [preauth]'
        msg2 = now + host + sshd + msg + ip
		#print(msg2)
        #send data
        HOST = 'api.logentries.com'
        PORT = 10000

        for token in tokens:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.sendall('%s %s\n' % (token, msg2))
            s.close()

        print msg2

    message()

# Delay before sending the next event
def main():
    ''' Run indefinitely '''
    while True:
        this_time = random.randint(3, 6)
		#print this_time
        ubuntu_secure(WEBTOKENS)
        time.sleep(this_time)

if __name__ == "__main__":
    main()
