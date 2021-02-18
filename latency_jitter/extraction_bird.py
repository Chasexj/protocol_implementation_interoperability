import re 
import json
import argparse
import os
import socket
import struct
import fileinput
from collections import defaultdict

Hello = "Hello"
DD = "Database Description"
LSR = "Link State Request"
LSU = "Link State Update"
LSA = "Link State Acknowledgment"
def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

def triangle(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.210.10.0.2":"10.10.0.3","10.10.0.210.10.0.18":"10.10.0.11","10.10.0.310.10.0.3":"10.10.0.2","10.10.0.310.10.0.10":"10.10.0.11","10.10.0.1110.10.0.11":"10.10.0.3","10.10.0.1110.10.0.19":"10.10.0.2"}
    #r1 = 172.17.0.2
    r1 = []
    #r2 = 172.17.0.3
    r2 = []
    #r3 = 172.17.0.4
    r3 = []
    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Time Stamp" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Time Stamp")
                time = line
            elif "Source: 10" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Source: ")
                inter = line
            elif "Message Type" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Message Type: ")
                message = line
            elif "Source OSPF Router" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Source OSPF Router: ")
                src_router = line
                recv_key = src_router+inter
                des_router = recv[recv_key]
                if src_router == "10.10.0.2":
                    r1.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.3":
                    r2.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.11":
                    r3.append(message+"Send at "+time + " to " + des_router )
                
                if des_router == "10.10.0.2":
                    r1.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.3":
                    r2.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.11":
                    r3.append(message+"Receive at "+time + " from " +src_router)\

    r1_send_if_recv =defaultdict(set)
    r1_recv_if_send =defaultdict(set)
    r2_send_if_recv =defaultdict(set)
    r2_recv_if_send =defaultdict(set)
    r3_send_if_recv =defaultdict(set)
    r3_recv_if_send =defaultdict(set)

    r1_send = []
    r1_receive = []
    for item in reversed(r1):
        if 'Send' in item:
            r1_send.append(item)
        else:
            r1_receive.append(item)
    for send_item in r1_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r1_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r1_receive.remove(recv_item)
                if send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r1_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break


#########################################################################################################################################

    r2_send = []
    r2_receive = []
    for item in reversed(r2):
        if 'Send' in item:
            r2_send.append(item)
        else:
            r2_receive.append(item)
            
    for send_item in r2_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r2_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r2_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r2_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break

#############################################################################################################################

    r3_send = []
    r3_receive = []
    for item in reversed(r3):
        if 'Send' in item:
            r3_send.append(item)
        else:
            r3_receive.append(item)

    for send_item in r3_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r3_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r3_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r3_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break
    result = [r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv]
    return result

def double(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.210.10.0.2":"10.10.0.3","10.10.0.310.10.0.3":"10.10.0.2"}
    #r1 = 172.17.0.2
    r1 = []
    #r2 = 172.17.0.3
    r2 = []

    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Time Stamp" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Time Stamp")
                time = line
            elif "Source: 10" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Source: ")
                inter = line
            elif "Message Type" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Message Type: ")
                message = line
            elif "Source OSPF Router" in line:
                line = line.strip("\n")
                line = line.strip('\t')
                line = line.strip("Source OSPF Router: ")
                src_router = line
                recv_key = src_router+inter
                des_router = recv[recv_key]
                if src_router == "10.10.0.2":
                    r1.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.3":
                    r2.append(message+"Send at "+time + " to " + des_router)
                
                if des_router == "10.10.0.2":
                    r1.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.3":
                    r2.append(message+"Receive at "+time + " from " +src_router)
    r1_send_if_recv =defaultdict(set)
    r1_recv_if_send =defaultdict(set)
    r2_send_if_recv =defaultdict(set)
    r2_recv_if_send =defaultdict(set)

    r1_send = []
    r1_receive = []
    for item in reversed(r1):
        if 'Send' in item:
            r1_send.append(item)
        else:
            r1_receive.append(item)

    for send_item in r1_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r1_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r1_receive.remove(recv_item)
                if send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r1_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break


#########################################################################################################################################

    r2_send = []
    r2_receive = []
    for item in reversed(r2):
        if 'Send' in item:
            r2_send.append(item)
        else:
            r2_receive.append(item)

    for send_item in r2_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r2_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r2_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r2_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break

    result = [r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv]
    return result

