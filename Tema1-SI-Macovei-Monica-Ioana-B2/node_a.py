from Crypto.Cipher import AES
import socket
import random
import time
from settings import K3,Q
from CBC import CBC
from OFB import OFB


def client_key_manager(mode):
    host = socket.gethostname() 
    port = 5000 

    client_socket = socket.socket() 
    client_socket.connect((host, port))  
    
    client_socket.send(mode.encode())  
    encrypted_key = client_socket.recv(16)  #primesc cheia criptata
    encrypted_IV = client_socket.recv(16)   #primesc IV criptat

    aes = AES.new(K3, AES.MODE_ECB)
    key = aes.decrypt(encrypted_key) 

    IV = aes.decrypt(encrypted_IV)

    client_socket.close() 
    return key.decode(), IV.decode(), encrypted_key, encrypted_IV

def client_node_b(mode, key, IV, encrypted_key, encrypted_IV):
    host = socket.gethostname() 
    port = 5001 

    client_socket = socket.socket() 
    client_socket.connect((host, port))  

    client_socket.send(mode.encode()) 
    client_socket.send(encrypted_key)  
    client_socket.send(encrypted_IV)  
    
    return client_socket
  
def random_mode():
    return random.choice(["CBC","OFB"])

if __name__ == '__main__':
    mode = random_mode()
    key, IV, encrypted_key, encrypted_IV = client_key_manager(mode)
    
    client_socket = client_node_b(mode, key, IV, encrypted_key, encrypted_IV)

    with open("node_B.py","rb") as file:
        mesaj = file.read()
        if mode == 'CBC':
            mode_type = CBC(IV)
        else:
            mode_type = OFB(IV)
        
        mesaj = mode_type.add_padding(mesaj) #adaug padding ca lung. msj. sa fie divizibila cu 16
        mesaje = mode_type.split_text(mesaj) #impart mesaj in mai multe texte de 16 caractere

        k=0
        for m in mesaje:
            if k==Q:
                k=0
                print("Resetting key, new mode: ", mode)
                key, IV, encrypted_key, encrypted_IV = client_key_manager(mode)
                mode = random_mode()
                if mode == 'CBC':
                    mode_type = CBC(IV)
                else:
                    mode_type = OFB(IV)
                client_socket.close()
                client_socket = client_node_b(mode, key, IV, encrypted_key, encrypted_IV)
            k += 1
            encrypted = mode_type.encrypt(m, key)
            client_socket.send(encrypted)
    client_socket.close()  
