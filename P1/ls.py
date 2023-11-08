import socket
import sys
import threading
import time
import random
import select


def server():
    try:
        ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    try:
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS2 Socket socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    #Server Binding
    lsListenPort = int(sys.argv[1])
    localhost_addr = socket.gethostbyname(socket.gethostname())
    print("[LS]: localhost: " + localhost_addr)
    host = socket.gethostname()
    print("[TS1]: host name is {}".format(host))
    server_binding = ('', lsListenPort)
    ls.bind(server_binding)
    ls.listen(30)
    cs, addr = ls.accept()


    #TS1 Connection
    ts1HostName = sys.argv[2]
    ts1Port = int(sys.argv[3])
    ts1_binding = (socket.gethostbyname(str(sys.argv[2])), ts1Port)
    ts1.connect(ts1_binding)
    print("Connection to TS1 Worked")
    
    #TS2 Connection
    ts2HostName = sys.argv[4]
    ts2Port = int(sys.argv[5])
    ts2_binding = (socket.gethostbyname(str(sys.argv[4])), ts2Port)
    ts2.connect(ts2_binding)
    print("Connection to TS2 Worked")

    ls.setblocking(0)
    # ls.listen(5)

    # clientSocketId, addr = ls.accept()

    #TS1 Connection
    inputs = [ts1, ts2]
    outputs = []
    message_queues = []
    while(inputs):
        lineBeingSent = cs.recv(1024).decode('utf-8')
        if(lineBeingSent == ""):
            break
        print(lineBeingSent + "What is being sent")
        ts1.send(lineBeingSent.encode('utf-8'))
        ts2.send(lineBeingSent.encode('utf-8'))
        readable, writeable, exceptional = select.select(inputs, outputs, inputs, 5)
        if not readable: 
            print("TS1 or TS2 did not have the mapping")
            receivedLine = lineBeingSent + " - TIMED OUT"
            cs.send(receivedLine.encode('utf-8'))
        else:
            for s in readable: 
                if(s == ts1):
                    print("TS1 socket had the mapping")
                    receivedLine = ts1.recv(1024).decode('utf-8')
                    print(receivedLine + " what was received from ts1")
                    cs.send(receivedLine.encode('utf-8'))
                    break
                elif(s == ts2):
                    print("TS2 socket had the mapping")
                    receivedLine = ts2.recv(1024).decode('utf-8')
                    print(receivedLine + " what was received from ts2")
                    cs.send(receivedLine.encode('utf-8'))
                    break

        inputs = [ts1, ts2]
        
    #localhost_addr = socket.gethostbyname(socket.gethostname())
    #print("[LS]: localhost: " + localhost_addr)
    
    #csockid, addr = ls.accept()
    #while True: 
        #stringAccepted = csockid.recv(1024).decode('utf-8')
        #if(stringAccepted == ""):
            #break
        #ls.send(stringAccepted.encode('utf-8'))


    # send a intro message to the client.  
    # msg = "Welcome to CS 352!"
    # csockid.send(msg.encode('utf-8'))
    #stringReverse = csockid.recv(1024).decode('utf-8')
    #stringReverse = stringReverse[::-1]
    #csockid.send(stringReverse.encode('utf-8'))
    
    #readFilePtr = open("in-proj.txt", "r")
    #count = 0
    #for line in readFilePtr:
        #stringReverse = csockid.recv(1024).decode('utf-8')
        #stringReverse = stringReverse[::-1]
        #stringReverse = stringReverse.lstrip("\n")
        #count += 1
        #csockid.send(stringReverse.encode('utf-8'))

    # Close the server socket
    ls.close()
    exit()

if __name__ == "__main__":
    t2 = threading.Thread(name='server', target=server)
    t2.start()
    print("Done.")
