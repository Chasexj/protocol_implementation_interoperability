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
    recv ={"172.17.0.310.10.0.2":"172.17.0.4","172.17.0.310.10.0.18":"172.17.0.5","172.17.0.410.10.0.3":"172.17.0.3","172.17.0.410.10.0.10":"172.17.0.5","172.17.0.510.10.0.11":"172.17.0.4","172.17.0.510.10.0.19":"172.17.0.3"}
    #r1 = 172.17.0.3
    r1 = []
    #r2 = 172.17.0.4
    r2 = []
    #r3 = 172.17.0.4
    r3 = []

    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Source: 10" in line:
                line = line.strip("Source: ")
                line = line.strip("\n")
                line = line.strip('\t')
                inter = line
            elif "Message Type" in line:
                line = line.strip("Message Type: ")
                line = line.strip("\n")
                line = line.strip('\t')
                message = line
            elif "Source OSPF Router" in line:
                line = line.strip("Source OSPF Router: ")
                line = line.strip("\n")
                line = line.strip('\t')
                src_router = line
                recv_key = src_router+inter
                des_router = recv[recv_key]
                if src_router == "172.17.0.3":
                    r1.append(message+"Send")
                elif src_router == "172.17.0.4":
                    r2.append(message+"Send")
                elif src_router == "172.17.0.5":
                    r3.append(message+"Send")
                
                if des_router == "172.17.0.3":
                    r1.append(message+"Receive")
                elif des_router == "172.17.0.4":
                    r2.append(message+"Receive")
                elif des_router == "172.17.0.5":
                    r3.append(message+"Receive")
    return r1,r2,r3

def double(fname):
    inter = ""
    src_router = ""
    des_router = ""
    message = ""
    recv ={"172.17.0.310.10.0.2":"172.17.0.4","172.17.0.410.10.0.3":"172.17.0.3"}
    #r7 = 172.17.0.3
    r7 = []
    #r8 = 172.17.0.4
    r8 = []

    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Source: 10" in line:
                line = line.strip("Source: ")
                line = line.strip("\n")
                line = line.strip('\t')
                inter = line
            elif "Message Type" in line:
                line = line.strip("Message Type: ")
                line = line.strip("\n")
                line = line.strip('\t')
                message = line
            elif "Source OSPF Router" in line:
                line = line.strip("Source OSPF Router: ")
                line = line.strip("\n")
                line = line.strip('\t')
                src_router = line
                recv_key = src_router+inter
                des_router = recv[recv_key]
                if src_router == "172.17.0.3":
                    r7.append(message+"Send")
                elif src_router == "172.17.0.4":
                    r8.append(message+"Send")
                
                if des_router == "172.17.0.3":
                    r7.append(message+"Receive")
                elif des_router == "172.17.0.4":
                    r8.append(message+"Receive")
    return r7,r8

def run(final_result):
    send_dict = defaultdict(set)
    recv_dict = defaultdict(set)
    for i in range(len(final_result)):
        for j in range(len(final_result[i])):
            r = final_result[i][j]
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

    final_result = []
    files3 = ['800_1_3.txt','800_2_3.txt']
    files2 = ["1000_1_2.txt"]
    for input_file3 in files3:
        final_result.append(triangle(input_file3))
    for input_file2 in files2:
        final_result.append(double(input_file2))
    run(final_result)

main()
#DB Description (2)
#LS Update (4)
#LS Request (3)
#LS Acknowledge (5)
#Hello Packet (1)
