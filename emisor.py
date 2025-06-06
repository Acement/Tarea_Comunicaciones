import serial
import time

# === CONFIGURA ESTO PRIMERO ===
PUERTO = "/dev/ttyACM0"       # Cambia según tu PC (ej: 'COM4', '/dev/ttyUSB0', etc.)
BAUDIOS = 9600
TIEMPO_ENTRE_PAQUETES = 1  # segundos entre paquetes

# === CARGAR ARCHIVO CON MATRIZ DE BITS ===
with open("paquetes/paq.txt", "r") as f:
    contenido = f.read()

# Filtra solo bits y agrupa en bloques de 24
bits = ''.join(filter(lambda c: c in '01', contenido))

if len(bits) % 24 != 0:
    print("⚠️ Advertencia: cantidad de bits no es múltiplo de 24")  

# === CONECTAR A ARDUINO ===
try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
    time.sleep(5)  # espera a que Arduino reinicie
    print(f"✅ Conectado a {PUERTO}")
except:
    print(f"❌ No se pudo conectar a {PUERTO}")
    exit()

# === ENVIAR CADA GRUPO DE 3 BYTES ===
while(True):
    for i in range(0, len(bits), 24):
        bloque = bits[i:i+24].ljust(24, '0')  # completa si faltan bits
        paquete = bytearray()

        for j in range(0, 24, 8):
            byte_bin = bloque[j:j+8]
            byte_val = int(byte_bin, 2)
            paquete.append(byte_val)

        arduino.write(paquete)
        print(f"📤 Enviado: {[f'{b:08b}' for b in paquete]}")
        time.sleep(TIEMPO_ENTRE_PAQUETES)
    print("Serie Terminada")

arduino.close()
print("✅ Todos los datos fueron enviados.")