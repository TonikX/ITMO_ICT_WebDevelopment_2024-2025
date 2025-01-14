import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../services/user.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css'],
})
export class UserListComponent implements OnInit {
  users: any[] = [];
  filteredUsers: any[] = [];
  filter: string = '';
  selectedRole: string | null = null;
  isSuperUser: boolean = false;
  newUser = {
    first_name: '',
    last_name: '',
    email: '',
    role: 'student',
  };

  constructor(private userService: UserService, private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.getCurrentUserDetails().subscribe({
      next: (data) => {
        this.isSuperUser = data.is_superuser;
        this.loadUsers();
      },
      error: (err) => console.error('Error fetching current user:', err),
    });
  }

  loadUsers(): void {
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.applyFilters();
      },
      error: (err) => console.error('Error loading users:', err),
    });
  }

  applyFilters(): void {
    this.filteredUsers = this.users.filter(
      (user) =>
        (!this.filter || user.first_name.toLowerCase().includes(this.filter.toLowerCase()) ||
          user.last_name.toLowerCase().includes(this.filter.toLowerCase())) &&
        (!this.selectedRole || user.role === this.selectedRole)
    );
  }

  addUser(): void {
    if (!this.newUser.first_name || !this.newUser.last_name || !this.newUser.email) {
      alert('Please fill in all fields.');
      return;
    }

    this.userService.createUser(this.newUser).subscribe({
      next: () => {
        this.loadUsers();
        this.newUser = { first_name: '', last_name: '', email: '', role: 'student' };
      },
      error: (err) => console.error('Error creating user:', err),
    });
  }

  deleteUser(userId: number): void {
    if (confirm('Are you sure you want to delete this user?')) {
      this.userService.deleteUser(userId).subscribe({
        next: () => this.loadUsers(),
        error: (err) => console.error('Error deleting user:', err),
      });
    }
  }
}
