import re 
import json
import argparse
import os
import socket
import struct
import fileinput
from collections import defaultdict
from collections import Counter
from pydtmc import (
    MarkovChain,
    plot_graph
)

from pytest import (
    mark
)
import matplotlib.pyplot as plt

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
                #############
                if message == "LS Update (4)":
                    while peek_line(file):
                        line = file.readline()
                        if "~" not in line:
                            if "Advertising Router" in line:
                                ARline = line.strip("\n")
                                ARline = ARline.strip('\t')
                                ARline = ARline.strip("Advertising Router: ")
                            elif "Sequence Number" in line:
                                SNline = line.strip("\n")
                                SNline = SNline.strip('\t')
                                SNline = SNline.strip("Sequence Number: ")
                                if "/AR"+ARline + "SN"+SNline not in message:
                                    message = message + "/AR"+ARline + "SN"+SNline
                        else:
                            break
                elif message == "LS Acknowledge (5)":
                    while peek_line(file):
                        line = file.readline()
                        if "~" not in line:
                            if "Advertising Router" in line:
                                ARline = line.strip("\n")
                                ARline = ARline.strip('\t')
                                ARline = ARline.strip("Advertising Router: ")
                            elif "Sequence Number" in line:
                                SNline = line.strip("\n")
                                SNline = SNline.strip('\t')
                                SNline = SNline.strip("Sequence Number: ")
                                if "/AR"+ARline + "SN"+SNline not in message:
                                    message = message +"/AR"+ARline+"SN"+SNline
                        else:
                            break
                #############
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
                #############
                if message == "LS Update (4)":
                    while peek_line(file):
                        line = file.readline()
                        if "~" not in line:
                            if "Advertising Router" in line:
                                ARline = line.strip("\n")
                                ARline = ARline.strip('\t')
                                ARline = ARline.strip("Advertising Router: ")
                            elif "Sequence Number" in line:
                                SNline = line.strip("\n")
                                SNline = SNline.strip('\t')
                                SNline = SNline.strip("Sequence Number: ")
                                if "/AR"+ARline + "SN"+SNline not in message:
                                    message = message + "/AR"+ARline + "SN"+SNline
                        else:
                            break
                elif message == "LS Acknowledge (5)":
                    while peek_line(file):
                        line = file.readline()
                        if "~" not in line:
                            if "Advertising Router" in line:
                                ARline = line.strip("\n")
                                ARline = ARline.strip('\t')
                                ARline = ARline.strip("Advertising Router: ")
                            elif "Sequence Number" in line:
                                SNline = line.strip("\n")
                                SNline = SNline.strip('\t')
                                SNline = SNline.strip("Sequence Number: ")
                                if "/AR"+ARline + "SN"+SNline not in message:
                                    message = message +"/AR"+ARline+"SN"+SNline
                        else:
                            break
                #############
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
    transition_counter = Counter()
    for i in range(len(final_result)):
        for j in range(len(final_result[i])):
            for k in range(len(final_result[i][j])-1):
                transition_counter[final_result[i][j][k]+"|||"+final_result[i][j][k+1]]+=1
    first_total = Counter()
    for i in transition_counter:
        first_total[i.split("|||")[0]]+=transition_counter[i]
    final_frequency = defaultdict()
    for i in transition_counter:
        final_frequency[i] = transition_counter[i]/first_total[i.split("|||")[0]]
    #list of all the nodes
    node_list = []
    for i in first_total:
        node_list.append(i)
    # list of frequencies
    p = [ [0]*len(node_list) for _ in range(len(node_list))]
    for i in node_list:
        for j in node_list:
            if i+"|||"+j in final_frequency:
                p[node_list.index(i)][node_list.index(j)]=final_frequency[i+"|||"+j]
    ##node_list rename, save_correspondance to default_dict
    symbol_packet_pair = defaultdict()
    symbol = 0
    print("Converting packet name to symbol...")
    for i in range(len(node_list)):
        symbol_packet_pair[str(symbol)]=node_list[i]
        node_list[i]=str(symbol)
        symbol = symbol+1
    print("Writing out symbol_packet_pair...")
    with open ('extraction_symbol_packet_pair.txt', 'w') as f:
        for i in symbol_packet_pair:
            f.write(i+"   :   "+symbol_packet_pair[i]+"\n")

    mc = MarkovChain(p, node_list)
    print(mc)
    print(mc.transition_probability('17','22'))
    # print("Plotting MC...")
    # plt.figure.Figure = plot_graph(mc)[0]
    # plt.subplots.figure = plot_graph(mc)[1]
    # plt.savefig("figure.png")

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
