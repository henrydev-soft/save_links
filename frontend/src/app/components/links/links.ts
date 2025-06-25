
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

export class Links {
  
}

/*
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
  }

  async loadLinks(): Promise<void> {
    this.errorMessage = null;
    try {
      this.links = await this.linkService.getLinks();
    } catch (error: any) {
      console.error('Error al cargar los enlaces:', error);
      this.errorMessage = 'Error al cargar los enlaces.';
    }
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
  async submitLink(): Promise<void> {
    this.errorMessage = null;
    if (this.linkForm.valid) {
      const linkData: LinkCreate | LinkUpdate = this.linkForm.value;

      try {
        if (this.editingLink) {
          await this.linkService.updateLink(this.editingLink.id, linkData);
          alert('Enlace actualizado con éxito.');
        } else {
          await this.linkService.createLink(linkData as LinkCreate);
          alert('Enlace creado con éxito.');
        }

        this.loadLinks();
        this.addNewLink();
      } catch (err) {
        console.error('Error al guardar enlace:', err);
        this.errorMessage = 'Error al guardar el enlace.';
      }

    } else {
      this.errorMessage = 'Por favor, rellena todos los campos requeridos correctamente.';
    }
  }

  // Eliminar un enlace
  async deleteLink(linkId: string): Promise<void> {
    if (confirm('¿Estás seguro de que quieres eliminar este enlace?')) {
      try {
        await this.linkService.deleteLink(linkId);
        alert('Enlace eliminado con éxito.');
        this.loadLinks();
      } catch (err) {
        console.error('Error al eliminar enlace:', err);
        this.errorMessage = 'Error al eliminar el enlace.';
      }
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

} */
