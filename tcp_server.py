import socket
import os
from _thread import *
import pickle


def index_peers(files_data,address):
	l=list()
	k=files_data.split('\n')
	m=k[:-1]
	n=k[-1]
	l.append(n)
	l.append(m)
	return l
    
# Code begins here
all_files=list()  # stores list of peers with file details

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host="159.65.148.201"
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
	for i in all_files:
		print(i)
	
	data=pickle.dumps(all_files)
	conn.sendall(data)
	print("Sent data to peer")
	conn.close()
s.close()

