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
    print("Calculating frequency of occurance of packets...")
    #all unique transition pairs counter
    transition_counter = Counter()
    for i in range(len(final_result)):
        for j in range(len(final_result[i])):
            for k in range(len(final_result[i][j])-1):
                transition_counter[final_result[i][j][k]+"|||"+final_result[i][j][k+1]]+=1
    #total occurance of the first item in the transition pairs
    first_total = Counter()
    for i in transition_counter:
        first_total[i.split("|||")[0]]+=transition_counter[i]
    #converting transition_counter to pure frequency in percentage
    final_frequency = defaultdict()
    for i in transition_counter:
        final_frequency[i] = transition_counter[i]/first_total[i.split("|||")[0]]


    #proceed to rule extraction
    rule_extraction(final_frequency)


    #list of all the nodes in first_total
    node_list = []
    for i in first_total:
        node_list.append(i)
    # list of frequencies in matrixs format
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
    print("Creating markov chain...")
    mc = MarkovChain(p, node_list)
    print("Plotting MC...")
    plt.figure.Figure = plot_graph(mc)[0]
    plt.subplots.figure = plot_graph(mc)[1]
    plt.savefig("figure.png")

def rule_extraction(final_frequency):
    print("Extracting rules...")
    #default dict of investigating items
    investigating = defaultdict()
    for i in final_frequency:
        #item specification/can be modified
        first_packet = i.split("|||")[0]
        second_packet = i.split("|||")[1]
        if "LS " in first_packet and "LS " in second_packet and "LS R" not in i:
            investigating[i]=final_frequency[i]
    
    #rules
    found_ar_rule = set()
    for i in investigating:
        #finding the needed field values
        first_packet = i.split("|||")[0]
        second_packet = i.split("|||")[1]
        #ar values
        first_packet_ar = re.findall(r'AR(.*?)SN', first_packet,re.DOTALL)
        second_packet_ar = re.findall(r'AR(.*?)SN', second_packet,re.DOTALL)
        # #prints out all intersections
        # print(first_packet_ar)
        # print(second_packet_ar)
        # print(list(set(first_packet_ar) & set(second_packet_ar)))

        #identifying packets types/id for packets with intersection, more conditions can be added to add specification
        if len(list(set(first_packet_ar) & set(second_packet_ar)))>=1:
            if "Send" in first_packet:
                first_packet_id = first_packet.split('/')[0] + " Send"
            else:
                first_packet_id = first_packet.split('/')[0] + " Receive"
            if "Send" in second_packet:
                second_packet_id = second_packet.split('/')[0] + " Send"
            else:
                second_packet_id = second_packet.split('/')[0] + " Receive"
            #Rule generation
            found_ar_rule.add(first_packet_id + "|" + second_packet_id)
    with open ("extracted_rules.txt","w") as efile:
        efile.write("Observed packets with intersecting advertising router sets:\n")
        for i in found_ar_rule:
            efile.write(i+"\n")

### 88 89 99 100
#AR 0  1  1  0
#SN 0  1  2  1
#incremental to scale comparsion

# send_AR[lsa .3] receive[lsu .2] --> after lsa, it is acceptable to receive a lsu where the AR ID is not in send_AR[]
# LSU(AR,AR,AR) LSA(AR,AR,AR) --> intersection of LSU(AR,AR,AR) LSA(AR,AR,AR): 0
#
###
def main():

    final_result = []
    print("Isolating packets from log files...")
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
