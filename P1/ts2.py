import socket
import threading
import time
import random
import sys

from xml import dom

def ts1():
    try:
        ts1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    
    # Listening Port
    tsListenPort = int(sys.argv[1])
    server_binding = ('', tsListenPort)
    ts1_socket.bind(server_binding)
    
    host = socket.gethostname()
    print("[TS1]: host name is {}".format(host))

    localhost_ip = (socket.gethostbyname(host))
    print("[TS1]: IP address is {}".format(localhost_ip))

    ts1_socket.listen(5)

    timeout = 10
    
    timeout_start = time.time()
    lsSocketId, addr = ts1_socket.accept()
    while True: 
        # Query towards the DNS server
        lineBeingReturned = "PENDING"
        stringAccepted = lsSocketId.recv(1024).decode('utf-8')
        if(stringAccepted == ""):
            break
        print(stringAccepted)
        # Opening the file pointer
        readFilePtr = open("PROJ2-DNSTS2.txt", "r")
        #Find first index for the space and if it 
        for line in readFilePtr:
            indexOfSpace = line.find(" ")
            domainString = line[0:indexOfSpace]
            if domainString.lower() == stringAccepted.lower():
                lineBeingReturned = line.strip()
                lineBeingReturned = lineBeingReturned + " IN"
                lsSocketId.send(lineBeingReturned.encode('utf-8'))
                break
    ts1_socket.close()
    exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='DNS_Server_1', target=ts1)
    t1.start()
    print("Done.") 
