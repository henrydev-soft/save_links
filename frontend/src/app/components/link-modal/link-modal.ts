import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LinkService } from '../../services/link';
import { Link } from '../../interfaces/link.interface';


@Component({
  selector: 'app-link-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './link-modal.html',
  styleUrl: './link-modal.css'
})

export class LinkModal implements OnChanges {
  @Input() visible = false;
  @Input() existingLink: Link | null = null;
  @Output() close = new EventEmitter<void>();

  form: FormGroup;

  constructor(private fb: FormBuilder, private linkService: LinkService) {
    this.form = this.fb.group({
      title: ['', Validators.required],
      url: ['', [Validators.required, Validators.pattern('https?://.+')]],
      description: [''],
      tags: ['']
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['existingLink'] && this.existingLink) {
      this.form.patchValue(this.existingLink);
    }

    if (changes['visible'] && this.visible && !this.existingLink) {
      this.form.reset(); // nuevo enlace
    }
  }

  async submit(): Promise<void> {
    if (this.form.valid) {

      const rawData = this.form.value;
      const payload = {
        ...rawData,
        tags: rawData.tags
          ? rawData.tags.split(',').map((tag: string) => tag.trim()).filter(Boolean)
          : []
      };

    
      if (this.existingLink) {
        await this.linkService.updateLink(this.existingLink.id, payload);
      } else {
        await this.linkService.createLink(payload);
      }

      this.form.reset();
      this.close.emit();
    }
  }

  cancel(): void {
    this.form.reset();
    this.close.emit();
  }
}
