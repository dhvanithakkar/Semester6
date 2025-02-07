def generate_key(message, key):
    """Extends the key to match the length of the message"""
    key = key.lower()
    if len(message) == len(key):
        return key
    else:
        key = (key * (len(message)//len(key) + 1))[:len(message)]
        return key

def encrypt(message, key):
    """
    Encrypts a message using the Vigenère cipher
    Formula: ci = (pi + ki) mod 26
    Where:
    ci = encrypted letter
    pi = position of plaintext letter
    ki = position of key letter
    """
    cipher_text = []
    message = message.lower()
    key = generate_key(message, key)
    
    for i in range(len(message)):
        if message[i].isalpha():
            # Convert letters to numbers (a=0, b=1, etc.)
            p_i = ord(message[i]) - ord('a')
            k_i = ord(key[i]) - ord('a')
            
            # Apply Vigenère formula
            c_i = (p_i + k_i) % 26
            
            # Convert back to letter
            cipher_text.append(chr(c_i + ord('a')))
        else:
            # Keep non-alphabetic characters unchanged
            cipher_text.append(message[i])
            
    return ''.join(cipher_text)

def decrypt(cipher_text, key):
    """
    Decrypts a message using the Vigenère cipher
    Formula: pi = (ci - ki) mod 26
    Where:
    pi = decrypted letter
    ci = position of ciphertext letter
    ki = position of key letter
    """
    plain_text = []
    cipher_text = cipher_text.lower()
    key = generate_key(cipher_text, key)
    
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            # Convert letters to numbers (a=0, b=1, etc.)
            c_i = ord(cipher_text[i]) - ord('a')
            k_i = ord(key[i]) - ord('a')
            
            # Apply inverse Vigenère formula
            p_i = (c_i - k_i) % 26
            
            # Convert back to letter
            plain_text.append(chr(p_i + ord('a')))
        elif cipher_text[i] == ' ':
            continue
        else:
            # Keep non-alphabetic characters unchanged
            plain_text.append(cipher_text[i])
            
    return ''.join(plain_text)

# Example usage
if __name__ == "__main__":
    message = "Hello World"
    key = "KEY"
    
    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)
    
    print(f"Original message: {message}")
    print(f"Key: {key}")
    print(f"Encrypted message: {encrypted}")
    print(f"Decrypted message: {decrypted}")
