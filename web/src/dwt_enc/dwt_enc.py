import cv2
import pywt
import numpy as np

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def binary_to_text(binary_message):
    text = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])
    return text

def dwt_encode(src, msg, dest):
    # Read the host image
    host = cv2.imread(src)
    m, n, p = host.shape

    # Perform DWT on the host image using Haar wavelet
    coeffs_host = pywt.dwt2(host, 'haar')
    host_LL, (host_LH, host_HL, host_HH) = coeffs_host

    # Encode text message
    binary_msg = text_to_binary(msg)

    # Ensure the binary message can fit into the host image
    if len(binary_msg) > m * n:
        raise ValueError("Text message is too long to be hidden in the image")

    # Convert binary message to an array of integers
    binary_array = np.array(list(binary_msg), dtype=int)

    # Ensure the binary message can fit into the host image
    if len(binary_msg) > host_LL.size:
        raise ValueError("Text message is too long to be hidden in the image")

    # Convert binary message to an array of integers
    binary_array = np.array(list(binary_msg), dtype=int)

    # Pad the binary array if necessary to match the size of host_LL
    padding_size = host_LL.size - len(binary_array)
    binary_array = np.concatenate((binary_array, np.zeros(padding_size, dtype=int)))

    # Reshape the binary array to the shape of host_LL
    binary_array = binary_array.reshape(host_LL.shape)

    # Watermark the host image
    watermarked_LL = host_LL + (0.03 * binary_array)
    watermarked = pywt.idwt2((watermarked_LL, (host_LH, host_HL, host_HH)), 'haar')

    # Save the watermarked image
    # cv2.imwrite('Watermarked_text.png', cv2.cvtColor(np.uint8(watermarked), cv2.COLOR_RGB2BGR))
    cv2.imwrite(dest, np.uint8(watermarked))

# Decode the hidden message
def dwt_decode(src, host):
    # Read the watermarked image
    watermarked = cv2.imread(src)
    original = cv2.imread(host)

    # Perform DWT on the host image using Haar wavelet
    coeffs_host = pywt.dwt2(original, 'haar')
    host_LL, (host_LH, host_HL, host_HH) = coeffs_host

    # Perform DWT on the watermarked image using Haar wavelet
    coeffs_watermarked = pywt.dwt2(watermarked, 'haar')
    watermarked_LL, _ = coeffs_watermarked

    # Extract the hidden message from the watermarked image
    decoded_binary_message = ((watermarked_LL - host_LL) / 0.03).flatten().astype(int)

    # Remove any extra elements that might have resulted from padding
    decoded_binary_message = decoded_binary_message[:len(host_LL.flatten())]

    decoded_text_message = binary_to_text(''.join(map(str, decoded_binary_message)))

    return decoded_text_message


# decoded_binary_message = (watermarked_LL - host_LL) / 0.03
# decoded_binary_message = decoded_binary_message.flatten().astype(int)
# decoded_text_message = binary_to_text(''.join(map(str, decoded_binary_message)))