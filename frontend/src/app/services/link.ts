import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { Link, LinkCreate, LinkUpdate } from '../interfaces/link.interface';
import { environment } from '../../environments/environment';
import { AuthService } from './auth-service';


@Injectable({
  providedIn: 'root'
})

export class LinkService {

  private http: HttpClient = inject(HttpClient);
  private apiUrl = environment.backendUrl; // Usaremos una variable de entorno para esto
  private authService = inject(AuthService);

  private linksSubject = new BehaviorSubject<Link[]>([]);
  links$ = this.linksSubject.asObservable();


  /**
   * 
   * @param path url
   * @returns url con id de usuario autenticado.
   */
  private async buildUrl(path: string): Promise<string> {
    const uid = await this.authService.getCurrentUserId();
    if (!uid) throw new Error('Usuario no autenticado');
    return `${this.apiUrl}/${uid}${path}`;
  }

  /**
   * Obtiene todos los enlaces del usuario autenticado.
   */
  async loadLinks(): Promise<void> {
    try {
      const url = await this.buildUrl('/links');
      const links = await firstValueFrom(this.http.get<Link[]>(url));
      this.linksSubject.next(links);
    } catch (error) {
      console.error('Error al cargar enlaces', error);
      this.linksSubject.next([]);
    }
  }


  /**
   * Crea un nuevo enlace para el usuario autenticado.
   * @param linkData Los datos del nuevo enlace.
   */
  async createLink(linkData: LinkCreate): Promise<void> {
    const url = await this.buildUrl('/links');
    const newLink =await firstValueFrom(this.http.post<Link>(url, linkData));

    // Actualiza solo el estado local sin recargar todo
    const currentLinks = this.linksSubject.value;
    this.linksSubject.next([...currentLinks, newLink]);
  }

  /**
   * Actualiza un enlace existente.
   * @param linkId El ID del enlace a actualizar.
   * @param linkData Los datos a actualizar.
   * @returns Un Observable del enlace actualizado.
   */
  async updateLink(linkId: string, linkData: LinkUpdate): Promise<void> {
    const url = await this.buildUrl(`/links/${linkId}`);
    const updatedLink = await firstValueFrom(this.http.put<Link>(url, linkData));

    // Reemplaza solo el enlace modificado
    const currentLinks = this.linksSubject.value;
    const updatedLinks = currentLinks.map(link =>
      link.id === linkId ? updatedLink : link
    );
    this.linksSubject.next(updatedLinks);
  }

  /**
   * Elimina un enlace.
   * @param linkId El ID del enlace a eliminar.
   * @returns Un Observable de la respuesta (vacía si es exitoso).
   */
  async deleteLink(linkId: string): Promise<void> {
    const url = await this.buildUrl(`/links/${linkId}`);
    await firstValueFrom(this.http.delete<void>(url));

    // Elimina el enlace localmente
    const currentLinks = this.linksSubject.value;
    const filteredLinks = currentLinks.filter(link => link.id !== linkId);
    this.linksSubject.next(filteredLinks);
  }
}
