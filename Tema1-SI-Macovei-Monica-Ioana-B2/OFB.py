from Crypto.Cipher import AES
import random
class OFB:
    def __init__(self,IV):
        self.IV = IV
        self.IV_dec = IV
    
    def xor(self, a, b):
        result = []
        for x,y in zip(a,b):
            ord_x = 0
            if isinstance(x, int): # ord() expected string of length 1, but int found
                ord_x = x
            else:
                ord_x = ord(x)
            
            ord_y = 0
            if isinstance(y, int):
                ord_y = y
            else:
                ord_y = ord(y)
            result.append( chr(ord_x ^ ord_y))
        return "".join(r for r in result)

    def encrypt(self, plaintext,key):
        aes = AES.new(key, AES.MODE_ECB)
        encrypted_IV = aes.encrypt(self.IV)
        cipher_text = self.xor(plaintext, encrypted_IV.decode("latin-1")) 

        self.IV = encrypted_IV
                
        return cipher_text.encode("latin-1")

    def decrypt(self,cipher_text, key):
        plaintext = ""
        aes = AES.new(key, AES.MODE_ECB)
        encrypted_IV = aes.encrypt(self.IV_dec)
        self.IV_dec = encrypted_IV
        
        plaintext = self.xor(cipher_text, encrypted_IV) 
        return plaintext

    def add_padding(self, plaintext):
        to_add = 16-len(plaintext)%16
        if to_add == 16:
            return plaintext
        return plaintext + (" "*to_add).encode()#adaugam spatiu pentru ca plaintext-ul sa fie divizibil cu 16

    def split_text(self, plaintext):
        split_plaintext = []
        for i in range(0, len(plaintext),16):
            split_plaintext.append(plaintext[i:i+16])
        return split_plaintext
    
    def remove_padding(self, plaintext, to_remove):
        return plaintext[:-to_remove]


    