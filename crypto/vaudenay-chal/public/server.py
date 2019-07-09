 
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto import Random
import struct
import socket

aes_key = b"****************"
mac_key = b"****************"
secret  = b"flag{*************************************}"

BS = 16

def listen():
    TCP_IP = "127.0.0.1"
    TCP_PORT = 9090
    BUFFER_SIZE = 1024
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    
    print("Listening on {}:{}...".format(TCP_IP, TCP_PORT))
    conn = None
    try:
        while True:
            conn, addr = s.accept()

            # Read ciphertext from user
            ciphertext = conn.recv(BUFFER_SIZE)
            if ciphertext:
                # Decrypt ciphertext
                try:
                    decrypted = decrypt(ciphertext)

                    # Check MAC
                    plaintext, tag = decrypted[:-16], decrypted[-16:]
                    if not tag == mac(plaintext):
                        raise Exception("MacError")

                    # Send decrypted plaintext
                    conn.send("OK")
                except Exception as e:
                    conn.send(str(e))
            conn.close()
    except KeyboardInterrupt:
        pass
    finally:
        if conn:
            conn.close()

def pad(s):
    """ PKCS#5 padding """
    c = 16 - (len(s) % 16)  # Char to pad by
    while len(s) % 16 != 0:
        s += chr(c)
    return s

def unpad(s):
    """ PKCS#5 unpadding """
    c = ord(s[-1])  # Get last char

    # Verify pad
    for b in s[-c:]:
        if ord(b) != c:
            raise Exception("PaddingError")
    return s[:len(s)-c]

def mac(s):
    """ Generate a mac """
    h = HMAC.new(mac_key)
    h.update(s)
    return h.digest()

def encrypt(plaintext):
    """
    Returns hex encoded encrypted value!
    """
    # Pad plaintext
    plaintext = pad(plaintext)

    # AES encrypt
    iv = Random.new().read(BS)
    aes = AES.new(aes_key, AES.MODE_CBC, iv)
    return iv + aes.encrypt(plaintext)

def decrypt(ciphertext):
    """
    Requires hex encoded param to decrypt
    """
    # AES decrypt
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    aes = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(ciphertext))

def generate_message():
    f = open("secret.txt", "wb")
    f.write(encrypt(secret))
    f.close()

if __name__ == "__main__":
    #generate_message()
    listen()
