import blowfish
from operator import xor
import time
import config_loader


def make_bytes(plaintext):
    plaintext = plaintext.encode()
    encoded_text = bytearray(plaintext)
    return encoded_text


def encrypt(plaintext, secret_key):
    start = time.time()
    plaintext = make_bytes(plaintext)
    secret_key = make_bytes(secret_key)

    key = blowfish.Cipher(secret_key)
    nounce = int.from_bytes(b"9867", "big")
    enc_counter = blowfish.ctr_counter(nounce, f=xor)
    data_encrypted = b"".join(key.encrypt_ctr(plaintext, enc_counter))
    # print("encryption in ", time.time()-start)
    # print(data_encrypted)             # troubleshooting lines
    return data_encrypted


def decrypt(encrypted_data, secret_key):
    # print(encrypted_data)             # troubleshooting lines
    secret_key = make_bytes(secret_key)
    key = blowfish.Cipher(secret_key)

    nounce = int.from_bytes(b"9867", "big")
    dec_counter = blowfish.ctr_counter(nounce, f=xor)
    data_decrypted = b"".join(key.decrypt_ctr(encrypted_data, dec_counter))

    return data_decrypted


if __name__ == '__main__':
    print(key)

