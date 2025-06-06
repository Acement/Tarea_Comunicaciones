from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img_path = './Imagenes/imagen_32x32.jpg'
img_size = 32
data_size= 24
ID_tran = 235
ID_recep = 135
data_matrix = []
seq_array = []
paq_array = []

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
    
with open("paquetes/paq.txt",'w+') as archivo:
    for i in data_matrix:
        archivo.write(i + "\n")

#print(paq_array)


