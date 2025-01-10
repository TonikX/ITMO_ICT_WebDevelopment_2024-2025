import { Component, OnInit } from '@angular/core';
import { SubmissionService } from '../../services/submission.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-submission-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './submission-list.component.html',
  styleUrls: ['./submission-list.component.css'],
})
export class SubmissionListComponent implements OnInit {
  submissions: any[] = [];
  filteredSubmissions: any[] = [];
  tasks: any[] = [];
  selectedTaskId: number | null = null; 
  selectedTaskDetails: any = null; 
  newSubmissionContent: string = '';
  searchQuery: string = '';

  constructor(private submissionService: SubmissionService) {}

  ngOnInit(): void {
    this.loadSubmissions();
    this.loadTasks();
  }

  loadSubmissions(): void {
    this.submissionService.getSubmissions().subscribe((data) => {
      this.submissions = data;
      this.filteredSubmissions = data; 
    });
  }

  loadTasks(): void {
    this.submissionService.getAllTasks().subscribe((tasks) => {
      this.tasks = tasks;
    });
  }

  onTaskSelect(taskId: number | null): void {
    if (taskId !== null) {
      this.selectedTaskId = taskId;
      this.loadTaskDetails(taskId);
    }
  }

  loadTaskDetails(taskId: number): void {
    this.submissionService.getTaskDetails(taskId).subscribe((details) => {
      this.selectedTaskDetails = details;
    });
  }

  addSubmission(): void {
    if (!this.newSubmissionContent.trim()) {
      alert('Submission content cannot be empty!');
      return;
    }

    const newSubmission = {
      task: this.selectedTaskId,
      content: this.newSubmissionContent,
    };

    this.submissionService.createSubmission(newSubmission).subscribe({
      next: () => {
        this.newSubmissionContent = '';
        this.loadSubmissions();
      },
      error: (err) => console.error('Error creating submission:', err),
    });
  }
}
