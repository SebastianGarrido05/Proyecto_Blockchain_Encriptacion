from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
import os

# GENERAR KEY
def generar_llave():
    return get_random_bytes(32)


# CIFRAR ARCHIVO
def cifrar_archivo(nombre_archivo, llave):
    with open(nombre_archivo, 'rb') as f:
        data = f.read()

    cipher = AES.new(llave, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open("archivo_cifrado.bin", "wb") as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

    print("Archivo cifrado como 'archivo_cifrado.bin'")

# DESCIFRAR ARCHIVO
def descifrar_archivo(nombre_archivo, llave):
    with open(nombre_archivo, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(llave, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    with open("archivo_descifrado.txt", "wb") as f:
        f.write(data)

    print("Archivo descifrado como 'archivo_descifrado.txt'")

# CLI
def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python crypto_tool.py cifrar archivo.txt")
        print("  python crypto_tool.py descifrar archivo_cifrado.bin")
        return

    accion = sys.argv[1]
    archivo = sys.argv[2]

    llave = generar_llave()

    # Guardar key
    with open("llave.key", "wb") as f:
        f.write(llave)

    if accion == "cifrar":
        cifrar_archivo(archivo, llave)

    elif accion == "descifrar":
        # Cargar key
        if not os.path.exists("llave.key"):
            print("No se encontró la llave.")
            return

        with open("llave.key", "rb") as f:
            llave = f.read()

        descifrar_archivo(archivo, llave)

    else:
        print("Acción no válida. Usa 'cifrar' o 'descifrar'.")

if __name__ == "__main__":
    main()