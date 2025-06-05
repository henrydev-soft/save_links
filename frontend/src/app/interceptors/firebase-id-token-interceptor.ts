import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth-service';
import { switchMap, take } from 'rxjs/operators';


export const firebaseIdTokenInterceptor: HttpInterceptorFn = (req, next) => {
  // Inyecta el servicio de autenticación
  const authService = inject(AuthService);

  // No interceptar peticiones a la API de Firebase (son de Firebase a Firebase)
  if (req.url.startsWith('https://securetoken.googleapis.com/') || req.url.startsWith('https://www.googleapis.com/')) {
    return next(req);
  }

  return authService.getIdToken().pipe(
    take(1), // Tomar el último token y completar
    switchMap(token => {
      if (token) {
        // Clonar la petición y añadir el encabezado de autorización
        const clonedReq = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`
          }
        });
        return next(clonedReq);
      } else {
        // Si no hay token, simplemente procede con la petición original (sin token)
        // Esto es útil para rutas públicas o si el usuario no está logueado
        return next(req);
      }
      
    })
  );

  return next(req);
};
