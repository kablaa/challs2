from pwn import *

BS = 16

def check(ciphertext):
    # Send to server to decrypt
    proc = remote("127.0.0.1", 9090)
    proc.send(ciphertext)
    output = proc.recv()
    proc.close()
    return output

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
    with open("secret.txt", "rb") as f:
        ciphertext = f.read()

    # Current plaintext
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

                res = check(ciphertext_)  # Check if this ciphertext decrypts
                if res == "PaddingError":
                    continue
                elif res in ("MacError", "OK"):
                    # Plaintext byte decrypted
                    P_i = chr(b ^ (i+1) ^ ord(C_i))
                    P = P_i + P
                    bs.append(b)
                    decrypted = True
                    break
                else:
                    raise Exception("Unexpected response")
            if not decrypted:
                raise Exception("Could not decrypt byte")

        ciphertext = ciphertext[:-16]

    # Print final plaintext
    print(P)
