"""
Archivo de configuración para inicializar Firebase Admin SDK.
Este archivo contiene la lógica para inicializar Firebase Admin SDK utilizando las credenciales
proporcionadas en la configuración de la aplicación.
"""

import firebase_admin
from firebase_admin import credentials, firestore
from app.core import settings


if not firebase_admin._apps:
    # Ruta al archivo de credenciales
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK inicializado.")
else:
    # Esto es una advertencia, la aplicación aún puede iniciar si no se usa Firebase Auth
    print("Advertencia: FIREBASE_CREDENTIALS_PATH no configurado. Firebase Auth no funcionará.")

firebase_client = firestore.client()