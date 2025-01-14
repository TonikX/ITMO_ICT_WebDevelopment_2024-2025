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
export class NavbarComponent implements OnInit {
  currentUser: any = null;
  isTeacher = false;
  isSuperUser = false;

  constructor(private router: Router, private authService: AuthService) {}

  ngOnInit() {
    this.authService.getCurrentUserDetails().subscribe({
      next: (user) => {
        this.currentUser = user;
        this.isTeacher = this.currentUser?.role === 'teacher';
        this.isSuperUser = this.currentUser?.is_superuser;
      },
      error: (error) => {
        console.error('Failed to fetch user details:', error);
      },
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  navigateTo(route: string): void {
    this.router.navigate([route]);
  }
}
