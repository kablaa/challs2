import sys
flag = "flag{g0ood_Y0U_No_YoRe_oPc0deS}"
to_enc = "i_did_you_a_hekkin_bamboozle_ " + flag
key = "LOL-ITS-A-KEY"
#add -> sub
#xor -> xor
#sub -> add
result = ""
encrypted_byte = 0
for i in range(0,len(to_enc)):
    k = i%len(key)
    j = k%3
    if j == 0:
        #add
        encrypted_byte = ord(to_enc[i]) + ord(key[k])
        # print str(i) +  ": " +to_enc[i]+ " - " + key[k]+  " = " +hex(encrypted_byte)

    elif j == 1:
        #xor
        encrypted_byte = ord(to_enc[i]) ^ ord(key[k])
        # print str(i) + ": " +to_enc[i]+" ^ "+ key[k]+  " = " +hex(encrypted_byte)

    elif j == 2:
        #sub
        encrypted_byte = ord(to_enc[i]) - ord(key[k])
        # print str(i) + ": " +to_enc[i]+" + " + key[k]+ " = " + hex(encrypted_byte)
    result += chr(encrypted_byte)

if len(sys.argv) > 1:
    if sys.argv[1] == "sol":
        print to_enc
else:
    b = ""
    for c in result:
        b += hex(ord(c)) + ','
    print b
