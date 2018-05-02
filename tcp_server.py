import socket
import os
from _thread import *
import pickle

# Get the inet address
def inet_addr():
	os.system("ifconfig wlp6s0 | grep 'inet addr' > ip.txt")
	f=open("ip.txt",'r')
	my_host=(((f.read()).lstrip()).split(' ')[1]).split(':')[1]
	f.close()
	os.system("rm ip.txt")
	return my_host

# List files
def index_peers(files_data,address):
	l=list()
	l.append(address)
	k=files_data.split('\n')
	k=k[:-1]
	l.append(k)
	return l
    
# Code begins here
all_files=list()  # stores list of peers with file details

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host= inet_addr()
port=9999
s.bind((host,port))

print("waiting..."+str(host))
s.listen(5)
flag=0
while True:
	conn,addr=s.accept()
	print("connected "+str(addr))
	
	conn.sendall(b"Index Server wants File list")
	files_data=conn.recv(1024).decode()
	received_files=index_peers(files_data,addr[0])
	ip=received_files[0]
	upgrade_flag=1
	if(flag):
		print(ip,all_files[0][0])
		for i,j in enumerate(all_files):
			if(str(all_files[i][0]) == str(ip)):
				print("True")
				del all_files[i]
				all_files.append(received_files)
				upgrade_flag=0
				break
	if(upgrade_flag):
		all_files.append(received_files)
	flag=1
	print(all_files)
	
	data=pickle.dumps(all_files)
	conn.sendall(data)
	print("Sent data to peer")
	conn.close()
s.close()

