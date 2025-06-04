import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthService } from '../../services/auth-service'; // Importa el servicio de autenticación
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, CommonModule],
  templateUrl: './signup.html',
  styleUrl: './signup.css'
})
export class Signup {
  signupForm: FormGroup;
  errorMessage: string | null = null;

  private fb: FormBuilder = inject(FormBuilder);
  private authService: AuthService = inject(AuthService);
  private router: Router = inject(Router);

  constructor() {
    this.signupForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.min(6)]] // Firebase requiere min 6 caracteres
    });
  }

  async onSubmit() {
    this.errorMessage = null;
    if (this.signupForm.valid) {
      const { email, password } = this.signupForm.value;
      try {
        // Llama al servicio de autenticación para registrar al usuario
        await firstValueFrom(this.authService.signUp(email, password));
        // Notifica al usuario del éxito y redirige
        alert('Registro exitoso. ¡Ahora puedes iniciar sesión!'); 
        this.router.navigate(['/links']);
      } catch (error: any) {
        console.error("Sign up failed:", error);
        if (error.code === 'auth/email-already-in-use') {
          this.errorMessage = 'El email ya está en uso.';
        } else if (error.code === 'auth/weak-password') {
          this.errorMessage = 'La contraseña es demasiado débil (mínimo 6 caracteres).';
        } else {
          this.errorMessage = 'Ocurrió un error al registrarse. Inténtalo de nuevo.';
        }
      }
    } else {
      this.errorMessage = 'Por favor, completa todos los campos correctamente.';
    }
  }

}
