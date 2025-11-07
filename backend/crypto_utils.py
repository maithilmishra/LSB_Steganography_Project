# backend/crypto_utils.py
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import base64, os, hashlib

# -----------------------------
# 🔹 AES-GCM Encryption Helpers
# -----------------------------
def aes_gcm_encrypt(plaintext: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    parts = [base64.b64encode(x).decode('utf-8') for x in (cipher.nonce, tag, ct)]
    return ":".join(parts)

def aes_gcm_decrypt(blob: str, key: bytes) -> str:
    nonce_b64, tag_b64, ct_b64 = blob.split(":")
    nonce = base64.b64decode(nonce_b64)
    tag = base64.b64decode(tag_b64)
    ct = base64.b64decode(ct_b64)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)
    return pt.decode('utf-8')

# -----------------------------
# 🔹 Key Generation
# -----------------------------
def generate_session_keys():
    """Generate fresh AES key (32 bytes) and randomization key (16-byte base64)."""
    aes_key = os.urandom(32)
    rand_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    return aes_key, rand_key

# -----------------------------
# 🔹 RSA Wrapping / Unwrapping
# -----------------------------
def rsa_wrap_keys(aes_key: bytes, rand_key: str, receiver_pub_pem: str) -> str:
    pub = RSA.import_key(receiver_pub_pem)
    cipher = PKCS1_OAEP.new(pub)
    payload = base64.b64encode(aes_key).decode('utf-8') + ":" + rand_key
    wrapped = cipher.encrypt(payload.encode('utf-8'))
    return base64.b64encode(wrapped).decode('utf-8')

def rsa_unwrap_keys(wrapped_b64: str, receiver_priv_pem: str):
    priv = RSA.import_key(receiver_priv_pem)
    cipher = PKCS1_OAEP.new(priv)
    wrapped = base64.b64decode(wrapped_b64)
    payload = cipher.decrypt(wrapped).decode('utf-8')
    aes_b64, rand_key = payload.split(":", 1)
    aes_key = base64.b64decode(aes_b64)
    return aes_key, rand_key
# -----------------------------

