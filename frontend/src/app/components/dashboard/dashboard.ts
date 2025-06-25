import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderControls } from '../header-controls/header-controls';
import { LinkList } from '../link-list/link-list';
import { Sidebar } from '../sidebar/sidebar';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    HeaderControls,
    LinkList,
    Sidebar
  ],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard {}
