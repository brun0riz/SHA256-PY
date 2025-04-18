import random
import utils as ut
from sympy import isprime

def generate_prime():
    while True:
        prime = random.randint(50, 200)
        if isprime(prime):
            return prime 
        
def choose_e(phi, n):
    while True:
        e = random.randint(2, phi-1) # has to be less than phi and greater than 1
        if isprime(e) and ut.gbc(e, phi) == 1 and ut.gbc(e, n) == 1: 
            return e

def calculate_d(e, phi):
    start = random.randint(1, phi)
    d = start
    while d < phi * 2:
        if (d * e) % phi == 1:
            return d
        d += 1

def sign_message(hash_message):
    # generate two distinct prime numbers
    # recive the prime numbers
    p = generate_prime()
    q = generate_prime()
    # check if p and q are equal, if true assign q a new prime number
    if p == q:
        q = generate_prime()

    # calculate n
    n = p * q
    
    # calculate phi(totiente) using the Euler function
    phi = (p-1)*(q-1)

    # choose e
    e = choose_e(phi, n)

    # calculate d
    d = calculate_d(e, phi)
    print(f"private exponent: {d}")
    print(f"private modulus: {n}")
    # sign the hash using the public key
    signature = pow(hash_message, e, n)

    print(f"signature: {signature}")

    return signature

def verify_signature(PD, PN, signature):
    
    decrypted_signature = pow(signature, PD, PN)
    print(f"signature: {signature}")
    print(f"Decrypted signature: {decrypted_signature}")

    return decrypted_signature
