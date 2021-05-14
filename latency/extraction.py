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
                #####can add more information/conditions to distinguish packets if want to
                #####below is excample
                if message == "LS Update (4)" or message == "LS Acknowledge (5)":
                    while peek_line(file):
                        line = file.readline()
                        if "~" not in line:
                            # if "LS Type" in line:
                            #     LSTline = line.strip("\n")
                            #     LSTline = LSTline.strip('\t')
                            #     LSTline = LSTline.strip("LS Type: ")
                            # elif "Link State ID: " in line:
                            #     LSIDline = line.strip("\n")
                            #     LSIDline = LSIDline.strip('\t')
                            #     LSIDline = LSIDline.strip("Link State ID: ")
                            # elif "Advertising Router" in line:
                            #     ARline = line.strip("\n")
                            #     ARline = ARline.strip('\t')
                            #     ARline = ARline.strip("Advertising Router: ")
                            # elif "Sequence Number" in line:
                            #     SNline = line.strip("\n")
                            #     SNline = SNline.strip('\t')
                            #     SNline = SNline.strip("Sequence Number: ")
                            #     if "/AR"+ARline + "SN"+SNline not in message:
                            #         message = message + "/LST"+LSTline+ "LSID"+LSIDline+ "AR"+ARline + "SN"+SNline
                            if "Sequence Number" in line:
                                SNline = line.strip("\n")
                                SNline = SNline.strip('\t')
                                SNline = SNline.strip("Sequence Number: ")
                                if "SN"+SNline not in message:
                                    message = message + "/SN"+SNline+"END"
                        else:
                            break
                #####
                #Assign messages to router sets with sent or receive at end of message
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

    result = [r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv, r3_recv_if_send, r3_send_if_recv]
    return result

def double(fname):
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
                #####can add more information/conditions to distinguish packets if want to
                #####below is excample
                if message == "LS Update (4)" or message == "LS Acknowledge (5)":
                    while peek_line(file):
                        line = file.readline()
                        if "~" not in line:
                            # if "LS Type" in line:
                            #     LSTline = line.strip("\n")
                            #     LSTline = LSTline.strip('\t')
                            #     LSTline = LSTline.strip("LS Type: ")
                            # elif "Link State ID: " in line:
                            #     LSIDline = line.strip("\n")
                            #     LSIDline = LSIDline.strip('\t')
                            #     LSIDline = LSIDline.strip("Link State ID: ")
                            # elif "Advertising Router" in line:
                            #     ARline = line.strip("\n")
                            #     ARline = ARline.strip('\t')
                            #     ARline = ARline.strip("Advertising Router: ")
                            # elif "Sequence Number" in line:
                            #     SNline = line.strip("\n")
                            #     SNline = SNline.strip('\t')
                            #     SNline = SNline.strip("Sequence Number: ")
                            #     if "/AR"+ARline + "SN"+SNline not in message:
                            #         message = message + "/LST"+LSTline+ "LSID"+LSIDline+ "AR"+ARline + "SN"+SNline
                            if "Sequence Number" in line:
                                SNline = line.strip("\n")
                                SNline = SNline.strip('\t')
                                SNline = SNline.strip("Sequence Number: ")
                                if "SN"+SNline not in message:
                                    message = message + "/SN"+SNline+"END"
                        else:
                            break
                #####
                #Assign messages to router sets with sent or receive at end of message
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

    result = [r1_recv_if_send, r1_send_if_recv, r2_recv_if_send, r2_send_if_recv]
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

    with open ('extraction_output.txt', 'w') as f:
            f.write("List of packets can be received given last sent packet type"+"\n")
            for key in recv_dict:
                f.write(key+"\n")
                f.write(str(recv_dict[key])+"\n")
                # ##### amount of packet can be added by uncommenting
                # p_amount = ""
                # for value in recv_dict[key]:
                #     pair = key + value
                #     p_amount = p_amount + str(recv_dict_counter[pair]) + "/"
                # f.write(p_amount+"\n")
                # f.write("\n")
                # #####
            f.write("###########################################################################################################################################################\n")
            f.write("List of packets can be send given last received packet type"+"\n")
            for key in send_dict:
                f.write(key+"\n")
                f.write(str(send_dict[key])+"\n")

    with open ('specific_extraction_output.txt', 'w') as f:
            f.write("List of packets can be received given last sent packet type"+"\n")
            for key in recv_dict:
                if "LS Update (4)" in key:
                f.write(key+"\n")
                f.write(str(recv_dict[key])+"\n")
                # ##### amount of packet can be added by uncommenting
                # p_amount = ""
                # for value in recv_dict[key]:
                #     pair = key + value
                #     p_amount = p_amount + str(recv_dict_counter[pair]) + "/"
                # f.write(p_amount+"\n")
                # f.write("\n")
                # #####
            f.write("###########################################################################################################################################################\n")
            f.write("List of packets can be send given last received packet type"+"\n")
            for key in send_dict:
                f.write(key+"\n")
                f.write(str(send_dict[key])+"\n")


def main():
    final_result = []
    files3 = ['l800_1_3.txt',
    'l800_2_3.txt']

    for input_file3 in files3:
        final_result.append(triangle(input_file3))

    files2 = ['l1000_1_2.txt']
    for input_file2 in files2:
        final_result.append(double(input_file2))

    #final_result.append(star('star_1000.txt'))
    #final_result.append(linear('linear_1000.txt'))

    run(final_result)
main()
#DB Description (2)
#LS Update (4)
#LS Request (3)
#LS Acknowledge (5)
#Hello Packet (1)
