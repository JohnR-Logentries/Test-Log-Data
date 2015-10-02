#!/usr/bin/python
''' Full AWS Environment Log Simulator '''
####################################################################################################
#                          **   Full AWS Environment Log Simulator   **                            #
#                                                                                                  #
#  By: The Logentries Customer Successs Team                                                       #
#                                                                                                  #
#  This simulator will create sample log events and forward those log events to the Logentries     #
#     token(s) specified.  Logs from the following services can be simulated:  AWS Cloud Watch,    #
#      Apache Access Logs, and Ubuntu Secure.                                                      #
#                                                                                                  #
#  The data produced from this simulator is intented to be used for demonstration purposes only.   #
####################################################################################################

import random
import time
import multiprocessing

from cloudWatch import cloud_watch
from apache_access_log import apache_access
from ubuntuSecure import ubuntu_secure


# Input your Logentries tokens below.   For just one token use ['token1']
TOKENS_CLOUD_WATCH = ['token1', 'token2']
TOKENS_APACHE_ACCESS = ['token1', 'token2']
TOKENS_UBUNTU_SECURE = ['token1', 'token2']


def main():
    ''' Load the desired modules '''

    # Cloud Watch
    proc_cloud_watch = multiprocessing.Process(target=mp_cloud_watch,
                                               args=(TOKENS_CLOUD_WATCH, 5, 10))
    proc_cloud_watch.start()

    # Apache Access
    proc_apache_access = multiprocessing.Process(target=mp_apache_access,
                                                 args=(TOKENS_APACHE_ACCESS, 5, 10))
    proc_apache_access.start()

    # Ubuntu Secure
    proc_ubuntu_secure = multiprocessing.Process(target=mp_ubuntu_secure,
                                                 args=(TOKENS_UBUNTU_SECURE, 5, 10))
    proc_ubuntu_secure.start()


def sleep(minsleep, maxsleep):
    ''' Sleep for some time between the min and max value '''
    this_time = random.randint(minsleep, maxsleep)
    time.sleep(this_time)

def mp_cloud_watch(tokens, minsleep, maxsleep):
    ''' Intended to be used with multiprocessing. Add sleep command before calling cloud_watch.
        Run it indefinitely                                                                     '''
    while True:
        sleep(minsleep, maxsleep)
        cloud_watch(tokens)

def mp_apache_access(tokens, minsleep, maxsleep):
    ''' Intended to be used with multiprocessing. Add sleep command before calling apache_access.
        Run it indefinitely                                                                      '''
    while True:
        sleep(minsleep, maxsleep)
        apache_access(tokens)

def mp_ubuntu_secure(tokens, minsleep, maxsleep):
    ''' Intended to be used with multiprocessing. Add sleep command before calling ubuntu_secure.
        Run it indefinitely                                                                      '''
    while True:
        sleep(minsleep, maxsleep)
        ubuntu_secure(tokens)

if __name__ == "__main__":
    main()
