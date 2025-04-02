import unicodedata
import utils as ut

def message_block(string):
    # Convert the string to binary
    string_n = unicodedata.normalize("NFC", string)  # Normaliza os acentos
    stringBinary = ''.join(format(byte, '08b') for byte in string_n.encode('utf-8'))

    # Add a '1' to the end of the string
    stringBinary += '1'

    # Prepend the string to the message block
    while (len(stringBinary) % 512) != 448:
        stringBinary += '0'

    # Append the length of the string in bits
    stringBinary += format(len(string) * 8, '064b')

    return stringBinary

def create_chunk(block_message):
    # Split the message into chunks of 512 bits, including the last chunk even if it's smaller than 512 bits
    chunks = []
    for i in range(0, len(block_message), 512):
        chunks.append(block_message[i:i + 512])
    return chunks

def rotate_and_shift_a0(line_block):
    line_block = int(line_block, 2)
    a0R7 = (line_block >> 7) | (line_block << (25)) & 0xFFFFFFFF
    a0R18 = (line_block >> 18) | (line_block << (14)) & 0xFFFFFFFF
    a0S3 = line_block >> 3
    return format((a0R7 ^ a0R18 ^ a0S3), '032b')

def rotate_and_shift_a1(line_block):
    line_block = int(line_block, 2)
    a1R17 = (line_block >> 17) | (line_block << (15)) & 0xFFFFFFFF
    a1R19 = (line_block >> 19) | (line_block << (13)) & 0xFFFFFFFF
    a1S10 = line_block >> 10
    return format((a1R17 ^ a1R19 ^ a1S10), '032b')

def CalculateSigma0(a):
    eR2 = ut.right_rotate(a, 2)
    eR13 = ut.right_rotate(a, 13)
    eR22 = ut.right_rotate(a, 22)
    sigma0 = eR2 ^ eR13 ^ eR22

    return format(sigma0, '032b')

def CalculateSigma1(e):
    eR6 = ut.right_rotate(e, 6)
    eR11 = ut.right_rotate(e, 11)
    eR25 = ut.right_rotate(e, 25)
    sigma1 = eR6 ^ eR11 ^ eR25

    return format(sigma1, '032b')

def CalculateMajority(a, b, c):
    a = int(a, 2)
    b = int(b, 2)
    c = int(c, 2)
    return format((a & b) ^ (a & c) ^ (b & c), '032b')

def CalculateChoice(e, f, g):
    e = int(e, 2)
    f = int(f, 2)
    g = int(g, 2)
    return format(((e & f) ^ (~(e) & g)), '032b')

def CalculateTemp1(h, M1, Choice, k, w):
    h = int(h, 2)
    M1 = int(M1, 2)
    Choice = int(Choice, 2)
    k = int(k, 2)
    w = int(w, 2)
    
    temp1 = (h + M1 + Choice + k + w) & 0xFFFFFFFF  
    return format(temp1, '032b')

def CalculateTemp2(M0, Majority):
    M0 = int(M0, 2)
    Majority = int(Majority, 2)
    
    temp2 = (M0 + Majority) & 0xFFFFFFFF  
    return format(temp2, '032b')

def CalculateE(d, Temp1):
    d = int(d, 2)
    Temp1 = int(Temp1, 2)
    
    e = (d + Temp1) & 0xFFFFFFFF
    return format(e, '032b')

def CalculateA(Temp1, Temp2):
    Temp1 = int(Temp1, 2)
    Temp2 = int(Temp2, 2)
    a = (Temp1 + Temp2) & 0xFFFFFFFF
    return format(a, '032b')

def message_schedule(chunks):
    # here we are going to run trough the chunks and create the message schedule

