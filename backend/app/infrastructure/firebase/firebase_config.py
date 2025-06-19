"""
Archivo de configuración para inicializar Firebase Admin SDK.
Este archivo contiene la lógica para inicializar Firebase Admin SDK utilizando las credenciales
proporcionadas en la configuración de la aplicación.
"""


import firebase_admin
from firebase_admin import credentials, firestore
import os

# Ruta al archivo de credenciales (ajusta según tu entorno)
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "path/to/credentials.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

firebase_client = firestore.client()