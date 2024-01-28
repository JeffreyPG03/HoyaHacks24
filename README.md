# HoyaHacks24

## Inspiration
Cryptography takes many seemingly wild concepts and connects them in a way to come up with a use. From the study of prime numbers, to factoring problems, to elliptic curves, seemingly innocuous problems become extremely useful in the protection of information. At the same time, cybersecurity is becoming increasingly important in every digital world. I was fortunate to have had the opportunity to study some rudimentary cryptography algorithms in a number theory and cryptography class but never had the opportunity to take the theory and put it into practice. P.E.N.G.U (Private Encrypted Networking with Guaranteed Unbreakability) takes all of these fascinating questions across many fields and put them to practice use encoding information.

## What it does
P.E.N.G.U. is a web-platform that provides encryption and decryption services to users. Users have the ability to use one of our three encryption/decryption services: text encryption, text-based steganography, or image-based steganography. Text encryption refers to encrypting a plaintext message and converting it into a ciphertext message consisting of text characters. Text-based steganography involves hiding text within the pixels of an image. And, image-based steganography hides one image within another image.

## How we built it
P.E.N.G.U. uses Python to encrypt and decrypt the data. For text encryption, we used a modified version of the DES (Data Encryption Standard) algorithm. For text-based steganography, we implemented two steganography algorithms: least significant bit (LSB) and discrete wavelet transform (DWT). We utilized open libraries in python such as PyWavelets, Python OpenCV, and Pillow to implement the algorithms in combination with a plethora of independently created algorithms specifically for our website. We also implemented a modified version of the DWT for embedding watermarks into pictures.

For the front-end, we used Flask to connect the python backend with a html and css frontend. We used bootstrap to simplify the frontend development, although our front-end UI is still very rudimentary. 

## Challenges we ran into
For both text encryption and image steganography, explanations of algorithm implementation in various research papers do not go into detail or about the code of the algorithm. Rather, they all explain the algorithms and its advantages and disadvantages at a high-level, which made it more difficult to implement these algorithms. For text encryption, reverse-engineering the original s-box method was nearly impossible due to no available information on how to do so and loss of information when using s-boxes to turn a 48-bit sequence into a 32-bit sequence. As a result, we implemented a modified version of DES and s-boxes to ensure that no information was lost so that a decryption algorithm could be reverse-engineered. 
Another big challenge during the process with the theoretical understanding of the algorithms and converting very high level pseudocode into actual code. Many of the algorithms we implemented had very little actual code implementations that we can find and it made our process of implementation a lot more tricky. Similarly, it was also the first time for the two of us using Flask and a python backend for a web application. Learning the difference and similarities between Flask and the other languages that we are familiar with definitely took a lot of time. 

## Accomplishments that we're proud of
We both became familiar with the theory of introductory encryption with this project. Additionally, we are proud of our implementations of the encryption algorithms and overcoming the various problems and bugs we faced. Despite being relatively inexperienced with hackathons (Hoya Hacks 2024 is our first and second hackathon), we are proud of our project and how much we did in just 36 hours. 

## What we learned
This project and hackathon was a giant learning experience. We both learned the theory behind various introductory encryption algorithms and coded them for the first time. We also learned how to use Flask and various python libraries including cv2 (OpenCV) and PyWavelets. 

## What's next for P.E.N.G.U.
In the future, we would like to make our text-encryption algorithm more robust, such as 3DES (Triple Data Encryption Standard) or RSA (Rivest-Shamir-Adleman Algorithm). Additionally, we would like to fine-tune our image-steganography algorithm to better hide the image with the encrypted data. Finally, we would like to implement a feature that combines all three encryption methods: encrypts text in cipher-text, hides cipher-text data in an image, and hides that image in another image.
