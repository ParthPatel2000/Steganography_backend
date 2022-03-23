from PIL import Image
import numpy as np
import encryption
import config_loader

# Decryption happens here
def secret2txt(encrypted_text):
    # print("\nFrom secret 2 text\n")
    key = str(config_loader.read('''data['key']'''))
    try:
        decrypted_data = encryption.decrypt(encrypted_text, key)
    except ValueError:
        _ = "Invalid key"
        return _, 2
    # print(decrypted_data)
    try:
        encoded = decrypted_data.decode()
        return encoded, 1
    except UnicodeDecodeError:
        # print("wrong key")
        _ = "wrong key"
        return _, 0


def bin2byte(binary_string):
    # print('\n from bin 2 byte\n')
    bytestring = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    # print(type(bytestring))
    # print(bytestring)             # troubleshooting lines
    return bytestring


def bin2txt(string):
    text = ""
    while string:
        byte = string[:8]
        ascii = int(byte, 2)
        text += chr(ascii)
        string = string[8:]
    return text


def to_8bit(data):
    data = bin(data)[2:]
    while len(data) < 8:
        data = '0' + data
    return data


def length_extract(data):
    length = ''
    for i in range(width):
        x = 0
        length += to_8bit(data[x][i][0])[-3:]
        length += to_8bit(data[x][i][1])[-3:]
        length += to_8bit(data[x][i][2])[-2:]

    # print('extracted length ', length)             # troubleshooting lines
    temp= bin2txt(length)
    # print('Text',temp)             # troubleshooting lines
    length = temp.split('<l>')[1]
    length = (int(length) )
    # print('binary string length',length)              # troubleshooting lines                  # Length of the bytestring
    return length


# photo = Image.open(r"D:\College\PYTHON PROGRAMS\Steagnography\received_images\2021_08_10-05-53_06.PNG")
photo = Image.open(config_loader.read('''data['environment']['receive_path']'''))
data = np.asarray(photo)
width, height = photo.size

secret = ''
secretlength = length_extract(data)

count = 0
for x in range(1, height):
    for y in range(width):
        if count < secretlength:
            secret += to_8bit(data[x][y][0])[-2:]
            count += 2
            if count == secretlength:
                break
            secret += to_8bit(data[x][y][1])[-2:]
            count += 2
            if count == secretlength:
                break
            secret += to_8bit(data[x][y][2])[-1:]
            count += 1
            if count == secretlength:
                break
# print('total ',count)             # troubleshooting lines

if(secretlength != count):
    extrabits= count - secretlength
    # print('extrabits',extrabits)             # troubleshooting lines
    secret= secret[0:-extrabits]
    # print('adjusted strlen',len(secret))             # troubleshooting lines
# print(secret)
enc_text = bin2byte(secret)
# print(enc_text)
message, return_code = secret2txt(enc_text)


# print("Extracted message is:",message)

with open("../Received Data/recieved.txt", "w+") as file:
    file.writelines(message)
print(return_code)
