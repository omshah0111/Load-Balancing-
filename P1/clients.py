import socket
import threading
import time
import random
import sys

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(sys.argv[2])
    localhost_addr = socket.gethostbyname(socket.gethostname())
    print("[C]: localhost: " + localhost_addr)
    
    lsServer_hostName = str(sys.argv[1])
    # connect to the server on local machine
    ls_binding = (socket.gethostbyname(str(sys.argv[1])), port)
    cs.connect(ls_binding)

    # Read and write file pointers
    readFilePtr = open("PROJ2-HNS.txt", "r")
    writeFilePtr = open("RESOLVED.txt", "w")

    # Sending and receiving data
    for line in readFilePtr:
        print(line)
        sent = line.strip()
        cs.send(sent.encode('utf-8'))
        data_from_server = cs.recv(1024)
        data_from_server = data_from_server.decode('utf-8')
        data_from_server += "\n"
        writeFilePtr.write(data_from_server)
    writeFilePtr.close()
    
    # Close the client socket
    cs.close()
    exit()

    # Receive data from the server

    # data_from_server=cs.recv(100)
    # print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8'))
    #helloString = "HELLO"
    #cs.send(helloString.encode('utf-8'))
    #data_from_server = cs.recv(300)
    #data_from_server = data_from_server.decode('utf-8')
    #print(data_from_server)

    #readFilePtr = open("in-proj.txt", "r")
    #writeFilePtr = open("output.txt", "w")
    #count = 0; 
    #for line in readFilePtr:
        #cs.send(line.encode('utf-8'))
        #data_from_server = cs.recv(300)
        #data_from_server = data_from_server.decode('utf-8')
        #writeFilePtr.write(data_from_server + "\n")
    #writeFilePtr.close()

    

if __name__ == "__main__":
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
    print("Done.")
