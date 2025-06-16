"""
Excepciones personalizadas para la aplicación

Define clases de error específicas para ser lanzadas a lo largo de la aplicación

Autor: Henry Jiménez
Fecha: 2025-06-16
"""


class AppException(Exception):
    """ Clase base de excepciones personalizadas para la aplicación """
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class UserNotFoundException(AppException):
    """ Excepcion personalizada para el caso de que el usuario no se encuentre en la base de datos """
    def __init__(self, user_id: str):
        super().__init__(f"Usuario con ID {user_id} no encontrado.", status_code=404)


class LinkNotFoundException(AppException):
    """ Excepcion personalizada para el caso de que el enlace no se encuentre en la base de datos """
    def __init__(self, link_id: str):
        super().__init__(f"Enlace con ID {link_id} no encontrado.", status_code=404)

class PermissionException(AppException):
    """ Excepcion personalizada para el caso de que el usuario no tenga permiso para realizar la operacion """
    def __init__(self):
        super().__init__(f"El usuario no tiene permiso para realizar esta operacion.", status_code=403)