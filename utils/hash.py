import hashlib

def generar_hash(documento):

    return hashlib.sha256(

        str(documento).encode()

    ).hexdigest()