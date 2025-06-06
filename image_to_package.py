from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img_path = './Imagenes/imagen_32x32.jpg'
img_size = 32
data_size= 24
ID_tran = 235
ID_recep = 135

clave_caesar = 4

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
        primero = matrix[i][:8]
        segundo = matrix[i][8:16]
        tercero = matrix[i][16:24]

        primero_caesar = int(primero,2) + clave_caesar
        segundo_caesar = int(segundo,2) + clave_caesar
        tercero_caesar = int(tercero,2) + clave_caesar

        aux_array = [primero_caesar, segundo_caesar, tercero_caesar]

        for j in range(0,len(aux_array)):
            while aux_array[j] > 255:
                aux_array[j] = aux_array[j] - 255
            aux_array[j] = bin(aux_array[j])[2:]

        

        for j in range(0,len(aux_array)):
            if len(aux_array[j]) < 8:
                for k in range(0,8 - len(aux_array[j]) ):
                    aux_array[j] = "0" + aux_array[j]

        print(f"Sin cifrar  : {primero}, {segundo}, {tercero}")
        print(f"Cifrado     : {aux_array[0]}, {aux_array[1]}, {aux_array[2]}")

        matrix[i] = aux_array[0] + aux_array[1] + aux_array[2]



    return matrix

# Cifrado Asimetrico


def save(matrix):
    with open("paquetes/paq.txt",'w+') as archivo:
        for i in matrix:
            archivo.write(i + "\n")

#print(paq_array)

if __name__ == "__main__":
    matriz_datos = data_matrix_build()

    print("1.- Cifrado Simentrico")
    print("2.- Cifrado Asimetrico")
    opt = input("Selecione: ")
    matriz_datos = caesar_cipher(matriz_datos)

    save(matriz_datos)

