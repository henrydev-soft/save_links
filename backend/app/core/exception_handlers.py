"""
Controladores globales de excepciones

Este módulo define manejadores personalizados para capturar errores comunes en toda
la aplicación FastAPI. Permite registrar respuestas estructuradas y centralizar el logging
de errores para mantener los servicios limpios y enfocados en la lógica de negocio.

Se deben registrar en `main.py` durante la creación de la app.

Autor: Henry Jiménez
Fecha: 2025-06-20
"""

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logger import logger
from app.core.exceptions import AppException



def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"[AppException] {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"[422 ValidationError] {exc.errors()}")
        
        sanitized_errors = []
        for err in exc.errors():
            sanitized_error = {
                "field": ".".join(str(part) for part in err.get("loc", [])),
                "message": err.get("msg"),
            }
            sanitized_errors.append(sanitized_error)

        return JSONResponse(
            status_code=422,
            content={
                "detail": "Error de validación en la solicitud.",
                "errors": sanitized_errors
            },
        )
    
    # Método no permitido (405): personalizado
    async def method_not_allowed_handler(request: Request, exc):
        logger.warning(f"[405] Método no permitido: {request.method} en {request.url}")
        return JSONResponse(
            status_code=405,
            content={"detail": "Método HTTP no permitido para este endpoint."},
        )
    app.add_exception_handler(405, method_not_allowed_handler)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"[Unhandled Exception] {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error inesperado en el servidor."},
        )