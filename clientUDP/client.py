# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -- coding: utf-8 --

# Buzi Sajmir    - sajmir.buzi@studio.unibo.it -0000975520

# Traccia 2 - Archittettura client-server UDP per il trasferimento file


#--------- UDP CLIENT in PYTHON -----------#


import socket as sk     #necessario per la comunicazione
import os               #serve per interfacciarsi con il sistema operativo
import time             #per utilizzare funzioni e oggetti legati al tempo
import sys              #per importare comandi da riga di comando


buffer = 1024
    


def checkPort(num):   #controllo della porta 
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

def sendMessage(message, sAddr):
    t = True
    n = 0  #iniziallizo a 0 la variabile dei messaggi
    
    try:
        sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM) #generazione di un socket per ogni pacchetto inviato
        
        if str(message).split("'")[0] == 'EOF'.encode() or str(message).split("'")[0] == "b" :   #per l'invio di pacchetti binari
             msgEn = message
             
        else:
            msg = str(n) + "**" + message
            msgEn = msg.encode('utf-8') 
            
        while t:
            sock.sendto(msgEn, sAddr)
            sock.settimeout(6)
            msgen, aaddr = sock.recvfrom(buffer)
            if message != "getting":                #per la ricezione di pacchetti binari
                msg = msgen.decode('utf-8')
                
            else:
                return msgen
                
            if int(msg.split('**')[0]) == 1:      #controllo di integrità
                sock.close()
                t = False
                
        return msg.split('**')[1]
    
    except (sk.timeout, sk.error):          #se non viene inviato nel tempo necceserio dettato dal timeout scatta l'eccezione
        print("\nAn Error Occurred with the Server connection")
        sys.exit()


def get(fName, sAddr):    #funzione get per downloadare file da server
    
    file = open(fName, 'wb')
    t = True
    while t:
        payload = sendMessage("getting", sAddr)
        time.sleep(0.3)                             #per evitare congestione
        
        if payload == 'EOF'.encode():
            
            file.close()
            t = False
        
        else:
            file.write(payload)
    
	

def put(fName, sAddr):   #funzione put per uploadare file sul server
    istr = sendMessage(fName, sAddr)
    
    if istr == "ready":
        file = open(fName, 'rb' )
        t = True
        
        while t:
            pack = file.read(996)
            if not pack:
                pack = 'EOF'.encode()
                t = False
                
            istr = sendMessage(pack, sAddr)
            time.sleep(0.3)  
            
            if istr != "recieved":  #controllo dell'errore se non è stato ricevuto correttamente
                print("Error")
                break
            
            time.sleep(0.3)
                
        file.close()

	
	

def UDPClient(sAddr):
    try:
        istr = sendMessage("menu", sAddr)
        print(istr)
        time.sleep(0.5)

        while True:
            #input("\n>>")
            data = input("\n>>")
            istr = data.split()
			
            if not istr:
                istr = "####"

                
            if istr[0] == "list" and len(istr) == 1:
                message = sendMessage(istr[0], sAddr)
                smsg = message.split(",")
                
                for file in smsg:
                    print(str(file))


            elif istr[0] == "exit" and len(istr) == 1:
                msg = sendMessage(istr[0], sAddr)
                print(msg)
                sys.exit()
                    
                
            elif istr[0] == "get" and len(istr) == 2:
                msg = sendMessage(istr[0], sAddr)
                
                if msg == "Ready!":
                    message = sendMessage(istr[1], sAddr)
                    
                    if message == "FileExists":
                        print(message)
                        get(istr[1], sAddr)
                        print("Get DONE\n")
                    else:
                        print("File Not Found in this directory\n\n")

            elif istr[0] == "put" and len(istr) == 2:
                
                if os.path.isfile(istr[1]): 
                    print("File Exists")
                    msg = sendMessage(istr[0], sAddr)
                    
                    if msg == "ready":
                        put(istr[1], sAddr)
                        print("Put DONE\n")
                else:
                    print("File not Found in this directory\n\n")
                    
            elif istr[0] == "menu" and len(istr) == 1:
                print("swowing menu again\n\n")
                istr = sendMessage("menu", sAddr)
                print(istr)

            else:
                print("command not recognized")
                print("insert filename if you are in GET and PUT")
    
    except(KeyboardInterrupt, sk.error):
        sys.exit()
			



if __name__ == '__main__' :
    try:
        if checkArgv(sys.argv):   
            port = checkPort(sys.argv[2])
            if port != 0:
                sAddr = (sys.argv[1], port)
                UDPClient(sAddr)
                
        else:
            print("\n\n Please Enter Server Host and Port\n")
            
    except (KeyboardInterrupt, IndexError):
        print("something went wrong!")
        sys.exit()