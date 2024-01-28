import tables as tb

#defining key
k_hex = "133457799BBCDFF1"
k = 0b0001001100110100010101110111100110011011101111001101111111110001
k_str = "0001001100110100010101110111100110011011101111001101111111110001"


def left_rotate(bin_as_str, shift):
    shifted_dig = bin_as_str[0:shift]
    bin_as_str = bin_as_str[shift:] + shifted_dig
    return bin_as_str


def permute_key():
    k_plus_arr = [None] * 56
    ctr = 0

    for spot in tb.pc_1:
        k_plus_arr[ctr] = int(k_str[spot - 1])
        ctr += 1

    return k_plus_arr


def make_keys():
    # Step 1: permute k according to pc_1
    k_plus_arr = permute_key()

    # Step 2: create C0, D0
    c0_str = ''.join(str(k_plus_arr[i]) for i in range(0, 28))
    d0_str = ''.join(str(k_plus_arr[i]) for i in range(28, 56))

    # Step 3: create (C1, D1), ..., (C16, D16)
    # c1_str, c2_str, c3_str, c4_str, c5_str, c6_str, c7_str, c8_str, c9_str, c10_str, c11_str, c12_str, c13_str, c14_str, \
    #     c15_str, c16_str = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    #
    # d1_str, d2_str, d3_str, d4_str, d5_str, d6_str, d7_str, d8_str, d9_str, d10_str, d11_str, d12_str, d13_str, d14_str, \
    #     d15_str, d16_str = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    # for i in range(1, 17):
    #     exec(f'c{i}_str = left_rotate(c{i - 1}_str, tb.num_left_shifts[{i - 1}])')
    #     exec(f'd{i}_str = left_rotate(d{i - 1}_str, tb.num_left_shifts[{i - 1}])')

    # Step 3: Update (C1, D1), ..., (C16, D16)

    cd_array = [[() for _ in range(2)] for _ in range(17)]
    cd_array[0][0] = c0_str
    cd_array[0][1] = d0_str

    for i in range(1, 17):
        cd_array[i][0] = left_rotate(cd_array[i-1][0], tb.num_left_shifts[i-1])
        cd_array[i][1] = left_rotate(cd_array[i - 1][1], tb.num_left_shifts[i - 1])

    print(cd_array[16][1])

    # Step 5: create K1-K16
    keys_bef_arr = [None] * 16

    for i in range(0, 16):
        keys_bef_arr[i] = cd_array[i+1][0] + cd_array[i+1][1]

    # k1_str_before, k2_str_before, k3_str_before, k4_str_before, k5_str_before, k6_str_before, k7_str_before, \
    #     k8_str_before, k9_str_before, k10_str_before, k11_str_before, k12_str_before, k13_str_before, k14_str_before, \
    #     k15_str_before, k16_str_before = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    #
    # for i in range(1, 17):
    #     exec(f'k{i}_str_before = c{i}_str + d{i}_str')

    # Step 6: Permute K1-K16
    # k1_str_arr, k2_str_arr, k3_str_arr, k4_str_arr, k5_str_arr, k6_str_arr, k7_str_arr, k8_str_arr, k9_str_arr, \
    #     k10_str_arr, k11_str_arr, k12_str_arr, k13_str_arr, k14_str_arr, k15_str_arr, k16_str_arr = \
    #     [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, \
    #     [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48, [None] * 48
    # exec(f'k{i}_str_arr[ctr] = k{i}_str_before[spot - 1]')

    ctr = 0
    keys_perm_arr = [[() for _ in range(48)] for _ in range(16)]

    for spot in tb.pc_2:
        for i in range(0, 16):
            keys_perm_arr[i][ctr] = keys_bef_arr[i][spot-1:spot]
        ctr += 1

    # Step 7: Convert K1-K16 into strings
    # k1_str, k2_str, k3_str, k4_str, k5_str, k6_str, k7_str, k8_str, k9_str, k10_str, k11_str, k12_str, k13_str, \
    #     k14_str, k15_str, k16_str = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    # exec(f'k{i}_str = k{i}_str.join(str(k{i}_str_arr[j]) for j in range(0, 48))')

    keys_str_arr = [None] * 16

    for i in range(0, 16):
        keys_str_arr[i] = ''.join(str(keys_perm_arr[i][j]) for j in range(0, 48))

    return keys_str_arr