def star(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.310.10.0.3":"10.10.0.2",
    "10.10.0.1110.10.0.11":"10.10.0.2",
    "10.10.0.1910.10.0.19":"10.10.0.2",
    "10.10.0.210.10.0.2":"10.10.0.3",
    "10.10.0.210.10.0.10":"10.10.0.11",
    "10.10.0.210.10.0.18":"10.10.0.19"}
    #r1 = 172.17.0.2
    r1 = []
    #r2 = 172.17.0.3
    r2 = []
    #r3 = 172.17.0.4
    r3 = []
    r4 = []
    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Time Stamp" in line:
                line = line.strip("Time Stamp")
                line = line.strip("\n")
                time = line
            elif "Source: 10" in line:
                line = line.strip("Source: ")
                line = line.strip("\n")
                inter = line
            elif "Message Type" in line:
                line = line.strip("Message Type: ")
                line = line.strip("\n")
                message = line
            elif "Source OSPF Router" in line:
                line = line.strip("Source OSPF Router: ")
                line = line.strip("\n")
                src_router = line
                recv_key = src_router+inter
                des_router = recv[recv_key]
                if src_router == "10.10.0.2":
                    r1.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.3":
                    r2.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.11":
                    r3.append(message+"Send at "+time + " to " + des_router )
                elif src_router == "10.10.0.19":
                    r4.append(message+"Send at "+time + " to " + des_router )
                
                if des_router == "10.10.0.2":
                    r1.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.3":
                    r2.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.11":
                    r3.append(message+"Receive at "+time + " from " +src_router)
                elif src_router == "10.10.0.19":
                    r4.append(message+"Send at "+time + " to " + des_router )

    r1_send_if_recv =defaultdict(set)
    r1_recv_if_send =defaultdict(set)
    r2_send_if_recv =defaultdict(set)
    r2_recv_if_send =defaultdict(set)
    r3_send_if_recv =defaultdict(set)
    r3_recv_if_send =defaultdict(set)
    r4_send_if_recv =defaultdict(set)
    r4_recv_if_send =defaultdict(set)

    r1_send = []
    r1_receive = []
    for item in reversed(r1):
        if 'Send' in item:
            r1_send.append(item)
        else:
            r1_receive.append(item)
    for send_item in r1_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r1_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r1_receive.remove(recv_item)
                if send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.19":
                    r4_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r1_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break


#########################################################################################################################################

    r2_send = []
    r2_receive = []
    for item in reversed(r2):
        if 'Send' in item:
            r2_send.append(item)
        else:
            r2_receive.append(item)
            
    for send_item in r2_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r2_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r2_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.19":
                    r4_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r2_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break

#############################################################################################################################

    r3_send = []
    r3_receive = []
    for item in reversed(r3):
        if 'Send' in item:
            r3_send.append(item)
        else:
            r3_receive.append(item)

    for send_item in r3_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r3_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r3_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.19":
                    r4_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r3_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break
#############################################################################################################################

    r4_send = []
    r4_receive = []
    for item in reversed(r3):
        if 'Send' in item:
            r4_send.append(item)
        else:
            r4_receive.append(item)

    for send_item in r4_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r4_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r4_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r4_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break
    result = [r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv, r4_recv_if_send, r4_send_if_recv]
    return result

