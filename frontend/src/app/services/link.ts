import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Link, LinkCreate, LinkUpdate } from '../interfaces/link.interface';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class LinkService {

  private http: HttpClient = inject(HttpClient);
  private apiUrl = environment.backendUrl; // Usaremos una variable de entorno para esto

  // Constructor opcional si solo usas inject()

  /**
   * Obtiene todos los enlaces del usuario autenticado.
   * @returns Un Observable de un array de enlaces.
   */
  getLinks(): Observable<Link[]> {
    return this.http.get<Link[]>(`${this.apiUrl}/links/`);
  }

  /**
   * Crea un nuevo enlace para el usuario autenticado.
   * @param linkData Los datos del nuevo enlace.
   * @returns Un Observable del enlace creado.
   */
  createLink(linkData: LinkCreate): Observable<Link> {
    return this.http.post<Link>(`${this.apiUrl}/links`, linkData);
  }

  /**
   * Actualiza un enlace existente.
   * @param linkId El ID del enlace a actualizar.
   * @param linkData Los datos a actualizar.
   * @returns Un Observable del enlace actualizado.
   */
  updateLink(linkId: string, linkData: LinkUpdate): Observable<Link> {
    return this.http.put<Link>(`${this.apiUrl}/links/${linkId}`, linkData);
  }

  /**
   * Elimina un enlace.
   * @param linkId El ID del enlace a eliminar.
   * @returns Un Observable de la respuesta (vacía si es exitoso).
   */
  deleteLink(linkId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/links/${linkId}`);
  }
}
