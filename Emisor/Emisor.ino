/*
ver ::cl 20120520
Configuracion basica para modulo transmisor RT 11
Utiliza libreria VirtualWire.h
pin 01 entrada desde Arduino pin digital 2
pin 02 Tierra
pin 07 tierra
pin 08 antena externa
pin 09 tierra
pin 10 5v
*/

// Cabecera = n de secuencia
// CheckSum se calcula con toda la info menos checksum
#include <VirtualWire.h>

int secuencia = 0;
const uint8_t IdEmisor = 235;
const uint8_t IdReceptor = 135;
int bitIndex = 0;

uint8_t buffer[3];
int bytesRecibidos = 0;

// === CRC-8 con polinomio 0x07 ===
uint8_t crc8(const uint8_t *data, size_t len) {
  uint8_t crc = 0x00;
  for (size_t i = 0; i < len; i++) {
    crc ^= data[i];
    for (uint8_t j = 0; j < 8; j++) {
      if (crc & 0x80)
        crc = (crc << 1) ^ 0x07;
      else
        crc <<= 1;
    }
  }
  return crc;
}

void printByteAsBits(uint8_t b) {
  for (int i = 7; i >= 0; i--) {
    Serial.print(bitRead(b, i));
  }
  Serial.print(" ");
}

void setup() {
  vw_set_ptt_inverted(true);
  vw_setup(2000);
  vw_set_tx_pin(2);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Serial.println("Configurando envío...");
}

void loop() {

  while (Serial.available() > 0 && bytesRecibidos < 3) {
    buffer[bytesRecibidos++] = Serial.read();
  }


  if (bytesRecibidos == 3) {
    uint8_t paquete[7];
    paquete[0] = secuencia++;
    paquete[1] = IdEmisor;
    paquete[2] = IdReceptor;
    paquete[3] = buffer[0];
    paquete[4] = buffer[1];
    paquete[5] = buffer[2];
    paquete[6] = crc8(paquete, 6);
  

    vw_send(paquete, sizeof(paquete));
    vw_wait_tx();

    digitalWrite(13, HIGH);
    delay(200);
    digitalWrite(13, LOW);

    if (secuencia == 43){
      secuencia = 0;
    }


  Serial.print("Enviado (bits): ");
  for (int i = 0; i < 7; i++) {
    printByteAsBits(paquete[i]);
  }
  Serial.println("\n");

    bytesRecibidos = 0;
  }
}