# Inicialize the hash values
    h0 = format(int(ut.get_fractional_part((2**0.5)) * (2**32)), '032b')
    h1 = format(int(ut.get_fractional_part((3**0.5)) * (2**32)), '032b')
    h2 = format(int(ut.get_fractional_part((5**0.5)) * (2**32)), '032b')
    h3 = format(int(ut.get_fractional_part((7**0.5)) * (2**32)), '032b')
    h4 = format(int(ut.get_fractional_part((11**0.5)) * (2**32)), '032b')
    h5 = format(int(ut.get_fractional_part((13**0.5)) * (2**32)), '032b')
    h6 = format(int(ut.get_fractional_part((17**0.5)) * (2**32)), '032b')
    h7 = format(int(ut.get_fractional_part((19**0.5)) * (2**32)), '032b')

    for chunk in chunks:
        w=[]
        
        # split the chunk into 16 words of 32 bits each
        for i in range(0, 512, 32):
            w.append(chunk[i:i+32])
        if len(w) < 64:
            w += ['0' * 32] * (64 - len(w))            
        i = 0
        # Rotate and shift the values
        while (i+16) < 64:
            a0 = rotate_and_shift_a0(w[i+1])
            a1 = rotate_and_shift_a1(w[i+14])

            new_val = (int(w[i], 2) + int(a0, 2) + int(w[i+9], 2) + int(a1, 2)) % (2**32)
            w[i+16] = format(new_val, '032b') 

            i += 1

        # Initialize the constants
        prime_list = ut.get_prime_numbers(64)
        k = []
        # print("PRIME LIST")
        for i in range(0, 64):
            frac_part = int(ut.get_fractional_part((prime_list[i]**(1/3))) * (2**32))
            k.append(format(frac_part, '032b'))
            # print(k[i])
        # Incialize the working variables
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        print("\n")

        for i in range(64):
            # Calculate the Majority and Chioce variables
            Majority = CalculateMajority(a, b, c)
            Choice = CalculateChoice(e, f, g)
           
            # Calculate the M0 and M1 variables
            M1 = CalculateSigma1(e)

            M0 = CalculateSigma0(a)

            # Calculate the temp variables
            Temp1 = CalculateTemp1(h, M1, Choice, k[i], w[i])
            Temp2 = CalculateTemp2(M0, Majority)

            # shuffle the working variables
            h = g
            g = f
            f = e
            e = CalculateE(d, Temp1)
            d = c
            c = b
            b = a
            a = CalculateA(Temp1, Temp2)
        
        h0 = format((int(h0, 2) + int(a, 2)) & 0xFFFFFFFF, '032b')
        h1 = format((int(h1, 2) + int(b, 2)) & 0xFFFFFFFF, '032b')
        h2 = format((int(h2, 2) + int(c, 2)) & 0xFFFFFFFF, '032b')
        h3 = format((int(h3, 2) + int(d, 2)) & 0xFFFFFFFF, '032b')
        h4 = format((int(h4, 2) + int(e, 2)) & 0xFFFFFFFF, '032b')
        h5 = format((int(h5, 2) + int(f, 2)) & 0xFFFFFFFF, '032b')
        h6 = format((int(h6, 2) + int(g, 2)) & 0xFFFFFFFF, '032b')
        h7 = format((int(h7, 2) + int(h, 2)) & 0xFFFFFFFF, '032b')

    h0 = int(h0, 2)
    h1 = int(h1, 2)
    h2 = int(h2, 2)
    h3 = int(h3, 2)
    h4 = int(h4, 2)
    h5 = int(h5, 2)
    h6 = int(h6, 2)
    h7 = int(h7, 2) 

    hash_SHA256 = ''.join(format(h, '08x') for h in [h0, h1, h2, h3, h4, h5, h6, h7])

    return hash_SHA256

########### MAIN ###########
string_to_encrypt = input("Enter the string to encrypt: ")
# The first step is to covert the string to binary and add a '1' to the end of the string
# The '1' will be our delimiter

block_message = message_block(string_to_encrypt)
# here create the block message

print("LENGTH: ", len(block_message))
""" NEED TO BE 512 BITS per BLOCK """

# Now we have to create the chuncks, they will be 512 bits long
chunks = create_chunk(block_message)
print("\nCHUNKS: ", chunks)

# The next step is to create the message schedule
hash_256 = message_schedule(chunks)

print("HASH SHA256: ", hash_256)





