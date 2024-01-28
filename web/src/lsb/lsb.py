import numpy as np
from PIL import Image

def lsb_encode(src, msg, dest):
    
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    msg += "#END#"
    b_message = ''.join([format(ord(i), "08b") for i in msg])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
        return False
    
    index=0
    for p in range(total_pixels):
        for q in range(0, 3):
            if index < req_pixels:
                array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                index += 1

    array=array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(dest)



def lsb_decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    b_message = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            b_message += (bin(array[p][q])[2:][-1])

    b_message = [b_message[i: i+8] for i in range(0, len(b_message), 8)]

    msg = ""
    for i in range(len(b_message)):
        if msg[-5:] == "#END#":
            break
        else:
            msg += chr(int(b_message[i], 2))
    if "#END#" in msg:
        unencrupted = msg[:-5]
        return unencrupted
    else:
        print("No hidden message found")

# def Stego():
#     print("--Welcome to $t3g0--")
#     print("1: Encode")
#     print("2: Decode")

#     func = input()

#     if func == '1':
#         print("Enter Source Image Path")
#         src = input()
#         print("Enter Message to Hide")
#         message = input()
#         print("Enter Destination Image Path")
#         dest = input()
#         print("Encoding...")
#         lsb_encode(src, message, dest)

#     elif func == '2':
#         print("Enter Source Image Path")
#         src = input()
#         print("Decoding...")
#         lsb_decode(src)

#     else:
#         print("ERROR: Invalid option chosen")