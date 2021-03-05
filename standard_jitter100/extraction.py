import re 
import json
import argparse
import os
import socket
import struct
import fileinput
from collections import defaultdict
from collections import Counter

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
    recv ={"172.17.0.210.10.0.2":"172.17.0.3","172.17.0.210.10.0.18":"172.17.0.4","172.17.0.310.10.0.3":"172.17.0.2","172.17.0.310.10.0.10":"172.17.0.4","172.17.0.410.10.0.11":"172.17.0.3","172.17.0.410.10.0.19":"172.17.0.2"}
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
    recv ={"172.17.0.210.10.0.2":"172.17.0.3","172.17.0.310.10.0.3":"172.17.0.2"}
    #r7 = 172.17.0.3
    r7 = []
    #r8 = 172.17.0.4
    r8 = []

    with open (fname) as file:
        while peek_line(file):
            line = file.readline()
            if "Source: 10" in line:
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
    send_dict_counter = Counter()
    recv_dict_counter = Counter()
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
                        recv_dict_counter[last_send.strip("Send")+msg.strip("Receive")]+=1
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
                        send_dict_counter[last_receive.strip("Receive")+msg.strip("Send")]+=1
                    elif "Receive" in msg:
                        last_receive = msg


    print("List of packets can be received given last sent packet type")
    for key in recv_dict:
        print(key)
        print(recv_dict[key])
        frequency = ""
        for value in recv_dict[key]:
            pair = key + value
            frequency = frequency + str(recv_dict_counter[pair]) + "/"
        print(frequency)
        print("\n")
    print("-------------------------------------------------------------------")
    print("List of packets can be send given last received packet type")
    for key in send_dict:
        print(key)
        print(send_dict[key])
        frequency = ""
        for value in send_dict[key]:
            pair = key + value
            frequency = frequency + str(send_dict_counter[pair]) + "/"
        print(frequency)
        print("\n")

def main():

    final_result = []
    files3 = ['800_1_3.txt','800_2_3.txt','800_3_3.txt','800_4_3.txt',
    '800_5_3.txt','800_6_3.txt','800_7_3.txt','800_8_3.txt',
    '800_9_3.txt','800_10_3.txt','800_11_3.txt','800_12_3.txt',
    '800_13_3.txt','800_14_3.txt','800_15_3.txt']
    files2 = ["1000_1_2.txt","1000_2_2.txt","1000_3_2.txt","1000_4_2.txt",
    "1000_5_2.txt","1000_6_2.txt","1000_7_2.txt","1000_8_2.txt","1000_9_2.txt",
    "1000_10_2.txt"]
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
