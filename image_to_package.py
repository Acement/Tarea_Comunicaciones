from PIL import Image
import numpy as np

img_path    = "./Imagenes/imagen_32x32.jpg"
paq_path    = "paquetes/paq.txt"
img_size    = 32
data_size   = 24
ID_tran     = 235
ID_recep    = 135

clave_caesar = 4

prime_1 = 7
prime_2 = 13

public = 19
private = 307

def data_matrix_build():
    data_matrix = []
    #Abre la imagen y la transforma a pixel
    img = Image.open(img_path)
    img = img.convert('1')
    img_array = np.array(img)
    img_bin = ''.join(format(pixel, '1') for row in img_array for pixel in row)

    #Guarda la informacion del paquete en arreglos
    aux_c = 0
    aux_c_img_bin = 0
    aux_string = ''

    for pix in img_bin:
        aux_string += pix
        aux_c += 1
        aux_c_img_bin += 1
        if aux_c == data_size or aux_c_img_bin == len(img_bin):
            if len(aux_string) < data_size:
                for i in range(0, data_size-len(aux_string)):
                    aux_string = aux_string + "0"
            data_matrix.append(aux_string)
            aux_c = 0
            aux_string = ''
    
    return data_matrix

#Cifrado Cesar
def caesar_cipher(matrix):
    for i in range(0,len(matrix)):

        #Separa los paquetes en 3 bytes
        primero = matrix[i][:8]
        segundo = matrix[i][8:16]
        tercero = matrix[i][16:24]

        
        #Pasa los valores a int y le suma la clave cesar
        primero_caesar = int(primero,2) + clave_caesar
        segundo_caesar = int(segundo,2) + clave_caesar
        tercero_caesar = int(tercero,2) + clave_caesar

        aux_array = [primero_caesar, segundo_caesar ,tercero_caesar]  

        #Los valores que se pasan de 8 bits se regresan a 0 y pasa todos los valores a binario
        for j in range(0,len(aux_array)):

            while aux_array[j] > 255:
                aux_array[j] = aux_array[j] - 256
            aux_array[j] = bin(aux_array[j])[2:]

        #Por como funciona la operacion de pasar a bineario, este bloque de codigo le agrega los 0 que faltan para que sean 8 bits
        for j in range(0,len(aux_array)):
            if len(aux_array[j]) < 8:
                for k in range(0,8 - len(aux_array[j])):
                    aux_array[j] = "0" + aux_array[j]


        matrix[i] = aux_array[0] + aux_array[1] + aux_array[2]

    print ("Terminado cifrado simetrico")
    return matrix

# Cifrado Asimetrico
def asymetric_cipher(matrix):
    cipher_matrix = []
    
    print()
    n = prime_1 * prime_2
    phi = (prime_1 - 1) * (prime_2 - 1)

    print(f"n       : {n}")
    print(f"phi     : {phi}")
    print(f"public key  : ({public},{n})")
    print(f"private key : ({private},{n})")
    print()

    for i in range(0,len(matrix)):
        primero = matrix[i][:8]
        segundo = matrix[i][8:16]
        tercero = matrix[i][16:24]

        aux_array = [primero, segundo, tercero]

        for j in range(0,len(aux_array)):
            aux = bin(pow(int(aux_array[j],2),public) % n)[2:]
            if (len(aux)) < 8:
                for k in range(0,8 - len(aux)):
                    aux = "0" + aux
        
        cipher_matrix.append(aux_array[0] + aux_array[1] + aux_array[2])

    print("Terminado cifrado asimetrico")
    return cipher_matrix


def save(matrix):
    with open(paq_path,'w+') as archivo:
        for i in matrix:
            archivo.write(i + "\n")


if __name__ == "__main__":
    check = True

    matriz_datos = data_matrix_build()

    while check: 
        print("1.- Cifrado Simentrico")
        print("2.- Cifrado Asimetrico")
        opt = input("Selecione: ")
        match(int(opt)):
            case 1:
                matriz_datos = caesar_cipher(matriz_datos)
                check = False
            case 2:
                matriz_datos = asymetric_cipher(matriz_datos)
                check = False
            case _:
                print("ERROR! Ingrese una opcion valida")

    save(matriz_datos)
    print(f"Proceso imagen a paquete terminado, guardado en: {paq_path}")

