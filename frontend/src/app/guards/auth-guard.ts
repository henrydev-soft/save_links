import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth-service'; // Importa el servicio de autenticación
import { map, take } from 'rxjs/operators';
import { Observable } from 'rxjs'; // Necesario para tipar el retorno
import { UrlTree } from '@angular/router';



export const authGuard: CanActivateFn = (route, state): Observable<boolean | UrlTree> => {
  
  // Inyecta el AuthService
  const authService = inject(AuthService); 
  // Inyecta el Router
  const router = inject(Router);        

  return authService.isAuthenticated().pipe(
    take(1), // Toma solo la primera emisión y completa el Observable
    map(isAuthenticated => {
      if (isAuthenticated) {
        return true; // Permite el acceso a la ruta
      } else {
        // Si no está autenticado, redirige a la página de login
        console.log('Usuario no autenticado. Redirigiendo a /login');
        return router.createUrlTree(['/login']); // Crea un UrlTree para redirigir
      }
    })
  );
};
