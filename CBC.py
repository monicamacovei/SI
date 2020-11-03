from Crypto.Cipher import AES
import random
class CBC:
    def __init__(self, IV):
        self.IV = IV
        self.IV_dec = IV
    
    def xor(self, a, b):
        result = []
        for x,y in zip(a,b):
            ord_x = 0
            if isinstance(x, int): #error: ord() expected string of length 1, but int found
                ord_x = x
            else:
                ord_x = ord(x) #numarul reprezentat de caracter in ASCII
            
            ord_y = 0
            if isinstance(y, int):
                ord_y = y
            else:
                ord_y = ord(y)
            result.append( chr(ord_x ^ ord_y)) #X XOR Y transformat din cod in caracter
        return "".join(result) #transformam din lista in string

    def encrypt(self, plaintext,key):
        cipher_text = self.xor(plaintext, self.IV) 
        aes = AES.new(key, AES.MODE_ECB) #initializam aes cu mod ECB
       
        cipher_text = aes.encrypt(cipher_text.encode("latin-1")) #am folosit latin-1 pentru ca uft-8 dadea eroare
        self.IV = cipher_text 
        return cipher_text

    def decrypt(self,cipher_text, key):
        aes = AES.new(key, AES.MODE_ECB)
        new_cipher_text = aes.decrypt(cipher_text)
        plaintext = self.xor(new_cipher_text.decode("latin-1"), self.IV_dec) 
        self.IV_dec = cipher_text
        return plaintext

    def add_padding(self, plaintext):
        to_add = 16-len(plaintext)%16
        if to_add == 16:
            return plaintext
        return plaintext + (" "*to_add).encode() #adaugam spatiu pentru ca plaintext-ul sa fie divizibil cu 16

    def split_text(self, plaintext):
        split_plaintext = []
        for i in range(0, len(plaintext),16): #de la 0 pana la len(plaintext) din 16 in 16
            split_plaintext.append(plaintext[i:i+16]) #luam doar textul de la pozitia i pana la i+16
        return split_plaintext
    
    def remove_padding(self, plaintext, to_remove):
        return plaintext[:-to_remove]