import re
def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

with open ('s.txt') as file:
    while peek_line(file):
        line = file.readline()
        line = line.strip('\n')
        send_result = re.search('Send at (.*) to ', line)
        send_time = float(send_result.group(1))
        send_time = round(1000000*(send_time - 1607588029.598773000)/1000,2)
        ptype = re.search('(.*)Send at', line)
        p = str(ptype.group(1))
        print(str(send_time) + "   "+ p)

print()

with open ('r.txt') as file:
    while peek_line(file):
        line = file.readline()
        line = line.strip('\n')
        recv_result = re.search('Receive at (.*) from ', line)
        recv_time = float(recv_result.group(1))
        recv_time = round(1000000*(recv_time - 1607588029.598705000)/1000,2)
        ptype = re.search('(.*)Receive at', line)
        p = str(ptype.group(1))
        print(str(recv_time) + "   "+ p)

        #send_result =re .search('Send at (.*) to ', send_item)