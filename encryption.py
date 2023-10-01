from Crypto.Protocol.KDF import PBKDF2
from dotenv import dotenv_values
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto import Random
import base64

def encrypt(key, source, encode=True):
	"""Encrypt a source message using a key.

	Args:
		key (bytes): The key with which you want to encrypt as bytes.
		source (str): The message to encrypt.
		encode (bool): Whether to encode the output in base64. Default is true.

	Returns:
		str: Base64 encoded cipher
	"""

	source = source.encode()
	IV = Random.new().read(AES.block_size)  # generate IV
	encryptor = AES.new(key, AES.MODE_CBC, IV)
	padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
	source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
	data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
	return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True):
	"""Decrypt a source message using a key.

	Args:
		key (bytes): Key to decrypt with as bytes.
		source: The cipher (or encrypted message) to decrypt.
		decode (bool): Whether to first base64 decode the cipher before trying to decrypt with the key. Default is true.

	Returns:
		str: The decrypted message.
	"""

	source = source.encode()
	if decode:
		source = base64.b64decode(source)

	IV = source[:AES.block_size]  # extract the IV from the beginning
	decryptor = AES.new(key, AES.MODE_CBC, IV)
	data = decryptor.decrypt(source[AES.block_size:])  # decrypt
	padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
	if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
		raise ValueError("Invalid padding...")
	return data[:-padding]  # remove the padding

def compute_vault_key(master_password):
	"""Compute the vault key using master password and secret key.
	
	Args:
		master_password (str): The Master password.

	Returns:
		bytes: The vault key.
	"""
	
	secret_key = dotenv_values(".env").get("SECRET_KEY")
	vault_key = PBKDF2(master_password.encode(), secret_key.encode(), 32, count=1000000, hmac_hash_module=SHA512)
	return vault_key