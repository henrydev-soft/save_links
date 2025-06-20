"""
Versión 1 de la API REST

Este paquete agrupa todos los componentes de la versión 1 de la API expuesta por la aplicación.
Incluye:

- `api_router.py`: enrutador principal que agrega todos los módulos de rutas.
- `dependences.py`: funciones comunes para inyección de dependencias (por ejemplo, base de datos).

Este diseño permite escalar hacia múltiples versiones (v1, v2...) sin afectar la estructura base.

Autor: Henry Jiménez
Fecha: 2025-06-19
"""

from .api_router import api_v1_router