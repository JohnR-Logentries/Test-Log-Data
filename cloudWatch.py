#!/usr/bin/python
''' Generate CloudWatch Logs and send them indefinitely to Logentries '''
import random
import socket
import time
import datetime
import json
from collections import OrderedDict

# Input your Logentries tokens below.   For just one token use ['token1']
WEBTOKENS = ['token1', 'token2']

def cloud_watch(tokens):
    ''' CloudWatch '''
    def instance_metric(times2run):
        ''' Generate and send instance metrics data '''

        SysMetric = ["NetworkIn", "StatusCheckFailed", "StatusCheckFailed_System",
                     "StatusCheckFailed_Instance", "ReplicaLag", "ReadThroughput",
                     "BinLogDiskUsage", "FreeableMemory", "WriteThroughput",
                     "DatabaseConnections", "FreeStorageSpace", "SwapUsage",
                     "ReadIOPS", "WriteIOPS", "ReplicaLag", "CPUUtilization",
                     "WriteLatency", "DiskWriteOps", "ReadLatency"] #20
        VolMetric = ["VolumeIdleTime", "VolumeReadOps", "VolumeTotalReadTime",
                     "VolumeThroughputPercentage", "VolumeConsumedReadWriteOps",
                     "VolumeWriteBytes", "VolumeQueueLength", "VolumeReadBytes",
                     "VolumeTotalWriteTime", "DiskQueueDepth", "DiskReadOps"] #10
        VolTars = ["vol-34b8c01d", "vol-41fe82a6", "vol-e82911b2", "vol-994ac88d"]
        Inst = ["i-bff14a12", "i-15c7e62a", "i-d91a5de2", "i-f51c7a2e"]
        for i in xrange(0, times2run):
            avg = 0;rr = 1;a = 0;a_max = 0;a_sum = 0;a_min = 0;z = 0
            now = str(datetime.datetime.now().strftime("%Y-%m-%f %H:%M:%S"))
			## randecord will generate random floats for the metrics
            a = float(random.randrange(29))
            if a >= 19:
                msg = str(random.choice(VolMetric))
                randtar = str(random.choice(VolTars))
            else:
                msg = str(random.choice(SysMetric))
                randtar = str(random.choice(Inst))
            if msg == "FreeableMemory":
                if randtar == "i-bff14a12":	#small
                    a_min = float(random.randrange(100000004, 150000000, 1)) #100 to 150MB
                    a_max = a_min
                    a_sum = a_min
                    avg = (a_min+a_max)/2
					#print(a_min) #test
					#print("from FreeableMemory")
                if randtar == "i-d91a5de2":	#micro
                    a_min = float(random.randrange(100000000, 800000000, 1)) #100 to 800MB
                    a_max = a_min
                    a_sum = a_min
                    avg = (a_min+a_max)/2
					#print(a_min) #test
					#print("from FreeableMemory")
                if randtar == "i-15c7e62a":	#medium
                    a_min = float(random.randrange(2000000000, 3750000000, 1)) #2GB to 3.75GB
                    a_max = a_min
                    a_sum = a_min
                    avg = (a_min+a_max)/2
					#print(a_min) #test
					#print("from FreeableMemory")
                if randtar == "i-f51c7a2e":	#large
                    a_min = float(random.randrange(2500000000, 7200000000, 1)) #2.5GB to 7.2GB
                    a_max = a_min
                    a_sum = a_min
                    avg = (a_min+a_max)/2
					#print(a_min) #test
					#print("from FreeableMemory")
            if msg == "FreeStorageSpace":
                a_min = float(random.randrange(1000000000, 100000000000, 1)) #10GB to 100GB
                a_max = a_min
                a_sum = a_min
                avg = a_min
				#print(a_min) #test
				#print("from FreeStorageSpace")
            if msg == "CPUUtilization":
                if randtar == "i-bff14a12":
                    a_min = random.uniform(80, 95)
                    a_max = a_min
                    avg = a_min
                    a_sum = a_min+a_max
                else:
                    a_min = random.uniform(0, 20)
                    a_max = random.uniform(20, 50)
                    avg = (a_min+a_max)/2
				#print(a_min) #test
				#print("from CPUUtilization")
            if msg == "VolumeThroughputPercentage":
                a_min = random.uniform(0, 50)
                a_max = a_min
                avg = a_min
                a_sum = a_min
            if msg in ["NetworkIn", "NetworkOut"]:
                a_min = float(random.randrange(5000, 10000, 1))
                a_max = float(random.randrange(100000, 9000000, 1))
                avg = (a_min+a_max)/2
				#print(a_min) #test
				#print("from NetworkIn") #test
            if msg in ["DiskWriteOps", "DiskReadBytes", "DiskReadOps", "DiskQueueLength",
                       "ReadIOPS", "WriteIOPS", "ReadLatency", "WriteLatency",
                       "DiskQueueDepth", "VolumeQueueLength"]:
                a_min = float(random.random())
                a_max = a_min
                avg = (a_min+a_max)/2
                a_sum = a_min
				#print(a_min) #test
				#print("from DiskOps")
            if msg in ["StatusCheckFailed", "StatusCheckFailed_Instance",
                       "StatusCheckFailed_System", "DatabaseConnections",
                       "SwapUsage"]:
                a_min = 0
                a_max = 0
                avg = 0
                a_sum = 0
				#print(a_min) #test
				#print("from StatusCheck")
            if msg in ["ReplicaLag", "WriteThroughput", "ReadThroughput", "BinLogDiskUsage",
                       "VolumeReadBytes", "VolumeWriteBytes", "VolumeIdleTime", "VolumeReadOps",
                       "VolumeWriteOps", "VolumeConsumedReadWriteOps"]:
                rr = 0;randrecord = ""
				#print(a_min) #test
				#print("from ReplicaLag")
            if msg in ["VolumeTotalReadTime", "VolumeTotalWriteTime"]:
                a_min = float(random.random())
                a_max = a_min
                avg = a_min
                a_sum = a_min
				#print(a_min) #test
				#print("from VolumeTotalReadTime")
            if avg == 0:
                avg1 = float((a_min+a_max)/2)
                avg = float((avg1+a_min+a_max)/2)
				#print("from avg" ) #test
            if rr == 1:
                randrecord = str('"minimum": "%f","maximum": "%f","average": "%f","sum": "%f","timestamp": "%s"'%(a_min, a_max, avg, a_sum, now))
                z = str(randrecord)
				#print("from rr")
            metric = '){"target": "%s","metric":"%s","records":[{%s}]}'%(randtar, msg, randrecord)
			#print(a_min) #test
			#print("msg is:"+msg)
			#type("the type of msg is:"+msg)
            print metric
            HOST = "data.logentries.com"
            PORT = 80
            for token in tokens:
            	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                s.sendall("%s %s\n" % (token, metric))
                s.close()
            msg = ""

    def instance_info():
        ''' Generate and send instnace logs '''
        #now = datetime.datetime.now().strftime("%Y-%m-%f %H:%M:%S")
        Instance1 = ('InstanceId', 'i-f51c7a2e'), ('ImageId', 'ami-47a23a30'), ('State', "{Code: 16, Name: running, }"), ('PrivateDnsName', 'ip-79-125-121-101.eu-west-1.compute.internal'), ('PublicDnsName', ' '), ('StateTransitionReason', ' '), ('Keyname', ' '), ('AmiLaunchIndex', '0'), ('ProductCodes', ' '), ('InstanceType', 't2.large'), ('LaunchTime', 'Tue Aug 25 23:10:19 UTC 2015'), ('Placement', "{AvailabilityZone: 'eu-west-1c', Groupname: ' ' , Tenancy: 'default'}"), ('Monitoring', "{State: disabled, }"), ('SubnetId', 'subnet-5bc67e12'), ('VpcId', 'vpc-1c4de291'), ('PrivateIpAddress', '79.125.121.101'), ('PublicIpAddress', '52.17.72.110'), ('Architecture', 'x86_64'), ('RootDeviceName', '/dev/sda1'), ('BlockDeviceMappings', "[{RootDeviceName: '/dev/sda1', Ebs: {VolumeId: 'vol-34b8c01d', Status: 'attached', AttachTime: 'Tue Aug 25 23:10:21 UTC 2015', DeleteOnTera_mination: 'true', }, }],"), ('VirtualizationType', 'hvm'), ('ClientToken', 'bBl239856349581749'), ('Tags', "[{Key: Name, Value: Ubuntu_Datahub, }],"), ('SecurityGroups', "[{Groupname: 'SSH + Datahub', GroupId: 'sg-a7b2fd29', }],"), ('SourceDestCheck', 'True'), ('Hypervisor', 'xen'), ('NetworkInterfaces', "[{NetworkInterfaceId: 'eni-141d9fc2', SubnetId: 'subnet-5bc67e12', VpcId: 'vpc-1c4de291', Description: 'Primary network interface', OwnerId: '956783256841', Status: 'in-use', PrivateIpAddress: '79.125.121.101', SourceDestCheck: 'true', Groups: [{GroupName: 'SSH Only', GroupId: 'sg-a7b2fd29'}]', Attachment: '{AttachmentId: 'eni-attach-89d71ef5', DeviceIndex: '0', Status: 'attached', AttachTime: 'Tue Aug 25 23:10:21 UTC 2015', DeleteOnTera_mination: 'true', }', Association: {PublicIp: '52.17.72.110', IpOwnerId: 'amazon', }, }]"), ('EbsOptimized', 'false')
        Instance2 = ('InstanceId', 'i-d91a5de2'), ('ImageId', 'ami-68347d1f'), ('State', "{Code: 16, Name: running, }"), ('PrivateDnsName', 'ip-79-125-121-105.eu-west-1.compute.internal'), ('PublicDnsName', ' '), ('StateTransitionReason', ' '), ('Keyname', ' '), ('AmiLaunchIndex', '0'), ('ProductCodes', ' '), ('InstanceType', 't2.micro'), ('LaunchTime', 'Thur Aug 20 23:15:42 UTC 2015'), ('Placement', "{AvailabilityZone: 'eu-west-1c', Groupname: ' ' , Tenancy: 'default'}"), ('Monitoring', '{State: disabled, }'), ('SubnetId', 'subnet-5bc67e12'), ('VpcId', 'vpc-1c4de291'), ('PrivateIpAddress', '79.125.121.105'), ('PublicIpAddress', ' '), ('Architecture', 'x86_64'), ('RootDeviceName', '/dev/sda1'), ('BlockDeviceMappings', "[{RootDevicename: '/dev/sda1', Ebs: {VolumeId: 'vol-41fe82a6', Status: 'attached', AttachTime: 'Thur Aug 20 23:15:42 UTC 2015', DeleteOnTera_mination: 'true', }, }]"), ('VirtualizationType', 'hvm'), ('ClientToken', 'aWP789253104506781'), ('Tags', "[{Key: 'Name', Value: 'Windows_IIS', }],"), ('SecurityGroups', "[{Groupname: 'RDP Only', GroupId: 'sg-s5911997', }],"), ('SourceDestCheck', 'True'), ('Hypervisor', 'xen'), ('NetworkInterfaces', "[{NetworkInterfaceId: 'eni-c7b145d9', SubnetId: 'subnet-5bc67e12', VpcId: 'vpc-1c4de291', Description: 'Primary network interface', OwnerId: '956783256841', Status: 'in-use', PrivateIpAddress: '79.125.121.105', SourceDestCheck: 'true', Groups: [{GroupName: 'RDP Only', GroupId: 'sg-b2ce32f1'}], Attachment: {AttachmentId: 'eni-attach-91a2e6gf', DeviceIndex: '0', Status: 'attached', AttachTime: 'Thur Aug 20 23:15:42 UTC 2015', DeleteOnTera_mination: 'true', }, Association: {PublicIp: ' ', IpOwnerId: 'amazon', }, }]"), ('EbsOptimized', 'false')
        Instance3 = ('InstanceId', 'i-15c7e62a'), ('ImageId', 'ami-9f62ffe8'), ('State', "{Code: 80, Name: stopped, }"), ('PrivateDnsName', 'ip-79-125-121-212.eu-west-1.compute.internal'), ('PublicDnsName', ' '), ('StateTransitionReason', ' '), ('Keyname', ' '), ('AmiLaunchIndex', '0'), ('ProductCodes', ' '), ('InstanceType', 't2.medium'), ('LaunchTime', 'Wed Aug 26 21:31:47 UTC 2015'), ('Placement', "{AvailabilityZone: 'eu-west-1c', Groupname: ' ' , Tenancy: 'default'}"), ('Monitoring', "{State: disabled, }"), ('SubnetId', 'subnet-5bc67e12'), ('VpcId', 'vpc-97cf3d2a'), ('PrivateIpAddress', '79.125.121.212'), ('PublicIpAddress', '52.17.20.138'), ('Architecture', 'x86_64'), ('RootDeviceName', '/dev/sda1'), ('BlockDeviceMappings', "[{RootDeviceName: '/dev/sda1', Ebs: {VolumeId: 'vol-e82911b2', Status: 'attached', AttachTime: 'Wed Aug 26 21:31:47 UTC 2015', DeleteOnTera_mination: 'true', }, }],"), ('VirtualizationType', 'hvm'), ('ClientToken', 'bBl239856349581749'), ('Tags', "[{Key: Name, Value: Ubuntu_Datahub, }],"), ('SecurityGroups', "[{Groupname: 'SSH + Datahub', GroupId: 'sg-a7b2fd29', }],"), ('SourceDestCheck', 'True'), ('Hypervisor', 'xen'), ('NetworkInterfaces', "[{NetworkInterfaceId: 'eni-141d9fc2', SubnetId: 'subnet-5bc67e12', VpcId: 'vpc-97cf3d2a', Description: 'Primary network interface', OwnerId: '956783256841', Status: 'in-use', PrivateIpAddress: '79.125.121.101', SourceDestCheck: 'true', Groups: [{GroupName: 'SSH Only', GroupId: 'sg-a7b2fd29'}]', Attachment: '{AttachmentId: 'eni-attach-45ce61a7', DeviceIndex: '0', Status: 'detached', AttachTime: 'Wed Aug 26 21:31:47 UTC 2015', DeleteOnTera_mination: 'true', }', Association: {PublicIp: '52.17.20.138', IpOwnerId: 'amazon', }, }]"), ('EbsOptimized', 'false')
        Instance4 = ('InstanceId', 'i-bff14a12'), ('ImageId', 'ami-47a23a30'), ('State', "{Code: 16, Name: running, }"), ('PrivateDnsName', 'ip-79-125-121-101.eu-west-1.compute.internal'), ('PublicDnsName', ' '), ('StateTransitionReason', ' '), ('Keyname', ' '), ('AmiLaunchIndex', '0'), ('ProductCodes', ' '), ('InstanceType', 't2.small'), ('LaunchTime', 'Tue Aug 25 23:10:19 UTC 2015'), ('Placement', "{AvailabilityZone: 'eu-west-1c', Groupname: ' ' , Tenancy: 'default'}"), ('Monitoring', "{State: disabled, }"), ('SubnetId', 'subnet-5bc67e12'), ('VpcId', 'vpc-1c4de291'), ('PrivateIpAddress', '79.125.121.101'), ('PublicIpAddress', '52.17.72.110'), ('Architecture', 'x86_64'), ('RootDeviceName', '/dev/sda1'), ('BlockDeviceMappings', "[{RootDeviceName: '/dev/sda1', Ebs: {VolumeId: 'vol-994ac88d', Status: 'attached', AttachTime: 'Tue Aug 25 23:10:21 UTC 2015', DeleteOnTera_mination: 'true', }, }],"), ('VirtualizationType', 'hvm'), ('ClientToken', 'bBl239856349581749'), ('Tags', "[{Key: Name, Value: Ubuntu_Datahub, }],"), ('SecurityGroups', "[{Groupname: 'SSH + Datahub', GroupId: 'sg-a7b2fd29', }],"), ('SourceDestCheck', 'True'), ('Hypervisor', 'xen'), ('NetworkInterfaces', "[{NetworkInterfaceId: 'eni-94b8f1cc', SubnetId: 'subnet-5bc67e12', VpcId: 'vpc-1c4de291', Description: 'Primary network interface', OwnerId: '956783256841', Status: 'in-use', PrivateIpAddress: '79.125.121.101', SourceDestCheck: 'true', Groups: [{GroupName: 'SSH Only', GroupId: 'sg-a7b2fd29'}]', Attachment: '{AttachmentId: 'eni-attach-89d71ef5', DeviceIndex: '0', Status: 'attached', AttachTime: 'Tue Aug 25 23:10:21 UTC 2015', DeleteOnTermination: 'true', }', Association: {PublicIp: '52.17.72.110', IpOwnerId: 'amazon', }, }]"), ('EbsOptimized', 'false')
        I1 = str(json.dumps(OrderedDict(Instance1)))
        I2 = str(json.dumps(OrderedDict(Instance2)))
        I3 = str(json.dumps(OrderedDict(Instance3)))
        I4 = str(json.dumps(OrderedDict(Instance4)))
        HOST = 'data.logentries.com'
        PORT = 80
        for token in tokens:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.sendall('%s %s\n %s %s\n %s %s\n %s %s\n' % (token, str(I1), token, str(I2), token, str(I3), token, str(I4)))
            s.close()

    time2run = random.randint(18, 25)
    instance_metric(time2run)
    instance_info()

def main():
    ''' Run indefinitely '''
    while True:
        this_time = random.randint(5, 10)
        time.sleep(this_time)
        cloud_watch(WEBTOKENS)

if __name__ == "__main__":
    main()
