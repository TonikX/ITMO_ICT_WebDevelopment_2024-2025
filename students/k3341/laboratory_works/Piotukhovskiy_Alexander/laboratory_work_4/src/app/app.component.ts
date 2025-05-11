import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [
    RouterOutlet
  ]
})
export class AppComponent {
  constructor(private http: HttpClient) {}


}
