"""
Configuración global de logging

Este módulo configura un logger estándar reutilizable en toda la aplicación.
Permite registrar eventos, errores y trazas de ejecución para debugging o monitoreo.

Autor: Henry Jiménez
Fecha: 2025-06-11
"""

import logging

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formato del log
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Asociar el handler al logger si no se ha configurado antes
if not logger.hasHandlers():
    logger.addHandler(console_handler)