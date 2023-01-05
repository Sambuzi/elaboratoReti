# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:41:36 2022

@author: sajmi
"""

# -- coding: utf-8 --

# Buzi Sajmir  - sajmir.buzi@studio.unibo.it - 0000975520

# Traccia 2 - Archittettura client-server UDP per il trasferimento file


#--------- UDP SERVER in PYTHON -----------#


import socket as sk     #necessario per la comunicazione
import os               #serve per interfacciarsi con il sistema operativo
import sys              #per importare comandi da riga di comando
import time 
buffer = 1024
  
#funzioni 
def checkPort(num):
	try:
		port = int(num)

	except:
		print("\nError! Invalid Port Number\n")
		sys.exit()
        
	if port < 1025 or port > 65535:
		print("\nWrong Port Number\n")
		return 0

	else:
		return port
    
    
def checkArgv(arg):
		
	if len(arg) == 3:
		return True
	else:
		return False



def ServerList():
    try:
        files = os.listdir()
        lists = []
            
        for file in files:
            lists.append(file)  #creazione lista dei file
            
        return str(lists)
    
    except:
        print("Server Error\n")
        return "0"
        
        
        
def UDPServer(host, port): 
    try:
        sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)     
        sAddr = ((host, port))
        sock.bind(sAddr)                            #associazione di un socket alla tupla (indirizzo, porta)
        print("\nServer Ready on Port " + str(port) + "\n\n")
        
        while True:
            msgEn, cAddr = sock.recvfrom(buffer)
            msg = msgEn.decode('utf-8')
            istr = msg.split("**")[1]
            print(istr)
            
            if int(msg.split("**")[0]) != 0:      #contollo integrità pacchetto
                message = "-1** "
                
            else:
                message = "1**"
            print("server OK")
            time.sleep(1)
            if istr == "menu":
                message = message + "\nUDP Server actions:\n" 
                message = message + "            ------ menu ---------"
                message = message + "            shows list of operations \n"
                message = message + "            ------ list ---------"
                message = message + "            Lists all Server Files \n "
                message = message + "            ------ get  --------"
                message = message + "            Get a file from Server \n"
                message = message + "            ------ put  --------"
                message = message + "            Put a file into Server dir \n "
                message = message + "            ------ exit --------\n\n"

                msgEn = message.encode()
                sock.sendto(msgEn, cAddr)
			
            if istr == "list":
                msg = message + ServerList()
                sock.sendto(msg.encode('utf-8'), cAddr)

            elif istr == "exit":
                message = message + "Exiting..."
                sock.sendto(message.encode(), cAddr)
                sock.close()
                sys.exit()

            elif istr == "get":
                msg = message + "Ready!"
                sock.sendto(msg.encode(), cAddr)
                commEn, cAddr = sock.recvfrom(buffer)
                fName = commEn.decode('utf-8').split("**")[1]
                print("--file " + fName +"moved into client")
                
                if os.path.isfile(fName):
                    msg = message + "FileExists"
                    sock.sendto(msg.encode(), cAddr)
                    file = open(fName, 'rb')        #apriamo il file in lettura binaria
                    t = True
                    
                    while t:
                        pack = file.read(996)
                        
                        if not pack:
                            pack = 'EOF'.encode()
                            t = False
                            file.close()
                        
                        msgEn, cAddr = sock.recvfrom(buffer)
                        sock.sendto(pack, cAddr)
                                                          
                else:
                    msg = message + "FileNotFound"
                    sock.sendto(msg.encode(), cAddr)
                    print("does not exists " + fName)
                        
            elif istr == "put":
                try:
                    msg = message + "ready"
                    sock.sendto(msg.encode(), cAddr)
                    msgEn, cAddr = sock.recvfrom(buffer)
                    fName = msgEn.decode('utf-8').split("**")[1]
                    file = open(fName, 'wb')
                    print("--file " + fName + "moved into Server")
                    t = True
                    msg = message + "ready"
                    sock.sendto(msg.encode(), cAddr)
                
                    while t:
                        pack, cAddr = sock.recvfrom(buffer)
                        file.write(pack)
                        msg = message + "recieved"
                        sock.sendto(msg.encode(), cAddr)
                    
                        if pack == 'EOF'.encode():
                            t = False
                        
                    file.close()
                    
                except:
                    print("Error\n")
                    sys.exit()
                      
    except(KeyboardInterrupt, sk.error):
        sys.exit()
                    
                    
    
			



if __name__ == '__main__' :         #quando il programma viene aperto da riga di comando
    
    try:
        
        if checkArgv(sys.argv):
            port = checkPort(sys.argv[2])
            
            if port != 0:
                UDPServer(sys.argv[1], port)
                
        else:
            print("\n\n Please Enter Server Host and Port\n")
    except (KeyboardInterrupt, IndexError):
        print("something went wrong!")
        sys.exit()