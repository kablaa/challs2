from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto import Random
import struct

aes_key     = b"XZEXLzUe4Hic2P0I"
mac_key = b"DJY/un3VbZ2GzUp0"

BS = 16

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
            raise Exception("Padding error!")
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

def check(ciphertext):
    try:
        decrypted = decrypt(ciphertext)
        plaintext, tag = decrypted[:-16], decrypted[-16:]
        if not tag == mac(plaintext):
            return "MacError"
        else:
            return "Success"
    except Exception as e:
        if str(e) == "Padding error!":
            return "PaddingError"

def pretty_print(xs):
    s = ""
    for i, x in enumerate(xs):
        s += hex(ord(x)) + " "
        if (i + 1) % 16 == 0:
            s += " | "
    print("=" * 10)
    print(s)
    print("=" * 10)

if __name__ == "__main__":
    # SERVERSIDE
    plaintext = b"SUPER SECRET"
    x = plaintext + mac(plaintext)
    ciphertext = encrypt(x)

    # CLIENTSIDE
    P = ""

    # Loop over all blocks
    for _ in range(len(ciphertext) / BS - 1):
        bs = []
        # Iterate possible bytes
        for i in range(BS):
            R_idx = -17-i
            C_i = ciphertext[R_idx]
            # Prepare ciphertext_ for vaudenay attack
            ciphertext_ = ciphertext[:]
            for j in range(i):
                j_idx = -17-j
                ciphertext_ = ciphertext_[:j_idx] + chr(bs[j] ^ (j+1) ^ (i+1)) + ciphertext_[j_idx+1:]

            decrypted = False
            for b in range(256):
                if b == ord(C_i) and i == 0:
                    # Unmodified ciphertext decrypts and is a false positive
                    continue
                # Set C[R_idx] = b
                ciphertext_ = ciphertext_[:R_idx] + chr(b) + ciphertext_[R_idx+1:]
                #import pdb; pdb.set_trace()

                res = check(ciphertext_)  # Check if this ciphertext decrypts
                if res == "PaddingError":
                    continue
                elif res in ("MacError", "Success"):
                    # Plaintext byte decrypted
                    P_i = chr(b ^ (i+1) ^ ord(C_i))
                    P = P_i + P
                    bs.append(b)
                    decrypted = True
                    break
            if not decrypted:
                raise Exception("Could not decrypt byte")

        ciphertext = ciphertext[:-16]
    print(P)
