from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

package_path    = "paquetes/paq.txt"
aux_array       = []
width_img       = 32
height_img      = 32
expected_data   = width_img * height_img
ID_tran         = 235
ID_recep        = 135


def open_package():
    package_array = []
    with open(package_path,"r") as archivo:
        aux_array = archivo.readlines()

    for i in aux_array:
        package_array.append(i.replace("\n",''))
    return package_array

def check_sum(package):
    aux_array = []
    for i in package:
        total_paq = 0
        total_check = 0

        paq = i[:-8]
        check = i[-8:]

        for j in paq:
            total_paq += int(j)
        total_check = int(check,2)

        if total_paq == total_check:
            print("check")
            aux_array.append(paq)
        else:
            print("No check")
            aux_array.append("ERROR")
    return aux_array

def check_order(package):
        aux_array = []
        for i in range(0,len(package)):
            aux_array.append(i)
        
        for i in package:
            seq = i[:8]
            paq = i[8:]
            aux_array[int(seq,2)] = paq
            print(f"linea agregada en la posicion {int(seq,2)}")
        
        return aux_array

def check_id(package):
    aux_array = []

    for i in package:
        ID_tran_received = i[:8]
        ID_recep_received = i[8:16]
        paq = i[16:]

        if int(ID_tran_received,2) == ID_tran and int(ID_recep_received,2) == ID_recep:
            aux_array.append(paq)
        else:
            aux_array.append("ERROR")
            exit

    return aux_array

def image_builder(img_array):
    img_string          = ""
    processed_img_array = []

    for i in img_array:
        img_string = img_string + i

    img_string = img_string.replace('0','a')
    img_string = img_string.replace('1','0')
    img_string = img_string.replace('a','1')

    if len(img_string) > expected_data:
        img_string = img_string[:expected_data]

    for i in range(0,height_img):
        processed_img_array.append(img_string[(width_img * i):(width_img * (i+1))])

    for i in processed_img_array:
        print(len(i))
        print(i)
    print(len(processed_img_array))

    

if __name__ == '__main__':
    package = open_package()
    print(package)
    package_checked = check_sum(package)
    print(package_checked)
    package_sorted = check_order(package_checked)
    print(package_sorted)
    img_array = check_id(package_sorted)
    print(img_array)
    image_builder(img_array)
