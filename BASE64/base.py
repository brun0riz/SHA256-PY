# Tabela de caracteres do Base64
TABELA_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def texto_para_base64(texto):
    if type(texto) != bytes:
        binario = ''.join(format(ord(c), '08b') for c in texto)
    else:
        binario = ''.join(format(b, '08b') for b in texto)
    # Converter texto para binário (8 bits por caractere)
    
    # Certificar que o comprimento seja múltiplo de 6 (preencher com 0 se necessário)
    while len(binario) % 6 != 0:
        binario += '0'

    # Dividir a string binária em grupos de 6 bits
    grupos = [binario[i:i+6] for i in range(0, len(binario), 6)]
    
    # Converter cada grupo de 6 bits para um número decimal
    indices = [int(grupo, 2) for grupo in grupos]
    
    # Mapear os números para caracteres Base64
    base64_str = ''.join(TABELA_BASE64[i] for i in indices)
    
    # Adicionar '=' para manter múltiplo de 4 caracteres no final
    while len(base64_str) % 4 != 0:
        base64_str += '='
    
    return base64_str

def base64_para_texto(texto_codificado):
    texto_codificado = texto_codificado.replace('=', '')
    # print(texto_codificado)

    # Converter caracteres Base64 para números
    indices = [TABELA_BASE64.index(c) for c in texto_codificado]
    # print(indices)

    # Converter números para binário (6 bits por caractere)
    binario = ''.join(format(i, '06b') for i in indices)
    # print(binario)

    # Dividir a string binária em grupos de 8 bits
    grupos = [binario[i:i+8] for i in range(0, len(binario), 8)]

    # Converter cada grupo de 8 bits para um número decimal
    numeros = [int(grupo, 2) for grupo in grupos]

    # Converter números para caracteres ASCII
    texto = ''.join(chr(i) for i in numeros)
    # print("Texto Decodificado:", texto)

    return texto
    


def encrypt_base64(text_to_encrypt):
    return texto_para_base64(text_to_encrypt)

