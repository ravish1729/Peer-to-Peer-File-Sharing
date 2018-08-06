import socket
import os
import pickle
import threading


def inet_addr():
	'''
	Tells the IP address of client.
	'''
	os.system("ifconfig wlp9s0 | grep 'inet addr' > ip.txt")     # System call to read IP address of client in the network     
	f=open("ip.txt",'r')										 # IN subsequent lines of function IP address is read from text file
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


def client_thread():
	print("IP Address of Server for the File Request")
	host = str(input())
	port = 1234
	client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	client_socket.connect((host,port))
	print(client_socket.recv(1024).decode())
	file_name = str(input())
	client_socket.sendall(file_name.encode())
	file_received=client_socket.recv(8056).decode()
	f=open(file_name, 'wb')
	f.write(file_received)
	os.system("notify-send 'Received'")
	f.close()
	client_socket.close()


def server_thread():
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	host= inet_addr()
	port=1234
	server_socket.bind((host,port))
	print("waiting..."+str(host))
	server_socket.listen(5)
	while True:
		conn,addr=server_socket.accept()
		print("connected "+str(addr))
		conn.sendall(b"File Name")
		files_name=conn.recv(1024).decode()
		try:
			f=open(file_name,'rb')
			l=f.read()
			conn.sendall(l)
		except:
			conn.sendall(b"File not found")
		print('Disconnected with client')

def main(network_ip):
	# Connect to the network
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host= network_ip
	port= 9999
	s.connect((host,port))   # Connect to socket (IP address+Port number)
	
	# Details of server
	data = s.recv(1024).decode()
	print(data)
	
	# Send files in your shared folder to the index server
	files=list_files()
	s.sendall(files.encode())
	print(files)
	os.system("notify-send 'Sent!'") # Push notification 
	
	# List of files in the network
	peer_files = s.recv(1024)
	peer_files = pickle.loads(peer_files)
	s.close()
	print(peer_files)
	
	# Starting the client and server thread
	print("want to receive some files y/n")
	decision=str(input())
	if(decision=='y'):
	#client_thread()
		threading.Thread(target=client_thread, args=()).start()
	#server_thread()
	threading.Thread(target=server_thread, args=()).start()

print("IP Address of Network")
network_ip=str(input())
main(network_ip)
