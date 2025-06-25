import { Component, OnInit, HostListener  } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Link } from '../../interfaces/link.interface';
import { LinkService } from '../../services/link';
import { LinkModal } from '../link-modal/link-modal';
import { AsyncPipe } from '@angular/common';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-link-list',
  standalone: true,
  imports: [CommonModule, AsyncPipe, LinkModal],
  templateUrl: './link-list.html',
  styleUrl: './link-list.css'
})
export class LinkList implements OnInit{
  
  links$!: Observable<Link[]>;
  openMenuId: string | null = null;
  linkToEdit: Link | null = null;
  openEditModal = false;

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    const isMenuButton = target.closest('.menu-toggle');
    const isMenuContent = target.closest('.menu-content');
    
    if (!isMenuButton && !isMenuContent) {
      this.openMenuId = null;
    }
  }
  
  constructor(private linkService: LinkService) {}

  async ngOnInit(): Promise<void> {
    this.links$ = this.linkService.links$;
    await this.linkService.loadLinks();
  }

  onCloseModal(): void {
    this.openEditModal = false;
    this.linkToEdit = null;
    this.openMenuId = null;
  }

  toggleMenu(linkId: string): void {
    this.openMenuId = this.openMenuId === linkId ? null : linkId;
  }

  editLink(link: Link): void {
    this.linkToEdit = link;       
    this.openEditModal = true;
    this.openMenuId = null;
  }

  confirmDelete(linkId: string): void {
    if (confirm('¿Deseas eliminar este enlace?')) {
      this.linkService.deleteLink(linkId).then(() => {
        this.linkService.loadLinks(); // Refresca la lista
      });
    }
    this.openMenuId = null;
  }

}
