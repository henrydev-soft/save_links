import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LinkModal } from '../link-modal/link-modal';

@Component({
  selector: 'app-header-controls',
  standalone: true,
  imports: [CommonModule, LinkModal],
  templateUrl: './header-controls.html',
  styleUrl: './header-controls.css'
})
export class HeaderControls {

  showModal = false;

  openModal(): void {
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
  }

}
