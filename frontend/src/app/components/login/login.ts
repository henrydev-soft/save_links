import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthService } from '../../services/auth-service'; // Importa el servicio de autenticación
import { Router, RouterLink } from '@angular/router'; // Importa RouterLink para el enlace a registro
import { CommonModule } from '@angular/common'; // Necesario para ngIf
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  // Formulario de inicio de sesión
  loginForm: FormGroup;
  // Mensaje de error para mostrar en la interfaz
  errorMessage: string | null = null;

  // Inyección de dependencias
  private fb: FormBuilder = inject(FormBuilder);
  private authService: AuthService = inject(AuthService);
  private router: Router = inject(Router);

  constructor() {
    // Inicializa el formulario de inicio de sesión con validaciones
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  // Método para iniciar sesión
  async onSubmit() {
    // Limpia el mensaje de error al intentar iniciar sesión
    this.errorMessage = null;

    // Verifica si el formulario es válido
    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value;

      try {
        // Llama al servicio de autenticación para iniciar sesión
        await firstValueFrom(this.authService.signIn(email, password));;
        // Redirige al usuario a la página principal después de iniciar sesión
        await this.router.navigate(['/']);
      } catch (error: any) {
        console.error("Login failed:", error);
        if (error.code === 'auth/invalid-credential' || error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
          this.errorMessage = 'Credenciales inválidas. Verifica tu email y contraseña.';
        } else if (error.code === 'auth/user-disabled') {
          this.errorMessage = 'Tu cuenta ha sido deshabilitada.';
        } else {
          this.errorMessage = 'Ocurrió un error al iniciar sesión. Inténtalo de nuevo.';
        }
      }
    } else {
      this.errorMessage = 'Por favor, completa todos los campos correctamente.';
    }
  }

}
