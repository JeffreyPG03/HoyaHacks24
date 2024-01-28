import numpy as np
import src.des.tables as tb
import math
import src.des.keys as k


def message_to_binary(message_str):
    message_bin = ''.join(format(ord(i), '08b') for i in message_str)
    delimiter = '0000110100010001'
    message_bin = message_bin + delimiter

    return message_bin


def break_into_blocks(message):
    length = len(message)
    num_blocks = math.ceil(length / 64)
    ctr = 0

    blocks_arr = [None] * num_blocks

    for i in range(0, num_blocks):
        if (ctr + 64) <= length:
            blocks_arr[i] = message[ctr:ctr+64]
            ctr += 64
        else:
            blocks_arr[i] = message[ctr:length]
            # exec(f'm{i} = m[ctr:length]')
            leftover = ctr + 64 - length
            blocks_arr[i] = blocks_arr[i] + '0' * leftover

    return blocks_arr


def xor(first, second):
    out = ''

    for i in range(0, len(first)):
        if first[i:i + 1] == second[i:i + 1]:
            out = out + '0'
        else:
            out = out + '1'

    return out


def feistel_func_simple(k_n, r_n_1):
    k_short = k_n[0:32]
    temp = xor(k_short, r_n_1)

    out_arr = [None] * 32
    counter = 0

    for spot in tb.p:
        out_arr[counter] = int(temp[spot - 1])
        counter += 1

    out_str = ''.join(str(out_arr[i]) for i in range(0, 32))

    return out_str


def make_lr_16(l0_str, r0_str, key_arr):

    # Step 1: initialize lr_arr and update first element to have l0_str and r0_str
    lr_arr = [[() for _ in range(2)] for _ in range(17)]
    lr_arr[0][0] = l0_str
    lr_arr[0][1] = r0_str

    # Step 2: update (L1, R1) -- (L16, R16)
    for i in range(1, 17):
        lr_arr[i][0] = lr_arr[i-1][1]
        half_r_str = feistel_func_simple(key_arr[i-1], lr_arr[i-1][1])
        lr_arr[i][1] = xor(lr_arr[i-1][0], half_r_str)

    # Step 3: output l16_str and r16_str
    out_arr = [lr_arr[16][0], lr_arr[16][1]]
    return out_arr


def binary_to_string(s):
    return ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) // 8))


def encr(message_bin, key_arr, last):
    # Step 1: permute M according to IP table
    ip_arr = [None] * 64
    ctr = 0

    for spot in tb.ip:
        ip_arr[ctr] = int(message_bin[spot - 1])
        ctr += 1

    # Step 2: create L0, R0
    l0_str = ''.join(str(ip_arr[i]) for i in range(0, 32))
    r0_str = ''.join(str(ip_arr[i]) for i in range(32, 64))

    # Step 3: get L16, R16
    l16_str, r16_str = make_lr_16(l0_str, r0_str, key_arr)

    # Step 4: concatenate R16 with L16
    encr_before = r16_str + l16_str

    # Step 5:  permute encr_before according to ip_inv)
    encr_arr = [None] * 64
    ctr = 0

    for spot in tb.ip_inv:
        encr_arr[ctr] = int(encr_before[spot - 1])
        ctr += 1

    encr_bin_str = ''.join(str(encr_arr[i]) for i in range(0, 64))

    # Step 6: check if last block
    # if last:
    #     index = encr_bin_str.find('0000110100001010')
    #     encr_bin_str = encr_bin_str[0:index]

    # Step 7: turn encrypted message into text
    encr_str = binary_to_string(encr_bin_str)

    # Step 8: return
    return encr_str

def des_enc(message):
    # Step 1: get 16 keys
    key_arr = k.make_keys()

    # Step 2: convert message into binary
    message_bin = message_to_binary(message)

    # Step 3: divide binary message into 64-bit blocks
    message_blocks_arr = break_into_blocks(message_bin)

    # Step 4: encrypt each 64-bit block
    encrypted_message = ''
    counter = 0
    length = len(message_blocks_arr)
    for block in message_blocks_arr:
        if counter != (length - 1):
            encrypted_message = encrypted_message + encr(block, key_arr, False)
            counter += 1
        else:
            encrypted_message = encrypted_message + encr(block, key_arr, True)

    # Step 5: return
    return repr(encrypted_message)

