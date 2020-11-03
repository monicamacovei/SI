from Crypto.Cipher import AES
import socket
import random
from settings import K3, Q
from CBC import CBC
from OFB import OFB


def start_server():
    host = socket.gethostname()
    port = 5001

    server_socket = socket.socket() 
    server_socket.bind((host, port)) 

    server_socket.listen(2)

    k = Q #incepem cu k=Q ca sa intre direct in if-ul din while pentru a nu defini acelasi cod de doua ori
    with open("received_by_nodeB.py","w") as file: 
        while True:
            if k==Q:
                
                k=0
                conn, address = server_socket.accept() 
                mode = conn.recv(3).decode()
                if not mode:
                    break

                encrypted_key = conn.recv(16) 
                encrypted_IV = conn.recv(16)  

                aes = AES.new(K3, AES.MODE_ECB)

                key = aes.decrypt(encrypted_key)
                IV = aes.decrypt(encrypted_IV)
                
                if mode == 'CBC':
                    mode_type = CBC(IV)
                else:
                    mode_type = OFB(IV)
            k += 1
            message = conn.recv(16)
            if not message:
                break
            
            plain_text = mode_type.decrypt(message, key)

            print(plain_text,end="")
            file.write(plain_text)
    conn.close() 


if __name__ == '__main__':
    start_server()
