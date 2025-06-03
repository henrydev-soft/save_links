"""
Archivo de configuración para inicializar Firebase Admin SDK.
Este archivo contiene la lógica para inicializar Firebase Admin SDK utilizando las credenciales
proporcionadas en la configuración de la aplicación.
"""

import firebase_admin
from firebase_admin import credentials
from app.core.settings import settings # Importa la instancia de settings

def initialize_firebase():
    if not firebase_admin._apps:
        if settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH:
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK inicializado.")
        else:
            # Esto es una advertencia, la aplicación aún puede iniciar si no se usa Firebase Auth
            print("Advertencia: FIREBASE_SERVICE_ACCOUNT_KEY_PATH no configurado. Firebase Auth no funcionará.")