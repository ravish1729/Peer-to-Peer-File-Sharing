import socket
import os
import pickle
import threading

# Get the inet address
def inet_addr():
	os.system("ifconfig wlp6s0 | grep 'inet addr' > ip.txt")
	f=open("ip.txt",'r')
	my_host=(((f.read()).lstrip()).split(' ')[1]).split(':')[1]
	f.close()
	os.system("rm ip.txt")
	return my_host

def list_files():
	os.system("ls shared > listy.txt")
	f=open("listy.txt",'r')
	l=f.read()
	f.close()
	os.system("rm listy.txt")
	return l

# Client Thread
def client_thread(peer_files):
	print(peer_files)
	print("IP Address of Server for the File Request")
	host = str(input())
	port = 12345
	s.connect((host,port))
	print(s.recv(1024).decode())
	file_name = str(input())
	s.sendall(file_name.encode())
	file_received=s.recv(4028)
	conn.close()

# Server Thread
def server_thread():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	host= inet_addr()
	port=1234
	s.bind((host,port))
	print("waiting..."+str(host))
	s.listen(5)
	while True:
		conn,addr=s.accept()
		print("connected "+str(addr))
		conn.sendall(b"File Name")
		files_name=conn.recv(1024).decode()
		try:
			f=open(file_name,'rb')
			l=f.read()
			conn.sendall(l)
		except:
			conn.sendall(b"File not found")
		
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= "10.7.3.108"
port= 9999
s.connect((host,port))

data = s.recv(1024).decode()
print(data)

files=list_files()
s.sendall(files.encode())
print(files)
os.system("notify-send 'Sent!'")

peer_files = s.recv(1024)
peer_files = pickle.loads(peer_files)
s.close()

#threading.Thread(target=server_thread, args=()).start()
threading.Thread(target=client_thread, args=(peer_files,)).start()
