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
peers=[]              # stores list of peers
all_files=list()

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host= inet_addr()
port=9999
s.bind((host,port))

print("waiting..."+str(host))
s.listen(5)
while True:
	conn,addr=s.accept()
	print("connected "+str(addr))
	peers.append(addr)
	print(peers)
	
	conn.sendall(b"Index Server wants File list")
	files_data=conn.recv(1024).decode()
	all_files.append(index_peers(files_data,addr[0]))
	print(all_files)
	
	dataa=pickle.dumps(all_files)
	conn.sendall(dataa)
	print("Sent data to peer")
	conn.close()
s.close()













