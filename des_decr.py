import tables as tb
import keys as k
import math


def message_to_binary(message_str):
    message_bin = ''.join(format(ord(i), '08b') for i in message_str)
    return message_bin


def binary_to_string(s):
    return ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) // 8))


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


def rev_xor(key, ans):
    inp = ''

    for i in range(0, len(key)):
        if ans[i] == '0':
            inp = inp + key[i]
        else:
            if key[i] == '0':
                inp = inp + '1'
            else:
                inp = inp + '0'

    return inp


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

def rev_lr_16(l16_str, r16_str, key_arr):
    # Step 1: initialize lr_arr and update first element to have l16_str and r16_str
    lr_arr = [[() for _ in range(2)] for _ in range(17)]
    lr_arr[16][0] = l16_str
    lr_arr[16][1] = r16_str

    # Step 2: update (L1, R1) -- (L16, R16)
    for i in reversed(range(0, 16)):
        lr_arr[i][1] = lr_arr[i+1][0]
        half_l_str = feistel_func_simple(key_arr[i], lr_arr[i][1])
        lr_arr[i][0] = rev_xor(half_l_str, lr_arr[i+1][1])

    first_arr = [lr_arr[0][0], lr_arr[0][1]]
    return first_arr


def decrypt(encr_str, key_arr, last):
    # Step 1: un-permute encr_bin according to ip-inv table
    ip_inv_arr = [None] * 64
    ctr = 0

    for spot in tb.ip_inv:
        ip_inv_arr[spot - 1] = encr_str[ctr]
        ctr += 1

    # Step 2: find R16, L16
    r16_str = ''.join(str(ip_inv_arr[i]) for i in range(0, 32))
    l16_str = ''.join(str(ip_inv_arr[i]) for i in range(32, 64))

    rev_last_steps_decr = l16_str + r16_str

    # Step 3: find L0, R0
    l0_str, r0_str = rev_lr_16(l16_str, r16_str, key_arr)

    # Step 4: make permuted message
    perm_message = l0_str + r0_str

    # Step 5: un-permute message
    unperm_message_arr = [None] * 64
    ctr = 0

    for spot in tb.ip:
        unperm_message_arr[spot - 1] = perm_message[ctr]
        ctr += 1

    unperm_message = ''.join(str(unperm_message_arr[i]) for i in range(0, 64))

    # Step 6: drop delimiter + extra 0 if last block
    if last:
        index = unperm_message.find('0000110100010001')
        unperm_message = unperm_message[0:index]

    return unperm_message



def main(encr_str):
    # Step 1: make keys
    key_arr = k.make_keys()

    # Step 2: convert encrypted message in binary
    encr_bin = message_to_binary(encr_str)

    # Step 3: divide binary message into 64-bit blocks
    message_blocks_arr = break_into_blocks(encr_bin)

    # Step 4: decrypt each 64-bit block
    decrypted_message = ''
    counter = 0
    length = len(message_blocks_arr)
    for block in message_blocks_arr:
        if counter != (length - 1):
            decrypted_message = decrypted_message + decrypt(block, key_arr, False)
            counter += 1
        else:
            decrypted_message = decrypted_message + decrypt(block, key_arr, True)

    # Step 5: return
    decrypted_message_text = binary_to_string(decrypted_message)
    print(decrypted_message_text)
    return decrypted_message_text
