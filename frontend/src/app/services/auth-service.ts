import { Injectable, inject } from '@angular/core';
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, authState, User } from '@angular/fire/auth';
import { setLogLevel, LogLevel } from "@angular/fire";
import { Observable, from, of } from 'rxjs'; 
import { switchMap, map, catchError } from 'rxjs/operators';
import { Router } from '@angular/router'; 

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Inyecta el servicio Auth de Firebase
  private auth: Auth = inject(Auth);
  // Inyecta el servicio Router de Angular
  private router: Router = inject(Router);

  

  // Observable que emite el usuario autenticado
  user$: Observable<User | null>;
  // Observable que emite el UID del usuario autenticado
  currentUserId$: Observable<string | null>;  

  constructor() {

    setLogLevel(LogLevel.VERBOSE);

    // user$ se inicializa con el estado de autenticación de Firebase
    // authState() es un observable que emite el usuario cuando cambia el estado.
    this.user$ = authState(this.auth);

    // currentUserId$ se deriva de user$ para obtener solo el UID
    this.currentUserId$ = this.user$.pipe(
      map(user => user ? user.uid : null)
    );
  }

  /**
   * Registra un nuevo usuario con email y contraseña.
   * @param email Email del usuario.
   * @param password Contraseña del usuario.
   * @returns Observable que emite el usuario registrado o un error.
   */
  signUp(email: string, password: string): Observable<any> {
    return from(createUserWithEmailAndPassword(this.auth, email, password)).pipe(
      catchError(error => {
        console.error("Error during sign up:", error);
        throw error; // Propaga el error para que el componente lo maneje
      })
    );
  }

  /**
   * Inicia sesión con email y contraseña.
   * @param email El correo electrónico del usuario.
   * @param password La contraseña del usuario.
   * @returns Un Observable que emite el UserCredential o lanza un error.
   */
  signIn(email: string, password: string): Observable<any> {
    return from(signInWithEmailAndPassword(this.auth, email, password)).pipe(
      catchError(error => {
        console.error("Error during sign in:", error);
        throw error; // Propaga el error para que el componente lo maneje
      })
    );
  }

  /**
   * Cierra la sesión del usuario actual.
   * @returns Un Observable que completa cuando la sesión se cierra, o lanza un error.
   */
  signOut(): Observable<void> {
    return from(signOut(this.auth)).pipe(
      map(() => {
        console.log("User signed out.");
        this.router.navigate(['/login']); // Redirige al login después de cerrar sesión
      }),
      catchError(error => {
        console.error("Error during sign out:", error);
        throw error;
      })
    );
  }

  /**
   * Obtiene el ID Token actual del usuario.
   * Este token es necesario para autenticar las peticiones al backend de FastAPI.
   * @returns Un Observable que emite el ID Token o null si no hay usuario autenticado.
   */
  getIdToken(): Observable<string | null> {
    return this.user$.pipe(
      switchMap(user => {
        if (user) {
          return from(user.getIdToken());
        }
        return of(null);
      }),
      catchError(error => {
        console.error("Error getting ID Token:", error);
        return of(null); // Retorna null en caso de error para evitar romper la aplicación
      })
    );
  }

  /**
   * Verifica si el usuario está autenticado.
   * @returns Un Observable que emite true si el usuario está autenticado, false en caso contrario.
   */
  isAuthenticated(): Observable<boolean> {
    return this.user$.pipe(
      map(user => !!user) // Convierte el usuario (o null) a un booleano
    );
  }

  /**
   * Permite obtener el id del usuario
   * @returns uid del usuario
   */
  async getCurrentUserId(): Promise<string | null> {
    const user = await this.auth.currentUser;
    return user ? user.uid : null;
  }



}
