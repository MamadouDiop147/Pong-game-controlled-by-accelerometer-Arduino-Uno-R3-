#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Initialise l'Arduino et l'accéléromètre
void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
  
  // Vérifie la connexion avec l'accéléromètre
  if (!mpu.testConnection()) {
    Serial.println("Echec de connexion avec l'accéléromètre MPU-6050");
    while (1);
  }
}

// Lit les données de l'accéléromètre et les envoie via le port série
void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Utilise uniquement les données de l'axe Y pour contrôler la palette
  Serial.println(ay);
  delay(10);
}
