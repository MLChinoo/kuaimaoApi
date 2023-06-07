from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad, unpad

KEY = "625202f9149maomi".encode("UTF-8")
IV = "5efd3f6060emaomi".encode("UTF-8")


def encrypt(data: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ciphertext = cipher.encrypt(pad(data.encode("UTF-8"), AES.block_size))
    return ciphertext.hex().upper()


def decrypt(data: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    plaintext = unpad(cipher.decrypt(bytes.fromhex(data)), AES.block_size)
    return plaintext.decode("UTF-8")


def signature(data: str) -> str:
    md5_hash = MD5.new()
    salted_text = "data=" + data + "maomi_pass_xyz"
    md5_hash.update(salted_text.encode("UTF-8"))
    return md5_hash.hexdigest()
