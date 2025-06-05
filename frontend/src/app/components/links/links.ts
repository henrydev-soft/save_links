
import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common'; // Para ngIf, ngFor
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms'; // Para formularios de añadir/editar
import { AuthService } from '../../services/auth-service';
import { LinkService } from '../../services/link'; // Importa tu LinkService
import { Link, LinkCreate, LinkUpdate } from '../../interfaces/link.interface'; // Importa tus interfaces
import { Subscription } from 'rxjs'; // Necesario para Observables y Subscriptions


@Component({
  selector: 'app-links',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './links.html',
  styleUrl: './links.css'
})
export class Links  implements OnInit, OnDestroy {
  
  private linkService: LinkService = inject(LinkService); // Inyecta el LinkService
  private fb: FormBuilder = inject(FormBuilder);
  private authService: AuthService = inject(AuthService); // Inyecta el servicio de autenticación

  userEmail: string | null = null; // Para mostrar el email del usuario
  links: Link[] = []; // Array para almacenar los enlaces
  linkForm: FormGroup; // Formulario para añadir/editar enlaces
  editingLink: Link | null = null; // Para saber si estamos editando o añadiendo
  errorMessage: string | null = null; // Mensajes de error

  private userSubscription: Subscription | null = null;
  private linksSubscription: Subscription | null = null;

  constructor() {
    // Inicializa el formulario con FormBuilder    
    this.linkForm = this.fb.group({
      title: ['', Validators.required],
      url: ['', [Validators.required, Validators.pattern('https?://.+')]], // Validar URL
      description: ['']
    });
  }

  ngOnInit(): void {
    // Suscribirse al email del usuario
    this.userSubscription = this.authService.user$.subscribe(user => {
      this.userEmail = user ? user.email : null;
      if (user) {
        this.loadLinks(); // Cargar enlaces solo si hay un usuario logueado
      } else {
        this.links = []; // Limpiar enlaces si el usuario se desloguea
      }
    });
  }

  ngOnDestroy(): void {
    // Desuscribirse para evitar fugas de memoria
    this.userSubscription?.unsubscribe();
    this.linksSubscription?.unsubscribe();
  }

  loadLinks(): void {
    this.errorMessage = null;
    this.linksSubscription = this.linkService.getLinks().subscribe({
      next: (data) => {
        this.links = data;
      },
      error: (err) => {
        console.error('Error al cargar enlaces:', err);
        this.errorMessage = 'No se pudieron cargar los enlaces. ¿Está tu backend corriendo y configurado correctamente?';
      }
    });
  }

  // Prepara el formulario para añadir un nuevo enlace
  addNewLink(): void {
    this.editingLink = null;
    this.linkForm.reset();
    this.errorMessage = null;
  }

  // Prepara el formulario para editar un enlace existente
  editLink(link: Link): void {
    this.editingLink = link;
    this.linkForm.patchValue(link); // Rellena el formulario con los datos del enlace
    this.errorMessage = null;
  }

  // Envía el formulario para añadir o actualizar un enlace
  submitLink(): void {
    this.errorMessage = null;
    if (this.linkForm.valid) {
      const linkData: LinkCreate | LinkUpdate = this.linkForm.value;

      if (this.editingLink) {
        // Actualizar enlace existente
        this.linkService.updateLink(this.editingLink.id, linkData).subscribe({
          next: () => {
            alert('Enlace actualizado con éxito.'); // O usa una notificación más elegante
            this.loadLinks(); // Recarga los enlaces para ver el cambio
            this.addNewLink(); // Resetea el formulario
          },
          error: (err) => {
            console.error('Error al actualizar enlace:', err);
            this.errorMessage = 'Error al actualizar el enlace.';
          }
        });
      } else {
        // Crear nuevo enlace
        this.linkService.createLink(linkData as LinkCreate).subscribe({
          next: () => {
            alert('Enlace creado con éxito.');
            this.loadLinks();
            this.addNewLink();
          },
          error: (err) => {
            console.error('Error al crear enlace:', err);
            this.errorMessage = 'Error al crear el enlace.';
          }
        });
      }
    } else {
      this.errorMessage = 'Por favor, rellena todos los campos requeridos correctamente.';
    }
  }

  // Eliminar un enlace
  deleteLink(linkId: string): void {
    if (confirm('¿Estás seguro de que quieres eliminar este enlace?')) {
      this.linkService.deleteLink(linkId).subscribe({
        next: () => {
          alert('Enlace eliminado con éxito.');
          this.loadLinks(); // Recarga los enlaces
        },
        error: (err) => {
          console.error('Error al eliminar enlace:', err);
          this.errorMessage = 'Error al eliminar el enlace.';
        }
      });
    }
  }

  // Método para cerrar sesión
  logout(): void {
    this.authService.signOut().subscribe({
      error: (err) => {
        console.error('Error al cerrar sesión:', err);
        alert('No se pudo cerrar la sesión.');
      }
    });
  }

}
