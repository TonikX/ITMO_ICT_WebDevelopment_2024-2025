import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  currentUser: any = null;
  isTeacher = false;

  constructor(private router: Router, private authService: AuthService) {
    this.currentUser = this.authService.getCurrentUser();
    this.isTeacher = this.currentUser?.role === 'teacher';
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    return !!this.authService.getCurrentUser(); 
  }

  navigateTo(route: string) {
    this.router.navigate([route]);
  }
  
  ngOnInit() {
    this.authService.getCurrentUserDetails().subscribe({
      next: (user) => {
        this.currentUser = user;
      },
      error: (error) => {
        console.error('Failed to fetch user details:', error);
      },
    });
  }
}