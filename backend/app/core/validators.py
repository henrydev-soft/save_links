"""
Módulo compartido de validacón de datos
Este módulo contiene funciones de validación personalizadas. 

Usada principalmente por los Dtos del proyecto. 

Autor: Henry Jiménez
Fecha: 2025-06-16

"""

import validators


def check_length(field: str, value: str, max_length: int, min_length: int = 0) -> str:
    """ Valida que el campo no exceda la longitud permitida."""
    if len(value) > max_length:
        raise ValueError(f"El campo {field} no debe exceder {max_length} caracteres.")
    if len(value) < min_length:
        raise ValueError(f"El campo {field} debe tener al menos {min_length} caracteres.")
    return value


def is_valid_url(url: str) -> str:
    """ Valida que la URL sea válida."""    
    if not validators.url(url):
        raise ValueError("La URL no es válida.")
    return url

def is_valid_email(email: str) -> str:
    """ Valida que el correo electrónico sea valido."""
    if not validators.email(email):
        raise ValueError("El correo electrónico no es valido.")
    return email