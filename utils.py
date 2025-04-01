def print_em_blocos(texto):
    for i in range(0, len(texto), 8):
        print(texto[i:i+8], end="  ")
        if (i // 8 + 1) % 4 == 0:
            print()

def print_blocos(array):
    for bloco in enumerate(array, start=0):
        print(bloco)

def right_rotate(value, rotate_bits):
    # Converte o valor para inteiro se necessário e realiza a rotação à direita
    value = int(value, 2)
    return (value >> rotate_bits | value << (32 - rotate_bits)) & 0xFFFFFFFF

def get_fractional_part(number):
    fractional_part = number - int(number)
    return fractional_part 

def get_prime_numbers(quant_prime):
    prime_numbers = []
    i = 2

    while len(prime_numbers) != quant_prime:
        # test to see if i is prime
        # if i is divisible by any number other than 1 and itself, it is not prime
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                break
        else:
            prime_numbers.append(i)
        i += 1

    return prime_numbers

