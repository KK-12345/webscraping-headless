import hashlib
import base64
from cryptography.fernet import Fernet
from utils.constants import GenericConstants as gc
from utils.exceptions import EncryptionError

def generate_key(seed: str = None) -> bytes:
    """
        Generating a key for encrypted password
        @param: seed - Initial seed
        @type: seed - str
    """
    try:
        if not seed:
            seed = gc.SECURE_PASSPHRASE.value
        hashed_seed = hashlib.sha256(seed.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(hashed_seed)
    except Exception as ex:
        raise EncryptionError(f"Error generating key, reason {str(ex)}")


def encrypt_data(data: str, seed: str = None) -> str:
    """
        Encrypting a string field using key
        @param: data - to encrypt
        @type: data - str
        @param: seed - encryption seed
        @type: seed - str
    """
    try:
        # logger.info("Encrypting")
        key = generate_key(seed)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data.encode())
        decoded = encrypted.decode()
        # logger.info("Encrypted")
        return decoded
    except Exception as ex:
        raise EncryptionError(f"Error encrypting data, reason {str(ex)}")

def decrypt_data(encrypted_data: str, seed: str = None) -> str:
    """
        Decrypting to get string field using key
        @param: data - to decrypt
        @type: data - str
        @param: key - decrypting key
        @type: key - bytes
    """
    try:
        key = generate_key(seed)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data.encode())
        decoded = decrypted.decode()
        return decoded
    except Exception as ex:
        raise EncryptionError(f"Error decrypting data, reason {str(ex)}")



if __name__ == "__main__":
    seed = "my_secure_passphrase"
    data = "kk@9623194889"

    # Encrypt the data
    encrypted = encrypt_data(data, seed)
    print(f"Encrypted Data: {encrypted}")

    # Decrypt the data
    decrypted = decrypt_data(encrypted, seed)
    print(f"Decrypted Data: {decrypted}")
