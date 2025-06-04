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


#Transforma las ids a usuarios
ID_tran_bin = bin(ID_tran)[2:]
ID_recep_bin = bin(ID_recep)[2:]

#Transforma los numeros de la secuancia a binario
for num_seq in range(0,len(data_matrix)):
    num_seq_bin = bin(num_seq)[2:]
    if len(num_seq_bin) != 8:
        num_seq_aux = num_seq_bin
        for i in range(0,8 - len(num_seq_bin)):
            num_seq_aux = "0" + num_seq_aux
    seq_array.append(num_seq_aux)    

#Agrega el checksum y lo guarda en el array a mandar
for i in range(0,len(data_matrix)):
    paq_wo_check = seq_array[i] + ID_tran_bin + ID_recep_bin + data_matrix[i]
    checksum = 0

    for j in paq_wo_check:
        checksum += int(j)
    
    checksum_bin = bin(checksum)[2:]
    if len(num_seq_bin) != 8:
        checksum_aux = checksum_bin
        for i in range(0,8 - len(checksum_bin)):
            checksum_aux = "0" + checksum_aux
    
    paq_check = paq_wo_check + checksum_aux
    paq_array.append(paq_check)
    
with open("paquetes/paq.txt",'w+') as archivo:
    for i in paq_array:
        archivo.write(i + "\n")

#print(paq_array)


