import { Component } from '@angular/core';
import { SubmissionService } from '../../services/submission.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-submission-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './submission-list.component.html',
  styleUrls: ['./submission-list.component.css'],
})
export class SubmissionListComponent {
  submissions: any[] = [];

  constructor(private submissionService: SubmissionService) {
    this.loadSubmissions();
  }

  loadSubmissions() {
    this.submissionService.getSubmissions().subscribe((data) => {
      this.submissions = data;
    });
  }
}
