from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

path = input("Podaj ścieżkę do pliku z danymi do zaszyfrowania: ")

with open(path, "r", encoding="utf-8") as f:
    data = f.read().encode("utf-8")



key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce
print(ciphertext)
