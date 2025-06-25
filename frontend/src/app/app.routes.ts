import { Routes } from '@angular/router';
import { Login } from './components/login/login';
import { Signup } from './components/signup/signup';
import { Links } from './components/links/links';
import { Dashboard } from './components/dashboard/dashboard';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
    { path: 'login', component: Login },
    { path: 'signup', component: Signup },
    { 
        path: '', 
        component: Dashboard, 
        canActivate: [authGuard] // Protege la ruta de Links con el guardia de autenticación
    },

    // Redirecciones iniciales
    { path: '', redirectTo: '/login', pathMatch: 'full' }, // Si la ruta es vacía, redirige a login
    { path: '**', redirectTo: '/login' } // Para cualquier ruta no encontrada, también redirige a login
];
