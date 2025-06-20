"""
Repositorio Firebase para entidades de dominio

Este módulo inicializa e importa los repositorios implementados
usando Firebase como backend de persistencia. Cada clase aquí
implementa una interfaz definida en la capa de dominio.

Actualmente disponibles:
- FirebaseLinkRepository: Implementación de ILinkRepository
"""

from .firebase_link_repository import FirebaseLinkRepository
from .firebase_user_repository import FirebaseUserRepository

__all__ = ["FirebaseLinkRepository", "FirebaseUserRepository"]