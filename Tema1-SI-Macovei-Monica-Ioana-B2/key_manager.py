#tutorial socket https://www.journaldev.com/15906/python-socket-programming-server-client
from Crypto.Cipher import AES
import socket
import random
import time
from base64 import b64encode
import base64

class KeyManager:
    K3 = "bFAZAYQqZbQaU7tX"
    def get_key(self, mode):
        if mode == "CBC":
            self.__K1 = self.generate_key()
            aes = AES.new(self.K3, AES.MODE_ECB) #apelez functia de initializare cu K3 si mod de criptare ECB
            return aes.encrypt(self.__K1), aes.encrypt(self.generate_IV())

        else:
            self.__K2 = self.generate_key()
            aes = AES.new(self.K3, AES.MODE_ECB) 
            return aes.encrypt(self.__K2), aes.encrypt(self.generate_IV())

    def generate_key(self):
        key = ''
        for _ in range(16):
            code = random.randint(48,122) #genereaza un numar intre 48 si 122 (0 si z, codul ASCII)
            key += chr(code) #transform din ASCII in string
        return key

    def generate_IV(self):
        IV = ''
        for _ in range(16):
            code = random.randint(48,122) #genereaza un numar intre 48 si 122 (0 si z, codul ASCII)
            IV += chr(code) #transform din ASCII in string
        return IV

def server_program():
    host = socket.gethostname()
    port = 5000 

    server_socket = socket.socket() 
    server_socket.bind((host, port)) 

    server_socket.listen(2)
    
    KM = KeyManager()

    while True:
        conn, address = server_socket.accept() 
        print("Connection from: " + str(address))

        mode = conn.recv(3).decode() #primim prin socket modul de folosire care are 3 caractere
        if not mode:
            break
        
        print("Key for the mode:",mode)
        key, IV = KM.get_key(mode) #generez cheia si IV criptate (generate in functie de mod)
       
        conn.send(key)  #trimitem cheia, care are 16 caractere
        conn.send(IV)   #trimitem IV, care are 16 caractere
        print("Key and IV sent")

    conn.close() 


if __name__ == '__main__':
    server_program()


