from SIGNATURE.signMessage import sign_message, verify_signature

message = int(input("enter message: "))

message_signed = sign_message(message)

print(f"Message signed: {message_signed}")

pd = int(input("Please, enter private exponent: "))   
pn = int(input("Please, enter private modulus: "))

print(verify_signature(pd, pn, message_signed))