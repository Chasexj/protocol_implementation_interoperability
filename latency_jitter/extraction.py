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

def trial_1(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"172.17.0.210.10.0.2":"172.17.0.3","172.17.0.210.10.0.18":"172.17.0.4","172.17.0.310.10.0.3":"172.17.0.2","172.17.0.310.10.0.10":"172.17.0.4","172.17.0.410.10.0.11":"172.17.0.3","172.17.0.410.10.0.19":"172.17.0.2"}
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
                if src_router == "172.17.0.2":
                    r1.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "172.17.0.3":
                    r2.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "172.17.0.4":
                    r3.append(message+"Send at "+time + " to " + des_router )
                
                if des_router == "172.17.0.2":
                    r1.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "172.17.0.3":
                    r2.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "172.17.0.4":
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
                if send_to == "172.17.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "172.17.0.4":
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
                if send_to == "172.17.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "172.17.0.4":
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
                if send_to == "172.17.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                elif send_to == "172.17.0.3":
                    r2_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r3_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break

    return r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv

def trial_2(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"172.17.0.210.10.0.2":"172.17.0.3","172.17.0.310.10.0.3":"172.17.0.2"}
    #r1 = 172.17.0.2
    r1 = []
    #r2 = 172.17.0.3
    r2 = []

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
                if src_router == "172.17.0.2":
                    r1.append(message+"Send at "+time + " to " + des_router)
                elif src_router == "172.17.0.3":
                    r2.append(message+"Send at "+time + " to " + des_router)
                
                if des_router == "172.17.0.2":
                    r1.append(message+"Receive at "+time + " from " +src_router)
                elif des_router == "172.17.0.3":
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
                if send_to == "172.17.0.3":
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
                if send_to == "172.17.0.2":
                    r1_send_if_recv[recv_packet.group(1)].add(send_packet.group(1))
                r2_recv_if_send[send_packet.group(1)].add(recv_packet.group(1))
                break


    return r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv

def run(r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv, r4_recv_if_send, r4_send_if_recv, r5_recv_if_send, r5_send_if_recv, r6_recv_if_send, r6_send_if_recv, r7_recv_if_send, r7_send_if_recv, r8_recv_if_send, r8_send_if_recv,r9_recv_if_send, r9_send_if_recv, r10_recv_if_send, r10_send_if_recv,r11_recv_if_send, r11_send_if_recv,r12_recv_if_send, r12_send_if_recv,r13_recv_if_send, r13_send_if_recv,r14_recv_if_send, r14_send_if_recv,r15_recv_if_send, r15_send_if_recv,r16_recv_if_send, r16_send_if_recv):
    send_dict = defaultdict(set)
    recv_dict = defaultdict(set)

    for i in range(16):
        if i ==0:
            r_recv_if_send = r1_recv_if_send
            r_send_if_recv = r1_send_if_recv
        elif i ==1:
            r_recv_if_send = r2_recv_if_send
            r_send_if_recv = r2_send_if_recv
        elif i ==2:
            r_recv_if_send = r3_recv_if_send
            r_send_if_recv = r3_send_if_recv
        elif i ==3:
            r_recv_if_send = r4_recv_if_send
            r_send_if_recv = r4_send_if_recv
        elif i ==4:
            r_recv_if_send = r5_recv_if_send
            r_send_if_recv = r5_send_if_recv
        elif i ==5:
            r_recv_if_send = r6_recv_if_send
            r_send_if_recv = r6_send_if_recv
        elif i ==6:
            r_recv_if_send = r7_recv_if_send
            r_send_if_recv = r7_send_if_recv
        elif i ==7:
            r_recv_if_send = r8_recv_if_send
            r_send_if_recv = r8_send_if_recv
        elif i ==8:
            r_recv_if_send = r9_recv_if_send
            r_send_if_recv = r9_send_if_recv
        elif i ==9:
            r_recv_if_send = r10_recv_if_send
            r_send_if_recv = r10_send_if_recv
        elif i ==10:
            r_recv_if_send = r11_recv_if_send
            r_send_if_recv = r11_send_if_recv
        elif i ==11:
            r_recv_if_send = r12_recv_if_send
            r_send_if_recv = r12_send_if_recv
        elif i ==12:
            r_recv_if_send = r13_recv_if_send
            r_send_if_recv = r13_send_if_recv
        elif i ==13:
            r_recv_if_send = r14_recv_if_send
            r_send_if_recv = r14_send_if_recv
        elif i ==14:
            r_recv_if_send = r15_recv_if_send
            r_send_if_recv = r15_send_if_recv
        elif i ==15:
            r_recv_if_send = r16_recv_if_send
            r_send_if_recv = r16_send_if_recv
        #print(type(r_recv_if_send))
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
    r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv = trial_1('l800_1_3.txt')
    r4_recv_if_send, r4_send_if_recv, r5_recv_if_send, r5_send_if_recv, r6_recv_if_send, r6_send_if_recv = trial_1('l800_2_3.txt')
    r7_recv_if_send, r7_send_if_recv, r8_recv_if_send, r8_send_if_recv = trial_2('l1000_1_2.txt')
    #
    r9_recv_if_send, r9_send_if_recv, r10_recv_if_send, r10_send_if_recv, r11_recv_if_send, r11_send_if_recv = trial_1('l800_3_3.txt')
    r12_recv_if_send, r12_send_if_recv, r13_recv_if_send, r13_send_if_recv, r14_recv_if_send, r14_send_if_recv = trial_1('l800_3_3.txt')
    r15_recv_if_send, r15_send_if_recv, r16_recv_if_send, r16_send_if_recv = trial_2('l1000_2_2.txt')
    #
    run(r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv, r4_recv_if_send, r4_send_if_recv, r5_recv_if_send, r5_send_if_recv, r6_recv_if_send, r6_send_if_recv, r7_recv_if_send, r7_send_if_recv, r8_recv_if_send, r8_send_if_recv,r9_recv_if_send, r9_send_if_recv, r10_recv_if_send, r10_send_if_recv,r11_recv_if_send, r11_send_if_recv,r12_recv_if_send, r12_send_if_recv,r13_recv_if_send, r13_send_if_recv,r14_recv_if_send, r14_send_if_recv,r15_recv_if_send, r15_send_if_recv,r16_recv_if_send, r16_send_if_recv)
main()
#DB Description (2)
#LS Update (4)
#LS Request (3)
#LS Acknowledge (5)
#Hello Packet (1)
