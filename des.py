import numpy as np
import tables as tb
import math
import keys as k


def message_to_binary(message_str):
    message_bin = ''.join(format(ord(i), '08b') for i in message_str)
    delimiter = '0000110100001010'
    message_bin = message_bin + delimiter

    return message_bin


def break_into_blocks(message):
    m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, \
        m25, m26, m27, m28, m29, m30, m31, m32, m33, m34, m35, m36, m37, m38, m39, m40, m41, m42, m43, m44, m45, m46, \
        m47, m48, m49, m50, m51, m52, m53, m54, m55, m56, m57, m58, m59, m60, m61, m62, m63, m64, m65, m66, m67, m68, \
        m69, m70, m71, m72, m73, m74, m75, m76, m77, m78, m79, m80, m81, m82, m83, m84, m85, m86, m87, m88, m89, m90, \
        m91, m92, m93, m94, m95, m96, m97, m98, m99, m100 = \
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', \
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',\
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',\
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''

    length = len(message) + 16
    num_blocks = math.ceil(length / 64)
    ctr = 0

    for i in range(1, num_blocks + 1):
        if ctr <= (length + 64):
            exec(f'm{i} = m[ctr:ctr+64]')
            ctr += 64
        else:
            exec(f'm{i} = m[ctr:length]')
            leftover = ctr + 64 - length
            exec(f'm{i} = m{i}.join(str(0) for i in range(0, leftover))')

    blocks_arr = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22,
                 m23, m24, m25, m26, m27, m28, m29, m30, m31, m32, m33, m34, m35, m36, m37, m38, m39, m40, m41, m42,
                 m43, m44, m45, m46, m47, m48, m49, m50, m51, m52, m53, m54, m55, m56, m57, m58, m59, m60, m61, m62,
                 m63, m64, m65, m66, m67, m68, m69, m70, m71, m72, m73, m74, m75, m76, m77, m78, m79, m80, m81, m82,
                 m83, m84, m85, m86, m87, m88, m89, m90, m91, m92, m93, m94, m95, m96, m97, m98, m99, m100]
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
    # Step 1: extract keys from key array
    k1_str, k2_str, k3_str, k4_str, k5_str, k6_str, k7_str, k8_str, k9_str, k10_str, k11_str, k12_str, k13_str, \
        k14_str, k15_str, k16_str = key_arr

    # Step 2: make (L1, R1), ... , (L16, R16)
    l1_str = r0_str
    r1_str_half = feistel_func_simple(k1_str, r0_str)
    r1_str = xor(l0_str, r1_str_half)

    l2_str = r1_str
    r2_str_half = feistel_func_simple(k2_str, r1_str)
    r2_str = xor(l1_str, r2_str_half)

    l3_str = r2_str
    r3_str_half = feistel_func_simple(k3_str, r2_str)
    r3_str = xor(l2_str, r3_str_half)

    l4_str = r3_str
    r4_str_half = feistel_func_simple(k4_str, r3_str)
    r4_str = xor(l3_str, r4_str_half)

    l5_str = r4_str
    r5_str_half = feistel_func_simple(k5_str, r4_str)
    r5_str = xor(l4_str, r5_str_half)

    l6_str = r5_str
    r6_str_half = feistel_func_simple(k6_str, r5_str)
    r6_str = xor(l5_str, r6_str_half)

    l7_str = r6_str
    r7_str_half = feistel_func_simple(k7_str, r6_str)
    r7_str = xor(l6_str, r7_str_half)

    l8_str = r7_str
    r8_str_half = feistel_func_simple(k8_str, r7_str)
    r8_str = xor(l7_str, r8_str_half)

    l9_str = r8_str
    r9_str_half = feistel_func_simple(k9_str, r8_str)
    r9_str = xor(l8_str, r9_str_half)

    l10_str = r9_str
    r10_str_half = feistel_func_simple(k10_str, r9_str)
    r10_str = xor(l9_str, r10_str_half)

    l11_str = r10_str
    r11_str_half = feistel_func_simple(k11_str, r10_str)
    r11_str = xor(l10_str, r11_str_half)

    l12_str = r11_str
    r12_str_half = feistel_func_simple(k12_str, r11_str)
    r12_str = xor(l11_str, r12_str_half)

    l13_str = r12_str
    r13_str_half = feistel_func_simple(k13_str, r12_str)
    r13_str = xor(l12_str, r13_str_half)

    l14_str = r13_str
    r14_str_half = feistel_func_simple(k14_str, r13_str)
    r14_str = xor(l13_str, r14_str_half)

    l15_str = r14_str
    r15_str_half = feistel_func_simple(k15_str, r14_str)
    r15_str = xor(l14_str, r15_str_half)

    l16_str = r15_str
    r16_str_half = feistel_func_simple(k16_str, r15_str)
    r16_str = xor(l15_str, r16_str_half)

    # if time:
    # l1_str, l2_str, l3_str, l4_str, l5_str, l6_str, l7_str, l8_str, l9_str, l10_str, l11_str, l12_str, l13_str, l14_str, \
    #     l15_str, l16_str = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    #
    # r1_str, r2_str, r3_str, r4_str, r5_str, r6_str, r7_str, r8_str, r9_str, r10_str, r11_str, r12_str, r13_str, r14_str, \
    #     r15_str, r16_str = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    # update variables dynamically
    # for i in range(2, 17):
    #     exec(f'l{i}_str = r{i - 1}_str')
    #     exec(f'r{i}_str_half = feistel_func_simple(k{i}_str, r{i - 1}_str)')
    #     exec(f'r{i}_str = xor(l{i - 1}_str, r{i}_str_half)')

    # Step 3: output l16_str and r16_str

    out_arr = [l16_str, r16_str]
    return out_arr


