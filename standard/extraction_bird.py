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

def trial_1():
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.210.10.0.2":"10.10.0.3","10.10.0.210.10.0.18":"10.10.0.11","10.10.0.310.10.0.3":"10.10.0.2","10.10.0.310.10.0.10":"10.10.0.11","10.10.0.1110.10.0.11":"10.10.0.3","10.10.0.1110.10.0.19":"10.10.0.2"}
    #r1 = 10.10.0.2
    r1 = []
    #r2 = 10.10.0.3
    r2 = []
    #r3 = 10.10.0.11
    r3 = []

    with open ("b800_1_3.txt") as file:
        while peek_line(file):
            line = file.readline()
            if "Source: 10" in line:
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
                    r1.append(message+"Send")
                elif src_router == "10.10.0.3":
                    r2.append(message+"Send")
                elif src_router == "10.10.0.11":
                    r3.append(message+"Send")
                
                if des_router == "10.10.0.2":
                    r1.append(message+"Receive")
                elif des_router == "10.10.0.3":
                    r2.append(message+"Receive")
                elif des_router == "10.10.0.11":
                    r3.append(message+"Receive")
    return r1,r2,r3

def trial_2():
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.210.10.0.2":"10.10.0.3","10.10.0.210.10.0.18":"10.10.0.11","10.10.0.310.10.0.3":"10.10.0.2","10.10.0.310.10.0.10":"10.10.0.11","10.10.0.1110.10.0.11":"10.10.0.3","10.10.0.1110.10.0.19":"10.10.0.2"}
    #r4 = 10.10.0.2
    r4 = []
    #r5 = 10.10.0.3
    r5 = []
    #r6 = 10.10.0.11
    r6 = []

    with open ("b800_2_3.txt") as file:
        while peek_line(file):
            line = file.readline()
            if "Source: 10" in line:
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
                    r4.append(message+"Send")
                elif src_router == "10.10.0.3":
                    r5.append(message+"Send")
                elif src_router == "10.10.0.11":
                    r6.append(message+"Send")
                
                if des_router == "10.10.0.2":
                    r4.append(message+"Receive")
                elif des_router == "10.10.0.3":
                    r5.append(message+"Receive")
                elif des_router == "10.10.0.11":
                    r6.append(message+"Receive")
    return r4,r5,r6

def trial_3():
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"10.10.0.210.10.0.2":"10.10.0.3","10.10.0.310.10.0.3":"10.10.0.2"}
    #r7 = 10.10.0.2
    r7 = []
    #r8 = 10.10.0.3
    r8 = []

    with open ("b1000_1_2.txt") as file:
        while peek_line(file):
            line = file.readline()
            if "Source: 10" in line:
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
                    r7.append(message+"Send")
                elif src_router == "10.10.0.3":
                    r8.append(message+"Send")
                
                if des_router == "10.10.0.2":
                    r7.append(message+"Receive")
                elif des_router == "10.10.0.3":
                    r8.append(message+"Receive")
    return r7,r8

def run(r1,r2,r3,r4,r5,r6,r7,r8):
    send_dict = defaultdict(set)
    recv_dict = defaultdict(set)
    for i in range(8):
        if i == 0:
            r = r1
        elif i ==1:
            r = r2
        elif i == 2:
            r = r3
        elif i == 3:
            r = r4
        elif i == 4:
            r = r5
        elif i == 5:
            r = r6
        elif i == 6:
            r = r7
        elif i == 7:
            r = r8
        last_send= ""
        for msg in r:
            if r.index(msg) == 0:
                if "Send" in msg:
                    last_send = msg
            else:
                if "Receive" in msg:
                    recv_dict[last_send.strip("Send")].add(msg.strip("Receive"))
                elif "Send" in msg:
                    last_send = msg
        last_receive = ""
        for msg in r:
            if r.index(msg) == 0:
                if "Receive" in msg:
                    last_receive = msg
            else:
                if "Send" in msg:
                    send_dict[last_receive.strip("Receive")].add(msg.strip("Send"))
                elif "Receive" in msg:
                    last_receive = msg


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
    r1,r2,r3 = trial_1()
    r4, r5, r6 = trial_2()
    r7,r8 = trial_3()
    run(r1,r2,r3,r4,r5,r6,r7,r8)
    #run(r1,r2,r3,r4,r5,r6)

main()
#DB Description (2)
#LS Update (4)
#LS Request (3)
#LS Acknowledge (5)
#Hello Packet (1)
