import { Component, OnInit } from '@angular/core';
import { ReportService } from '../../services/reports.service';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-report',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css'],
  standalone: true,
  imports: [CommonModule],
})
export class ReportComponent implements OnInit {
  currentUser: any;
  tasksUploaded: any[] = [];
  tasksReviewed: any[] = [];
  averageScore: number | null = null;
  averageScoreForUser: number | null = null;
  personalStatistics: any = null; 
  taskStatistics: {
    tasks: number;
    submissions: number;
    reviews: number;
  } | null = null;
  constructor(
    private reportService: ReportService,
    private authService: AuthService
  ) {
    this.currentUser = this.authService.getCurrentUser();
  }

  ngOnInit() {
    if (this.currentUser.role === 'teacher') {
      this.loadUploadedTasks();
    } else if (this.currentUser.role === 'student') {
      this.loadReviewedTasks();
    }

    this.loadAverageScoreByUsername();
    this.loadTaskStatistics();
    this.loadPersonalStatistics();
  }

  loadUploadedTasks() {
    this.reportService.getUploadedTasks(this.currentUser.id).subscribe((data) => {
      this.tasksUploaded = data;
    });
  }

  loadReviewedTasks() {
    this.reportService.getReviewedTasks(this.currentUser.id).subscribe((data) => {
      this.tasksReviewed = data;
    });
  }

  loadAverageScoreByUsername() {
    this.reportService
      .getAverageScoreByUsername(this.currentUser.username)
      .subscribe((data) => {
        this.averageScoreForUser = data.average_score;
      });
  }

  loadTaskStatistics() {
    this.reportService.getTaskStatistics().subscribe((data) => {
      this.taskStatistics = data;
    });
  }

  loadPersonalStatistics() {
    this.reportService.getPersonalStatistics().subscribe((data) => {
      this.personalStatistics = data;
    });
  }
}