def binary_to_string(s):
    return ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) // 8))


def encr(message_bin, key_arr, last):
    # Step 1: extract keys from key array
    k1_str, k2_str, k3_str, k4_str, k5_str, k6_str, k7_str, k8_str, k9_str, k10_str, k11_str, k12_str, k13_str, \
        k14_str, k15_str, k16_str = key_arr

    # Step 2: permute M according to IP table
    ip_arr = [None] * 64
    ctr = 0

    for spot in tb.ip:
        ip_arr[ctr] = int(message_bin[spot - 1])
        ctr += 1

    # Step 3: create L0, R0
    l0_str = ''.join(str(ip_arr[i]) for i in range(0, 32))
    r0_str = ''.join(str(ip_arr[i]) for i in range(32, 64))

    # Step 4: get L16, R16
    l16_str, r16_str = make_lr_16(l0_str, r0_str, key_arr)

    # Step 5: concatenate R16 with L16
    encr_before = r16_str + l16_str

    # Step 6:  permute encr_before according to ip_inv)
    encr_arr = [None] * 64
    ctr = 0

    for spot in tb.ip_inv:
        encr_arr[ctr] = int(encr_before[spot - 1])
        ctr += 1

    encr_bin_str = ''.join(str(encr_arr[i]) for i in range(0, 64))

    # Step 6: check if last block
    if last:
        index = encr_bin_str.find('0000110100001010')
        encr_bin_str = encr_bin_str[0:index]

    # Step 7: turn encrypted message into text
    encr_str = binary_to_string(encr_bin_str)

    # Step 8: return
    return encr_str


def main(message):
    # Step 1: get 16 keys
    key_arr = k.make_keys()

    # Step 2: convert message into binary
    message_bin = message_to_binary(message)

    # Step 3: divide binary message into 64-bit blocks
    message_blocks_arr = break_into_blocks(message_bin)

    # Step 4: encrypt each 64-bit block
    encrypted_message = ''
    counter = 0;
    length = len(message_blocks_arr)
    for block in message_blocks_arr:
        if counter != (length - 1):
            encrypted_message = encrypted_message + encr(block, key_arr, False)
            counter += 1
        else:
            encrypted_message = encrypted_message + encr(block, key_arr, True)

    # Step 5: return
    return encrypted_message

print(main('hello'))

#
# # overriding for testing purposes
# mess = '0000000100100011010001010110011110001001101010111100110111101111'
#
# encr_str_bin = encr(mess)
#
# encr_str = decode_binary_string(encr_str_bin)
#
# print(encr_str)
