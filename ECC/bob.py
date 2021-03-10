import socket
import ECC as ecc
import re
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('\nWaiting for Alice connection.')
serv.bind(('127.0.0.1', 8080))
serv.listen(5)
privateKey = 5
conn, addr = serv.accept()
print('\nGenerating Public Key for Bob')
publicKey = ecc.generatePublicKey(privateKey)
publicKeyrecvX = conn.recv(8192)
publicKeyrecvY = conn.recv(8192)
print('\nPublic Key of Alice recieved:',int(publicKeyrecvX.decode()),int(publicKeyrecvY.decode()))
conn.send(str(publicKey[0]).encode())
conn.send(str(publicKey[1]).encode())
filename = conn.recv(4096)
f = open(filename.decode(),"r")
print('\nEncrypted File Recieved.Decrypting Message from file.')
cipher = []
for x in f:
    cipher.append(x)
f.close()
text = ''
for i in cipher:
    i = i.replace('\n','')
    i = i.replace(', ',',')
    print(i)
    c = i.split(' ')
    c1 = c[0].replace('(','').replace(')','').split(',')
    c2 = c[1].replace('(','').replace(')','').split(',')
    C1 = (int(c1[0]),int(c1[1]))
    C2 = (int(c2[0]),int(c2[1]))
    text += chr(ecc.decryptionECC(C1,C2,privateKey)[0])
conn.close()
print('\nMessage Decrypted: ',text)