def linear(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.310.10.0.3":"10.10.0.2",
    "10.10.0.210.10.0.2":"10.10.0.3",
    "10.10.0.1110.10.0.11":"10.10.0.3",
    "10.10.0.310.10.0.10":"10.10.0.11",
    "10.10.0.1910.10.0.19":"10.10.0.11",
    "10.10.0.1110.10.0.18":"10.10.0.19"}
    #r1 = 172.17.0.2
    r1 = []
    #r2 = 172.17.0.3
    r2 = []
    #r3 = 172.17.0.4
    r3 = []
    r4 = []
    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Time Stamp" in line:
                line = line.strip("Time Stamp")
                line = line.strip("\n")
                time = line
            elif "Source: 10" in line:
                line = line.strip("Source: ")
                line = line.strip("\n")
                inter = line
            elif "Message Type" in line:
                line = line.strip("Message Type: ")
                line = line.strip("\n")
                message = line
            elif "Source OSPF Router" in line:
                line = line.strip("Source OSPF Router: ")
                line = line.strip("\n")
                src_router = line
                recv_key = src_router+inter
                des_router = recv[recv_key]
                if src_router == "10.10.0.2":
                    r1.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.3":
                    r2.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "10.10.0.11":
                    r3.append(message+"Send at "+time + " to " + des_router )
                elif src_router == "10.10.0.19":
                    r4.append(message+"Send at "+time + " to " + des_router )
                
                if des_router == "10.10.0.2":
                    r1.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.3":
                    r2.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "10.10.0.11":
                    r3.append(message+"Receive at "+time + " from " +src_router)
                elif src_router == "10.10.0.19":
                    r4.append(message+"Send at "+time + " to " + des_router )

    r1_send_if_recv =defaultdict(set)
    r1_recv_if_send =defaultdict(set)
    r2_send_if_recv =defaultdict(set)
    r2_recv_if_send =defaultdict(set)
    r3_send_if_recv =defaultdict(set)
    r3_recv_if_send =defaultdict(set)
    r4_send_if_recv =defaultdict(set)
    r4_recv_if_send =defaultdict(set)

    r1_send = []
    r1_receive = []
    for item in reversed(r1):
        if 'Send' in item:
            r1_send.append(item)
        else:
            r1_receive.append(item)
    for send_item in r1_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r1_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r1_receive.remove(recv_item)
                if send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.19":
                    r4_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r1_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break


#########################################################################################################################################

    r2_send = []
    r2_receive = []
    for item in reversed(r2):
        if 'Send' in item:
            r2_send.append(item)
        else:
            r2_receive.append(item)
            
    for send_item in r2_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r2_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r2_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.19":
                    r4_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r2_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break

#############################################################################################################################

    r3_send = []
    r3_receive = []
    for item in reversed(r3):
        if 'Send' in item:
            r3_send.append(item)
        else:
            r3_receive.append(item)

    for send_item in r3_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r3_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r3_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.19":
                    r4_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r3_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break
#############################################################################################################################

    r4_send = []
    r4_receive = []
    for item in reversed(r3):
        if 'Send' in item:
            r4_send.append(item)
        else:
            r4_receive.append(item)

    for send_item in r4_send:
        send_result = re.search('Send at (.*) to ', send_item)
        send_time = float(send_result.group(1))
        send_to_result = re.search('to (.*)', send_item)
        send_to = str(send_to_result.group(1))
        for recv_item in r4_receive:
            recv_result = re.search('Receive at (.*) from ', recv_item)
            recv_time = float(recv_result.group(1))
            recv_from_result = re.search('from (.*)', recv_item)
            recv_from = str(recv_from_result.group(1))
            if (recv_time - send_time)>6 and send_to == recv_from:
                send_packet = re.search('(.*)Send at', send_item)
                recv_packet = re.search('(.*)Receive at', recv_item)
                r4_receive.remove(recv_item)
                if send_to == "10.10.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "10.10.0.11":
                    r3_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r4_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break
    result = [r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv, r4_recv_if_send, r4_send_if_recv]
    return result

def run(final_result):
    send_dict = defaultdict(set)
    recv_dict = defaultdict(set)

    for i in range(len(final_result)):
        for j in range(len(final_result[i])):
            if j % 2 == 0:
                r_recv_if_send = final_result[i][j]
                r_send_if_recv = final_result[i][j+1]
                for item in r_recv_if_send:
                    for item2 in r_recv_if_send[item]:
                        recv_dict[item].add(item2)
                for item in r_send_if_recv:
                    for item2 in r_send_if_recv[item]:
                        send_dict[item].add(item2)

    print("List of packets can be received given last sent packet type")
    for key in recv_dict:
        print(key)
        print(recv_dict[key])
        print("\n")
    print("-------------------------------------------------------------------")
    print("List of packets can be send given last received packet type")
    for key in send_dict:
        print(key)
        print(send_dict[key])
        print("\n")


def main():
    final_result = []
    files3 = ['lb800_1_3.txt','lb800_2_3.txt','lb800_3_3.txt','lb800_4_3.txt']

    for input_file3 in files3:
        final_result.append(triangle(input_file3))

    files2 = ['lb1000_2_2.txt','lb1000_1_2.txt']
    for input_file2 in files2:
        final_result.append(double(input_file2))

    final_result.append(star('bstar_1000.txt'))
    final_result.append(linear('blinear_1000.txt'))

    run(final_result)
main()

#DB Description (2)
#LS Update (4)
#LS Request (3)
#LS Acknowledge (5)
#Hello Packet (1)
