import cv2
import pywt
import numpy as np

def text_to_array(text):
    array = []
    index = -1
    with open(text, 'r') as input:
        for rows in input:
            a = ''
            b = ''
            vals = rows.split()
            if vals[0] == '[':
                vals = vals[1:]
                a = vals[0]
            elif rows[0] == '[':
                array.append([])
                index += 1
                a = vals[0][2:]
            else:
                a = vals[0][1:]
            b = vals[1][:-1]
            array[index].append([float(a), float(b)])
    return array

def watermark(A, B, dest, key_dest):

    # Read the host image
    host = cv2.imread(A)
    m, n, p = host.shape

    # Perform DWT on the host image using Haar wavelet
    coeffs_host = pywt.dwt2(host, 'haar')
    host_LL, (host_LH, host_HL, host_HH) = coeffs_host

    # Read and resize the watermark image
    water_mark = cv2.imread(B)
    water_mark = cv2.resize(water_mark, (n, m))

    # Perform DWT on the watermark image using Haar wavelet
    coeffs_water_mark = pywt.dwt2(water_mark, 'haar')
    water_mark_LL, (water_mark_LH, water_mark_HL, water_mark_HH) = coeffs_water_mark

    # Watermark the host image
    watermarked_LL = host_LL + (0.03 * water_mark_LL)
    watermarked = pywt.idwt2((watermarked_LL, (host_LH, host_HL, host_HH)), 'haar')

    # Save the watermarked image
    cv2.imwrite(dest, np.uint8(watermarked))
    np.set_printoptions(threshold=np.inf)
    with open(key_dest, 'w') as output:
        for row in host_LL:
            output.write(str(row) + '\n')

def ext_watermark(A, B, C):

    wm = cv2.imread(A)

    coeffs_wm = pywt.dwt2(wm, 'haar')
    wm_LL, (wm_LH, wm_HL, wm_HH) = coeffs_wm

    host_LL = text_to_array(B)
    host_LL = np.array(host_LL)

    extracted_watermark = (wm_LL - host_LL) / 0.03

    ext = pywt.idwt2((extracted_watermark, (wm_LH, wm_HL, wm_HH)), 'haar')

    cv2.imwrite(C, np.uint8(ext))
