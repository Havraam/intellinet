import random

def create_AES_key():
    aea_key = "Supercalifragilisticexpialidocious"
    aes_key = ""
    for i in range(14):
        num = random.randint(0,33)
        aes_key+=(aea_key[num])
    print (aes_key)

create_AES_key()