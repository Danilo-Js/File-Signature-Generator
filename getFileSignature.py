import hashlib
import os

diretorio = input('Type the path you want to generate signatures: ')

# Computes the signature of a file using a specific hash
def calculaAssinaturaArquivo(hash, file):
    try:
        # Generate the hash object
        hashObj = hashlib.new(hash)
        
        # Open the file in binary mode "rb"
        with open(file, 'rb') as f:
            # Read the file in blocks of 4096 bytes and update the hash object with those blocks
            for chunk in iter(lambda: f.read(4096), b''):
                hashObj.update(chunk)
        
        # Returns the signature of the file in hexadecimal format
        # Depending on the algorithm, we need to specify the size of the hash output via the parameter
        if hash == 'shake_128' or hash == 'shake_256':
            return hashObj.hexdigest(32)
        else:
            return hashObj.hexdigest()
    
    # Returns None in case of error when opening the file
    except IOError:
        return None

# Fetch the signatures of files in a directory and its subdirectories
def buscaAssinaturas(path):
    # Make the directory an absolute path
    caminho = os.path.join(os.path.expanduser("~"), path)

    # Store file signatures
    assinaturas = {}
    
    # Traverse the dir and its subdirs
    for root, dirs, files in os.walk(caminho, topdown=True):
        for arquivo in files:
            # Get the full path of the file
            arquivo_caminho = os.path.join(root, arquivo)

            # Iterates over all available hashing algorithms
            for algoritmo in hashlib.algorithms_available:
                # Calculate the signature of the file
                assinatura = calculaAssinaturaArquivo(algoritmo, arquivo_caminho)
                
                # If the signature was calculated
                if assinatura:
                    # Create an entry for the file in the signatures object (only if it doesn't exist)
                    if arquivo_caminho not in assinaturas:
                        assinaturas[arquivo_caminho] = {}
                    
                    # Add the signature of the file using the current algorithm to the dictionary
                    assinaturas[arquivo_caminho][algoritmo] = assinatura

    # Returns the dictionary of file signatures
    return assinaturas

# Fetch file signatures
assinaturas = buscaAssinaturas(diretorio)

# Print the signatures
print('\n\n\n')
for file, assinaturas_algoritmos in assinaturas.items():
    print(f'File: {file}\n')
    for algoritmo, assinatura in assinaturas_algoritmos.items():
        print(f'Signature  - {algoritmo}: {assinatura}')
    print('\n\n\n')
