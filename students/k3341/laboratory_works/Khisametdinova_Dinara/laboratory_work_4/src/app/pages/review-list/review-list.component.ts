import { Component } from '@angular/core';
import { ReviewService } from '../../services/review.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-review-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css'],
})
export class ReviewListComponent {
  reviews: any[] = [];

  constructor(private reviewService: ReviewService) {
    this.loadReviews();
  }

  loadReviews() {
    this.reviewService.getReviews().subscribe((data) => {
      this.reviews = data;
    });
  }
}
