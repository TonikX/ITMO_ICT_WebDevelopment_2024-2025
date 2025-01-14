import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { HomeService } from '../../services/home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class HomeComponent implements OnInit {
  currentUser: any;
  uploadedTasks: any[] = [];
  uploadedSubmissions: any[] = [];
  reviews: any[] = [];
  selectedDetails: any = null;

  constructor(
    private authService: AuthService,
    private homeService: HomeService
  ) {}

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUser();
    if (!this.currentUser) {
      console.error('No current user found.');
      return;
    }

    if (this.currentUser.role === 'teacher') {
      this.loadUploadedTasks();
    } else if (this.currentUser.role === 'student') {
      this.loadUploadedSubmissions();
      this.loadReviews();
    }
  }

  loadUploadedTasks(): void {
    this.homeService.getUploadedTasks(this.currentUser.id).subscribe({
      next: (tasks) => (this.uploadedTasks = tasks),
      error: (err) => console.error('Ошибка при загрузке заданий:', err),
    });
  }

  loadUploadedSubmissions(): void {
    this.homeService.getUploadedSubmissions(this.currentUser.id).subscribe({
      next: (submissions) =>
        (this.uploadedSubmissions = submissions.filter(
          (sub: any) => sub.user.id === this.currentUser.id
        )),
      error: (err) => console.error('Ошибка при загрузке submissions:', err),
    });
  }

  loadReviews(): void {
    this.homeService.getReviews(this.currentUser.id).subscribe({
      next: (reviews) =>
        (this.reviews = reviews.filter(
          (review: any) => review.user.id === this.currentUser.id
        )),
      error: (err) => console.error('Ошибка при загрузке reviews:', err),
    });
  }

  loadTaskDetails(taskId: number): void {
    this.homeService.getTaskDetails(taskId).subscribe({
      next: (details) => (this.selectedDetails = details),
      error: (err) => console.error('Ошибка при загрузке деталей задания:', err),
    });
  }

  loadSubmissionDetails(submissionId: number): void {
    this.homeService.getSubmissionDetails(submissionId).subscribe({
      next: (details) => (this.selectedDetails = details),
      error: (err) =>
        console.error('Ошибка при загрузке деталей submission:', err),
    });
  }
}
