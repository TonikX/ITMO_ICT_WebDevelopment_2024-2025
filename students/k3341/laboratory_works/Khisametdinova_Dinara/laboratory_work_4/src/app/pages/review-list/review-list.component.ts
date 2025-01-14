import { Component } from '@angular/core';
import { ReviewService } from '../../services/review.service';
import { SubmissionService } from '../../services/submission.service';
import { TaskService } from '../../services/task.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-review-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css'],
})
export class ReviewListComponent {
  reviews: any[] = [];
  tasks: any[] = [];
  submissions: any[] = [];
  selectedTaskId: number | null = null;
  selectedTask: any = null;
  selectedSubmission: any = null;
  currentUser: any = null;

  editingReview: any = null;
  newReview = {
    score: '',
    comments: '',
    submission: null,
    criterion: null,
  };

  constructor(
    private reviewService: ReviewService,
    private submissionService: SubmissionService,
    private taskService: TaskService
  ) {
    this.loadReviews();
    this.loadTasks();
  }

  loadReviews() {
    this.reviewService.getReviews().subscribe((data) => {
      this.reviews = data;
    });
  }

  loadTasks() {
    this.reviewService.getAllTasks().subscribe((data) => {
      this.tasks = data;
    });
  }

  onTaskSelect(event: Event) {
    const target = event.target as HTMLSelectElement;
    const id = parseInt(target.value, 10);
    this.selectedTaskId = id;
    this.selectedTask = this.tasks.find((task) => task.id === id);
    this.reviewService.getSubmissionsByTask(id).subscribe((data: any[]) => {
      this.submissions = data;
    });
  }

  onSubmissionSelect(event: Event) {
    const target = event.target as HTMLSelectElement;
    const id = parseInt(target.value, 10);
    this.selectedSubmission = this.submissions.find((submission) => submission.id === id);
  }

  addReview() {
    if (!this.newReview.submission || !this.newReview.criterion || !this.newReview.score || !this.newReview.comments) {
      alert('Please fill in all fields.');
      return;
    }
    this.reviewService.createReview(this.newReview).subscribe({
      next: () => {
        alert('Review added successfully.');
        this.newReview = { score: '', comments: '', submission: null, criterion: null };
        this.loadReviews();
      },
      error: (err) => console.error('Error adding review:', err),
    });
  }

  editReview(review: any) {
    this.editingReview = { ...review };
  }

  saveReview() {
    if (!this.editingReview.score || !this.editingReview.comments) {
      alert('Please fill in all fields.');
      return;
    }
    this.reviewService.updateReview(this.editingReview.id, this.editingReview).subscribe({
      next: () => {
        alert('Review updated successfully.');
        this.editingReview = null;
        this.loadReviews();
      },
      error: (err) => console.error('Error updating review:', err),
    });
  }

  cancelEdit() {
    this.editingReview = null;
  }
}
